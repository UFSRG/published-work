# Structure, Dynamics and Hydrogen Transport in Amorphous Polymers

This repository contains input files, scripts, and equilibrated polymer structures used in the simulations for the following publication:

**Title:**  
*Structure, Dynamics and Hydrogen Transport in Amorphous Polymers: An Analysis of the Interplay Between Free Volume Element Distribution and Local Segmental Dynamics from Molecular Dynamics Simulations*

**Journal:**  
[Macromolecules](https://pubs.acs.org/doi/10.1021/acs.macromol.3c01508)

---

## 📂 Contents

### Simulation Input Scripts

- **21step.in**  
  LAMMPS script for the 21-step equilibration protocol.

- **Tg.in**  
  LAMMPS input file for calculating the glass transition temperature (Tg).

- **prod.in**  
  LAMMPS input file for the production run in either NVT or NPT ensembles.

---

### Post-Processing and Analysis Scripts

- **Tg.ipynb**  
  Python Jupyter Notebook for calculating Tg from the output of `Tg.in`.

- **ACF.py**  
  Python script to compute the bond vector autocorrelation function.

- **msd.py**  
  Python script to calculate the mean squared displacement (MSD).

---

### Equilibrated Polymer Structures

- **PMP.lmps**  
  Equilibrated structure for polymethylpentene (PMP).

- **PS.lmps**  
  Equilibrated structure for polystyrene (PS).

- **TRP.lmps**  
  Equilibrated structure for HAB-6FDA TR (TRP).

---

## 📑 Citation

If you use these files or scripts, please cite:

> Mohammed Al Otmi, et al., *Macromolecules*, 2024, [https://pubs.acs.org/doi/10.1021/acs.macromol.3c01508](https://pubs.acs.org/doi/10.1021/acs.macromol.3c01508)

---

