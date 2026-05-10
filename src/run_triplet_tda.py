from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

TMPDIR = ROOT / ".tmp"
TMPDIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("TMPDIR", str(TMPDIR))
os.environ.setdefault("PYSCF_TMPDIR", str(TMPDIR))

from backends.pyscf_backend import (
    excitation_rows,
    load_scf_result_from_chkfile,
    run_tda,
    run_triplet_uks,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run triplet UKS + TDA for a molecule XYZ using the PySCF backend."
    )
    parser.add_argument("--xyz", required=True, type=Path, help="Input XYZ file")
    parser.add_argument("--charge", required=True, type=int, help="Total molecular charge")
    parser.add_argument(
        "--multiplicity",
        required=True,
        type=int,
        help="Spin multiplicity, e.g. 3 for a triplet",
    )
    parser.add_argument("--xc", default="b3lyp", help="XC functional for UKS/TDA")
    parser.add_argument("--basis", required=True, help="Basis set name")
    parser.add_argument("--nroots", default=10, type=int, help="Number of TDA roots")
    parser.add_argument(
        "--grid-level",
        default=3,
        type=int,
        help="PySCF numerical integration grid level for DFT",
    )
    parser.add_argument(
        "--density-fit",
        action="store_true",
        help="Enable PySCF density fitting for faster hybrid DFT/TDA runs",
    )
    parser.add_argument(
        "--chkfile",
        type=Path,
        help="Path to a PySCF SCF checkpoint file for saving or restart",
    )
    parser.add_argument(
        "--restart-from-chkfile",
        action="store_true",
        help="Skip SCF and load a converged reference from --chkfile",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for summary JSON and excitations CSV",
    )
    parser.add_argument("--verbose", default=4, type=int, help="PySCF verbosity level")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    spin = args.multiplicity - 1
    if args.restart_from_chkfile:
        if args.chkfile is None:
            raise ValueError("--restart-from-chkfile requires --chkfile")
        scf_result = load_scf_result_from_chkfile(args.chkfile, xc=args.xc)
    else:
        scf_result = run_triplet_uks(
            xyz_path=args.xyz,
            charge=args.charge,
            spin=spin,
            xc=args.xc,
            basis=args.basis,
            chkfile_path=args.chkfile,
            density_fit=args.density_fit,
            grid_level=args.grid_level,
            verbose=args.verbose,
        )

    summary = {
        "xyz": str(args.xyz),
        "charge": args.charge,
        "multiplicity": args.multiplicity,
        "spin": spin,
        "xc": args.xc,
        "basis": args.basis,
        "nroots": args.nroots,
        "grid_level": args.grid_level,
        "density_fit": args.density_fit,
        "chkfile": str(args.chkfile) if args.chkfile else None,
        "restart_from_chkfile": args.restart_from_chkfile,
        "energy_hartree": scf_result.energy_hartree,
        "s2": scf_result.s2,
        "tda_completed": False,
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    tda_result = run_tda(scf_result=scf_result, nroots=args.nroots)
    rows = excitation_rows(tda_result)
    pd.DataFrame(rows).to_csv(args.output_dir / "excitations.csv", index=False)
    summary["tda_completed"] = True
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
