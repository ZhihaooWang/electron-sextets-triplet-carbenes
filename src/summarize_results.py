from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def load_metadata(molecules_dir: Path) -> dict[str, dict]:
    metadata: dict[str, dict] = {}
    for json_path in sorted(molecules_dir.glob("carbene*.json")):
        metadata[json_path.stem] = json.loads(json_path.read_text())
    return metadata


def summarize_run(molecule: str, run_dir: Path, metadata: dict) -> dict | None:
    summary_path = run_dir / "summary.json"
    excitations_path = run_dir / "excitations.csv"
    if not summary_path.exists():
        return None

    summary = json.loads(summary_path.read_text())
    lowest = {}
    brightest = {}
    if excitations_path.exists():
        excitations = pd.read_csv(excitations_path)
        if not excitations.empty:
            lowest = excitations.sort_values("energy_ev").iloc[0].to_dict()
            brightest = excitations.sort_values("oscillator_strength", ascending=False).iloc[0].to_dict()

    benchmark_e = metadata.get("benchmark_lowest_excitation_ev")
    benchmark_f = metadata.get("benchmark_lowest_excitation_fosc")
    lowest_e = lowest.get("energy_ev")
    lowest_f = lowest.get("oscillator_strength")

    return {
        "molecule": molecule,
        "run_name": run_dir.name,
        "backend": "pyscf",
        "paper_geometry_method": metadata.get("method_geometry"),
        "paper_tddft_method": metadata.get("method_tddft"),
        "charge": summary.get("charge"),
        "multiplicity": summary.get("multiplicity"),
        "actual_xc": summary.get("xc"),
        "actual_basis": summary.get("basis"),
        "triplet_energy": summary.get("energy_hartree"),
        "triplet_s2": summary.get("s2"),
        "tda_completed": summary.get("tda_completed"),
        "lowest_triplet_excitation_ev": lowest_e,
        "lowest_triplet_fosc": lowest_f,
        "brightest_triplet_excitation_ev": brightest.get("energy_ev"),
        "brightest_triplet_fosc": brightest.get("oscillator_strength"),
        "benchmark_lowest_excitation_ev": benchmark_e,
        "benchmark_lowest_excitation_fosc": benchmark_f,
        "delta_lowest_excitation_ev": (
            None if lowest_e is None or benchmark_e is None else lowest_e - benchmark_e
        ),
        "delta_lowest_fosc": (
            None if lowest_f is None or benchmark_f is None else lowest_f - benchmark_f
        ),
        "grid_level": summary.get("grid_level"),
        "density_fit": summary.get("density_fit"),
        "nroots": summary.get("nroots"),
        "notes": metadata.get("notes"),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Summarize completed molecule runs into a CSV table.")
    parser.add_argument("--molecules-dir", type=Path, required=True)
    parser.add_argument("--runs-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    metadata = load_metadata(args.molecules_dir)
    rows: list[dict] = []

    for molecule, meta in metadata.items():
        molecule_runs = args.runs_root / molecule
        if not molecule_runs.exists():
            continue
        for run_dir in sorted(path for path in molecule_runs.iterdir() if path.is_dir()):
            row = summarize_run(molecule, run_dir, meta)
            if row is not None:
                rows.append(row)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(args.output, index=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
