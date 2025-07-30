# Exploring the temperature stability of CRISPR–Cas12b using Molecular Dynamics Simulations
This repository contains input files, scripts, and protein structures used in the simulations for the following publication:

*Exploring the temperature stability of CRISPR–Cas12b using Molecular Dynamics Simulations*

---

## Content

### Protein Structure
- **BrCas12b.pdb**  
  Alphafold predicted structure of BrCas12b
- **BrCas12b_RFND.pdb**  
  Alphafold predicted structure of BrCas12b with R160E/F208W/N524V/D868V mutation  

### mdp files
- **em.mdp**
- **nvt1.mdp**
- **nvt2.mdp**
- **npt.mdp**
- **nvtf_300K.mdp/nvtf_400K.mdp**  
  em -> nvt1 -> nvt2 -> npt -> nvtf_300K/nvtf_400K

### Post analysis script
- **Corss_correlation_score.ipynb**  
  Build cross-correlation matrix from GROMACS PCA output
  Build correlation matrix between different protein domains
