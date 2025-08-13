# Grotthuss Contribution in Anion Exchange Membranes: Insight from Classical Molecular Dynamics Simulations

This repository contains a **modified version of REACTER** to use with LAMMPS, developed as part of the study *"Grotthuss Contribution in Anion Exchange Membranes: Insight from Classical Molecular Dynamics Simulations"*.  
The REACTER modifications track **initiators before proton hopping** and improve output for post-processing, enabling clear separation of **vehicular** vs **Grotthuss** contributions to mean squared displacement (MSD).

---

## 📌 Overview

[REACTER](https://www.reacter.org/) is a LAMMPS extension that captures bond formation/breaking events during simulations via the `fix bond/react` mechanism.  
Here we modify `fix_bond_react.cpp` to:

- Track **initiators** before each proton hopping event.
- Output **reaction coordinates** alongside initiators.
- Improve compatibility with parallel runs on newer LAMMPS versions (tested with 2025 release).

> **Note:** Parallel runs may not work reliably on older LAMMPS versions.  
> Upgrading to LAMMPS 2025 resolved previous parallelization issues.

---

## 🛠 Installation (LAMMPS + Modified REACTER)

These instructions describe how to install the modified REACTER with a fresh LAMMPS build.  
They are written for a typical HPC environment but can be adapted for local machines.

---

### 1. Clone LAMMPS

```bash
git clone https://github.com/lammps/lammps.git
cd lammps
```

---

### 2. Add the Modified REACTER Files

- Navigate to the `src` directory inside the LAMMPS source.
- Replace `fix_bond_react.cpp`  with the modified versions from this repository. The file is located in src inside a REACTION folder.
- Ensure the modified files are saved in the correct location before building.

---

### 3. Prepare a Clean Build

```bash
rm -rf build
mkdir build
cd build
```

---

### 4. (HPC Users) Load Required Modules

If you are on a cluster like HPG, you may need to load updated compilers and MPI before building:

```bash
module purge
module load gcc/12.2.0 openmpi/5.0.7 cmake python
```

---

### 5. Configure with CMake

Enable required LAMMPS packages, including REACTION and other dependencies:

```bash
cmake ../cmake \
  -DPKG_REACTION=yes \
  -DPKG_EXTRA-DUMP=yes \
  -DPKG_MOLECULE=yes \
  -DPKG_EXTRA-MOLECULE=yes \
  -DPKG_KSPACE=yes \
  -DPKG_MISC=yes \
  -DPKG_GPU=yes \
  -DPKG_USER-MISC=yes \
  -DPKG_RIGID=yes \
  -DPKG_CLASS2=yes \
  -DBUILD_MPI=yes \
  -DBUILD_SHARED_LIBS=no \
  -DCMAKE_INSTALL_PREFIX=../install
```

---

### 6. Compile

```bash
make -j 8
```

*(Optional)* Install to the specified directory:

```bash
make install
```

---

### 7. Test Installation

Verify the build:

```bash
./lmp -h
```

If the help output lists `fix bond/react` and the packages above, REACTER is successfully installed.

---

**Note on Parallel Runs:**  
For parallel execution with REACTER, use **LAMMPS 2025 or later** to avoid MPI-related issues present in older versions.

---


## 📊 Post-Processing

### Grotthuss MSD Decomposition Script (with dot-product cross-correlation)

Given a LAMMPS trajectory (`.lammpstrj`) and a proton-hopping log (`out`/SLURM log),  
this script tracks hydroxide identities across proton hops (including multiple hops within a single saved interval), and computes mean squared displacement (MSD) decomposed into **vehicular** and **Grotthuss** components, plus their cross-correlation computed as an average dot product of the *running* vehicular and Grotthuss displacement vectors.

**Outputs**
- CSV with columns: `Time`, `Total MSD`, `Vehicular MSD`, `Grotthuss MSD`, `Cross_correlation`
- Optional: PNG plot (single y-axis)

**Usage**
```bash
python MSD_decouple.py \
  --traj AEM.lammpstrj \
  --out slurm_out \
  --hydroxide-type 3 \
  --csv msd.csv \
  --plot msd_plot.png \
  --verbose
```

---
---

## 📄 Citation

If you use this modified REACTER in your research, please cite:

> *Grotthuss Contribution in Anion Exchange Membranes: Insight from Classical Molecular Dynamics Simulations*  
> [Mohammed Al Otmi, Ping Lin , Amalakrishna Vemula, William Schertzer, Sean Wood, Jacob Gissinger, Coray Colina, Rampi Ramprasad, Ryan Lively, Janani Sampat; 2025, Journal/DOI – to be added upon publication]

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome. Please open an issue or submit a pull request.

---

