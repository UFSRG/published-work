# Grotthuss Contribution in Anion Exchange Membranes: Insight from Classical Molecular Dynamics Simulations

This repository hosts a **modified version of REACTER** for use with LAMMPS, developed as part of the study *"Grotthuss Contribution in Anion Exchange Membranes: Insight from Classical Molecular Dynamics Simulations"*.  
The modifications track **initiators before proton hopping** and improve output for post-processing, enabling clear separation of **vehicular** vs **Grotthuss** contributions to mean squared displacement (MSD).

---

## 📌 Overview

[REACTER](https://github.com/<original-reacter-repo-link>) is a LAMMPS extension that captures bond formation/breaking events during simulations via the `fix bond/react` mechanism.  
This fork modifies `fix_bond_react.cpp` to:

- Track **initiators** before each proton hopping event.
- Output **reaction coordinates** alongside initiators.
- Improve compatibility with parallel runs on newer LAMMPS versions (tested with 2025 release).
- Maintain full functionality for **single CPU** and **parallel** execution.

> **Note:** Parallel runs may not work reliably on older LAMMPS versions.  
> Our tests showed that upgrading to LAMMPS 2025 resolved previous parallelization issues.

---

## 🛠 Installation

1. **Install REACTER** following the official instructions here:  
   [REACTER Installation Guide](<link-to-installation-guide>)

2. **Replace `fix_bond_react.cpp`**  
   - Copy the modified `fix_bond_react.cpp` from this repository into your LAMMPS source directory, replacing the original file.

3. **Recompile LAMMPS**  
   ```bash
   make yes-MOLECULE
   make mpi   # or serial, depending on your setup
