# Electron Sextets Triplet Carbenes

Reproduction workflow for the TDDFT/TDA screening layer from the paper
*Electron Sextets as Optically Addressable Molecular Qubits: Triplet Carbenes*.

## Initial Scope

- Reproduce triplet-geometry and triplet-reference TDA results, starting with Carbene 3.
- Keep the workflow PySCF-first and backend-modular so ORCA can be added later.
- Store inputs, run artifacts, and CSV summaries in a consistent layout for later screening work.

## Repository Layout

- `docs/superpowers/specs/`: design notes for setup and implementation planning.
- `molecules/`: source structures for paper systems and future candidates.
- `src/`: command-line workflow entry points.
- `backends/`: backend-specific calculation adapters.
- `templates/`: backend input templates.
- `runs/`: per-molecule calculation outputs.
- `results/`: summary CSV outputs.
- `notebooks/`: exploratory reproduction notebooks.

## Current Status

This repository currently contains the approved bootstrap design and the minimal
project scaffold. Workflow implementation starts with a Carbene 3 PySCF/TDA
prototype in the next phase.

## Current Workflow

Create the local environment:

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
```

Run the paper-closer Carbene 3 reference path:

```bash
.venv/bin/python src/run_triplet_tda.py \
  --xyz molecules/carbene3.xyz \
  --charge 0 \
  --multiplicity 3 \
  --basis def2-svpd \
  --xc b3lyp \
  --nroots 1 \
  --density-fit \
  --grid-level 1 \
  --chkfile runs/carbene3/tda_triplet_df_grid1_1root/scf.chk \
  --output-dir runs/carbene3/tda_triplet_df_grid1_1root
```

Run the faster screening-mode Carbene 3 path:

```bash
.venv/bin/python src/run_triplet_tda.py \
  --xyz molecules/carbene3.xyz \
  --charge 0 \
  --multiplicity 3 \
  --basis def2-svp \
  --xc b3lyp \
  --nroots 1 \
  --density-fit \
  --grid-level 1 \
  --chkfile runs/carbene3/tda_triplet_screen_svp_1root/scf.chk \
  --output-dir runs/carbene3/tda_triplet_screen_svp_1root
```

Summarize completed or partial runs:

```bash
.venv/bin/python src/summarize_results.py \
  --molecules-dir molecules \
  --runs-root runs \
  --output results/paper3_reproduction_summary.csv
```
