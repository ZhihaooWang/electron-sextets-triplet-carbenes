# Carbene 3 Priority 1 Implementation Plan

Date: 2026-05-11

## Scope

Implement the smallest runnable slice from the task specification:

1. read a molecule from XYZ;
2. run a triplet UKS single-point calculation;
3. run TDA from that triplet reference;
4. write excitation energies and oscillator strengths to CSV.

This plan intentionally stops before geometry optimization and broken-symmetry
singlet work. Those come after the single-point TDA path is stable.

## Execution Steps

### Step 1: Environment and Project Wiring

- Add a `pyproject.toml` with the minimal runtime dependencies for the PySCF
  path.
- Keep the codebase lightweight and script-first.
- Use a local `.venv` so package installation does not affect the system
  interpreter.

### Step 2: Input and Metadata Layer

- Add a simple XYZ reader that preserves atom order and coordinates.
- Store Carbene 3 metadata in a machine-readable file alongside the structure.
- Record charge, multiplicity, geometry method target, TDDFT/TDA target, and
  paper reference.

### Step 3: PySCF Backend

- Implement a PySCF backend that can:
  - build an unrestricted triplet molecule;
  - run UKS with explicit functional and basis settings;
  - expose total energy and `<S^2>`;
  - run TDA for a configurable number of roots.

### Step 4: Output Layer

- Write a per-run `summary.json` with the run settings and key SCF results.
- Write `excitations.csv` with at least:
  - root index;
  - excitation energy in Hartree and eV;
  - wavelength in nm;
  - oscillator strength.

### Step 5: First Scientific Run

- Source an initial Carbene 3 structure from the paper SI when possible.
- Run the first Carbene 3 triplet UKS + TDA single point with:
  - charge `0`;
  - multiplicity `3`;
  - functional `b3lyp`;
  - basis `def2-svpd`;
  - TDA roots `10`.

### Step 6: Validation

- Confirm the triplet SCF converges and `<S^2>` is close to `2.0`.
- Compare the lowest relevant triplet excitation and oscillator strength to the
  task target of about `2.44 eV` and `0.015`.
- If the result is far off, check the structure source first before escalating
  to method changes.

## Risks

- PySCF is not installed yet in this environment.
- The paper SI structure coordinates are not yet present in the repository.
- The exact bright-state root may depend strongly on the starting geometry.

## Success Criteria for This Slice

- A single command can run Carbene 3 triplet UKS + TDA from an XYZ file.
- The run produces machine-readable outputs in `runs/carbene3/tda_triplet/`.
- The result is comparable to the paper target even if it is not yet fully
  optimized.
