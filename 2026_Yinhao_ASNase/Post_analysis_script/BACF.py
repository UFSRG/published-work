# Load Packages
import MDAnalysis as mda
import numpy as np
from MDAnalysis.lib import distances

# ───── User parameters ─────────────────────────────────────────────────────────
topology = "ASNase_npt.pdb"       # e.g. .pdb, .gro, .prmtop
trajectory = "npt_prod_whole_2µs_fit10ps.xtc"    # e.g. .xtc, .dcd, .trr
save_npz_file_path = 'ASNase_rt1_2µs_8A.npz'  # save the acf results for future plot
active_site_residues = [12, 25, 89, 90, 162]  # active site residues - m-csa
distance_cutoff = 8.0  # Ångström cutoff for shell region
# ───────────────────────────────────────────────────────────────────────────────
# 1. Load the system
u = mda.Universe(topology, trajectory)
# copy out the per‑atom resnames
resnames = u.residues.resnames.copy()

# wherever we had HIE or HIP, rename to HIS
mask = np.isin(resnames, ["ASPP"])
resnames[mask] = "ASP"
mask = np.isin(resnames, ["LYK"])
resnames[mask] = "LYS"

# overwrite the Universe's resnames attribute
u.add_TopologyAttr("resnames", resnames)
ca = u.select_atoms("protein and name CA")
ca_resids = ca.resids  # array of all CA residue IDs in order

# 1) Active‑site pairs: for each active residue, pair it with its neighbor(s)
resid_to_idx = {resid: idx for idx, resid in enumerate(ca_resids)}
pairs1 = []
for r in active_site_residues:
    if r in resid_to_idx:
        i = resid_to_idx[r]
        # forward bond (r -> r+1)
        if r+1 in resid_to_idx:
            pairs1.append((i, resid_to_idx[r+1]))
        # backward bond (r-1 -> r)
        if r-1 in resid_to_idx:
            pairs1.append((resid_to_idx[r-1], i))
pairs1 = list(set(pairs1))  # dedupe

# 2) Shell region: CA within cutoff of any active‐site CA, then adjacent‐only if both in shell
active_ca = ca.select_atoms("resid " + " ".join(map(str, active_site_residues)))
dmat = distances.distance_array(ca.positions, active_ca.positions)
shell_mask = (dmat <= distance_cutoff).any(axis=1)
shell_resids = np.array(ca_resids)[shell_mask]
pairs2 = []
for r in shell_resids:
    if (r+1 in shell_resids):
        pairs2.append((resid_to_idx[r], resid_to_idx[r+1]))
pairs2 = list(set(pairs2))

# 3) Whole protein: every adjacent CA–CA bond
pairs3 = [(i, i+1) for i in range(len(ca_resids)-1)]

# Define Dict. for each level
regions = {
    "active_site": pairs1,
    "shell":      pairs2,
    "whole":      pairs3
}

# Compute VACF for each region
n_frames = len(u.trajectory)
vacf_results = {}
for name, pairs in regions.items():
    if not pairs:
        print(f"Warning: no bonds found in region '{name}', skipping.")
        vacf_results[name] = np.zeros(n_frames//2)
        continue

    # Collect normalized vectors [frames × bonds × 3]
    vecs = np.zeros((n_frames, len(pairs), 3))
    for t, ts in enumerate(u.trajectory):
        pos = ca.positions
        for bi, (i, j) in enumerate(pairs):
            v = pos[j] - pos[i]
            vecs[t, bi] = v / np.linalg.norm(v)

    # Autocorrelation up to half the trajectory length
    max_lag = n_frames // 2
    acf = np.zeros(max_lag)
    for lag in range(max_lag):
        dots = (vecs[:n_frames-lag] * vecs[lag:]).sum(axis=2)
        acf[lag] = dots.mean()
    vacf_results[name] = acf

try:
    # Use keyword arguments (**data_to_save) to map dict keys to array names
    np.savez_compressed(save_npz_file_path, **vacf_results)
    print(f"\nData successfully saved to {save_npz_file_path} using np.savez_compressed.")

except IOError as e:
    print(f"Error saving file with np.savez_compressed: {e}")
