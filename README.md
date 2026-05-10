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
