from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pyscf import dft, gto, tdscf
from pyscf.scf import chkfile as scf_chkfile

EV_PER_HARTREE = 27.211386245988
NM_EV_FACTOR = 1239.841984


@dataclass
class SCFResult:
    energy_hartree: float
    s2: float
    mf: dft.uks.UKS


def read_xyz(xyz_path: Path) -> list[tuple[str, tuple[float, float, float]]]:
    lines = [line.strip() for line in xyz_path.read_text().splitlines() if line.strip()]
    if len(lines) < 3:
        raise ValueError(f"XYZ file is too short: {xyz_path}")

    try:
        natoms = int(lines[0])
    except ValueError as exc:
        raise ValueError(f"First XYZ line must be an integer atom count: {xyz_path}") from exc

    atom_lines = lines[2:]
    if len(atom_lines) != natoms:
        raise ValueError(
            f"XYZ atom count mismatch for {xyz_path}: header says {natoms}, got {len(atom_lines)} lines"
        )

    atoms: list[tuple[str, tuple[float, float, float]]] = []
    for line in atom_lines:
        parts = line.split()
        if len(parts) != 4:
            raise ValueError(f"Malformed XYZ line in {xyz_path}: {line!r}")
        symbol = parts[0]
        coords = tuple(float(value) for value in parts[1:4])
        atoms.append((symbol, coords))
    return atoms


def build_molecule(
    xyz_path: Path,
    charge: int,
    spin: int,
    basis: str,
    verbose: int = 4,
) -> gto.Mole:
    atoms = read_xyz(xyz_path)
    mol = gto.M(
        atom=atoms,
        unit="Angstrom",
        charge=charge,
        spin=spin,
        basis=basis,
        verbose=verbose,
    )
    return mol


def run_triplet_uks(
    xyz_path: Path,
    charge: int,
    spin: int,
    xc: str,
    basis: str,
    chkfile_path: Path | None = None,
    density_fit: bool = False,
    grid_level: int = 3,
    conv_tol: float = 1e-9,
    max_cycle: int = 100,
    verbose: int = 4,
) -> SCFResult:
    mol = build_molecule(xyz_path=xyz_path, charge=charge, spin=spin, basis=basis, verbose=verbose)
    mf = dft.UKS(mol)
    if density_fit:
        mf = mf.density_fit()
    mf.xc = xc
    mf.grids.level = grid_level
    if chkfile_path is not None:
        mf.chkfile = str(chkfile_path)
    mf.conv_tol = conv_tol
    mf.max_cycle = max_cycle
    energy_hartree = mf.kernel()
    if not mf.converged:
        raise RuntimeError(f"UKS did not converge for {xyz_path}")
    s2, _ = mf.spin_square()
    return SCFResult(energy_hartree=energy_hartree, s2=s2, mf=mf)


def run_tda(scf_result: SCFResult, nroots: int) -> tdscf.uhf.TDA:
    tda = scf_result.mf.TDA()
    tda.nstates = nroots
    tda.kernel()
    return tda


def load_scf_result_from_chkfile(chkfile_path: Path, xc: str | None = None) -> SCFResult:
    mol = scf_chkfile.load_mol(str(chkfile_path))
    mf = dft.UKS(mol)
    mf.__dict__.update(scf_chkfile.load(str(chkfile_path), "scf"))
    mf.chkfile = str(chkfile_path)
    mf.converged = True
    if xc is not None:
        mf.xc = xc
    s2, _ = mf.spin_square()
    return SCFResult(energy_hartree=float(mf.e_tot), s2=s2, mf=mf)


def excitation_rows(tda: tdscf.uhf.TDA) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    osc_strengths = tda.oscillator_strength()
    for idx, energy_hartree in enumerate(tda.e):
        energy_ev = energy_hartree * EV_PER_HARTREE
        wavelength_nm = NM_EV_FACTOR / energy_ev if energy_ev > 0 else float("inf")
        rows.append(
            {
                "root": idx + 1,
                "energy_hartree": float(energy_hartree),
                "energy_ev": energy_ev,
                "wavelength_nm": wavelength_nm,
                "oscillator_strength": float(osc_strengths[idx]),
            }
        )
    return rows
