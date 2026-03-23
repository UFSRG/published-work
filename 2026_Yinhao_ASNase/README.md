# Influence of PEGylation on enzyme structure, dynamics and substrate binding: case study on L-Asparaginase
This repository contains input files, scripts, and protein structures used in the simulations for the following publication:


*Influence of PEGylation on enzyme structure, dynamics and substrate binding: case study on L-Asparaginase*\
*DOI will be updated upon publication*

---

## 📂 Content


### Initial_structure_CMD
Initial structure used for 2µs conventional molecular dynamics (CMD)
- **6UOH_pH74_pqr.pdb**  
  Structure of ASNase monomer from pdb code 6UOH, the protonation state of residues is designated using pdb2pqr from APBS server
- **6UOH_pH74_pqr_Nter.pdb**  
  Structure of ASNase-PEG with 5kDa PEG attached at the N-terminus of the protein
- **6UOH_pH74_pqr_K29.pdb**  
  Structure of ASNase-PEG with 5kDa PEG attached at the ε-amino at the end of K29 of the protein
- **6UOH_pH74_pqr_K207.pdb**  
  Structure of ASNase-PEG with 5kDa PEG attached at the ε-amino at the end of K207 of the protein

### Initial_structure_FM
Initial structure used for FM, get from clustering analysis from 2µs CMD
- **ASNase_C0.pdb**  
  Representative structure of ASNase monomer from cluster 0
- **ASNase_Nter_C0.pdb**  
  Representative structure of ASNase-PEG with 5kDa PEG attached at the N-terminus of the protein from cluster 0
- **ASNase_K29_C0.pdb**  
  Representative structure of ASNase-PEG with 5kDa PEG attached at the ε-amino at the end of K29 of the protein from cluster 0
- **ASNase_K207_C0.pdb**  
  Representative structure of ASNase-PEG with 5kDa PEG attached at the ε-amino at the end of K207 of the protein from cluster 0

### mdp files
Following mdp files is included

- **em.mdp**
- **nvt1_310K.mdp**
- **npt1_310K.mdp**
- **npt_prod.mdp**  
- **npt_mtd.mdp**  
- **nvtq.mdp**

**Conventional MD (2 µs)**  
Non-PEGylated: `em → nvt1_310K → npt1_310K → npt_prod`  
PEGylated: `em → nvt1_310K → npt1_310K → nvtq → npt_prod`

**Funnel Metadynamics (FM)**  
Non-PEGylated: `em → nvt1_310K → npt1_310K → npt_mtd`  
PEGylated: `em → nvt1_310K → npt1_310K → nvtq → npt_mtd`


### FM
Files needed for FM
- **ASNase_ASN**
- **ASNase_Nter_ASN**
- **ASNase_K29_ASN**
- **ASNase_K207_ASN**

Within each folder, contains \_alignment.pdb file for structure alignment for RMSD calculation and definition of the funnel shaped potential, plumed_FM_\*.dat file input file for FM, and plumed_FM_*_reweight.dat file for reweighting and get 2D free energy profile.


### Post_analysis_script
**Original code is conceptualized, then partially realized and improved by Gemini.**
- **FM_data_processing.ipynb**  
  Analyze the results from FM, examine the convergence of the simulation and calculate the absolute binding free energy(python realization with idea from tcl script within FMAP)
- **BACF.py**  
  Calculate the Bond vector auto correlation function from different level (active site, shell within active site, whole protein)
- **PSF_Ca.py**  
  Calculate partial structure factor between different component of the system
