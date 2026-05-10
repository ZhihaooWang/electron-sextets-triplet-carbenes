# Electron Sextets Triplet Carbenes Bootstrap Design

Date: 2026-05-11

## Goal

Create the initial private GitHub repository and local project scaffold for a
PySCF-first reproduction workflow targeting the TDDFT/TDA layer from the paper
*Electron Sextets as Optically Addressable Molecular Qubits: Triplet Carbenes*.

This setup covers repository bootstrap only. It does not yet implement the
calculation workflow.

## Context

The task specification calls for:

- a modular repository that can start with PySCF and later add ORCA or other backends;
- a workflow centered on triplet geometry optimization, triplet-reference TDA,
  optional broken-symmetry singlet analysis, and CSV-based result extraction;
- a first scientific target of Carbene 3 before expanding to Carbenes 2 and 1.

The current workspace initially contained only the paper task specification and
no existing git repository for this project.

## Selected Approach

Recommended approach selected by the user:

1. Create a private GitHub repository first.
2. Use the repository name `electron-sextets-triplet-carbenes`.
3. Bootstrap a minimal local scaffold that matches the task specification.
4. Keep the first tracked state intentionally thin: design doc, README,
   `.gitignore`, and empty top-level directories for the workflow.

## Repository Decisions

### Repository Name and Visibility

- GitHub repository name: `electron-sextets-triplet-carbenes`
- Visibility: private

### Local Root

- Local path: `/mnt/c/Users/wang/reproduce/electron-sextets-triplet-carbenes`

### Initial Branch

- Use `main` as the default working branch after initialization.

## Minimal Initial Scaffold

The repository starts with these directories:

```text
docs/superpowers/specs/
molecules/
molecules/candidates/
src/
backends/
templates/
runs/
results/
notebooks/
```

This structure mirrors the task specification closely enough to avoid early
layout churn while still keeping the first commit small.

## Included in the First Commit

The first commit should contain:

- this approved design document;
- a concise `README.md` describing scope and layout;
- a `.gitignore` suitable for Python work, notebooks, and generated run files;
- placeholder files needed to keep the empty scaffold directories tracked.

The first commit should not contain:

- PySCF workflow code;
- molecule coordinates copied without verification;
- backend templates that have not yet been validated;
- result CSVs or notebook content.

## GitHub and Git Setup

The repository should be created through `gh` using the authenticated account
already configured on this machine. The local repository should then add the
GitHub remote as `origin` and push the initial `main` branch.

If git identity is not already configured globally, set a repository-local
identity so the bootstrap commit can be made without mutating unrelated user
configuration.

## Immediate Next Step After Bootstrap

After the repository bootstrap is complete, the next planning stage should
focus on the smallest executable slice from the task specification:

1. read XYZ input;
2. run a triplet UKS single point;
3. run TDA from that reference;
4. extract excitation energies and oscillator strengths for Carbene 3.

## Self-Review

- No placeholders remain.
- The document is scoped to repository bootstrap only.
- The branch, repo name, visibility, and local root are explicit.
- The scaffold matches the task specification without overcommitting to
  unvalidated implementation details.
