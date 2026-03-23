### V2
import numpy as np
import MDAnalysis as mda
from mdcraft.analysis.structure import StructureFactor

def generate_wavevectors_short(
    box_dimensions,
    q_max=0.5,
    num_q_magnitudes=15,
    points_per_shell=20
):
    """
    Generates a concise list of 3D wavevectors (q_x, q_y, q_z) with a focus on small, log-spaced q-magnitudes.

    Args:
        box_dimensions (list or np.array): The three dimensions of the simulation box [Lx, Ly, Lz] in Angstroms.
        q_max (float): Maximum q magnitude to generate (in Angstrom^-1).
        num_q_magnitudes (int): Number of distinct q-magnitude shells.
        points_per_shell (int): Number of q-vectors to distribute on each shell.

    Returns:
        numpy.ndarray: An array of shape (N, 3) containing the wavevectors.
    """
    box_dimensions = np.asarray(box_dimensions)
    if len(box_dimensions) != 3:
        raise ValueError("box_dimensions must have length 3.")

    # Smallest non-zero q related to the largest box dimension
    q_min_theoretical = 2 * np.pi / np.max(box_dimensions)

    if q_min_theoretical >= q_max:
        raise ValueError(
            f"q_min_theoretical ({q_min_theoretical:.4f} Å⁻¹) >= q_max ({q_max:.4f} Å⁻¹). "
            "Increase q_max or check box_dimensions."
        )

    q_magnitudes = np.logspace(
        np.log10(q_min_theoretical), np.log10(q_max), num_q_magnitudes
    )

    wavevectors_list = []
    # Use a simple way to get somewhat distributed points on a sphere for brevity
    # For more uniform distributions, Fibonacci sphere or other methods are better
    # but make the function longer. This uses random points on a unit sphere.
    for q_mag in q_magnitudes:
        if q_mag < 1e-9:  # Avoid q=0
            continue
        for _ in range(points_per_shell):
            # Generate random points on a sphere
            vec = np.random.randn(3)
            vec = vec / np.linalg.norm(vec) * q_mag
            wavevectors_list.append(vec)

    if not wavevectors_list:
        return np.empty((0,3))

    unique_wavevectors = np.unique(np.asarray(wavevectors_list), axis=0)
    # Filter out any potential q=0 vector again if it crept in due to randomness near zero
    unique_wavevectors = unique_wavevectors[np.linalg.norm(unique_wavevectors, axis=1) > 1e-9]

    return unique_wavevectors

# Define Parameters 
# ───── User parameters ─────────────────────────────────────────────────────────
topology = "ASNase_K29_NPT.pdb"  # e.g. .pdb, .gro, .prmtop
trajectory = "npt_prod_2µs_fit10ps_t.xtc"  # e.g. .xtc, .dcd, .trr
save_npz_file_path = 'ASNase_K29_1_2µs_psf.npz' # Save path
# ───────────────────────────────────────────────────────────────────────────────
# 1. Load the system
u = mda.Universe(topology, trajectory)

# 2. change back the residue names for those not standard
resnames = u.residues.resnames.copy()
mask = np.isin(resnames, ["PEGE", "EPEG"])
resnames[mask] = "PEGM"
mask = np.isin(resnames, ["ASPP"])
resnames[mask] = "ASP"
mask = np.isin(resnames, ["LYK"])
resnames[mask] = "LYS"
mask = np.isin(resnames, ["LLEU"])
resnames[mask] = "LEU"
u.add_TopologyAttr("resnames", resnames)
# 3. define groups for psf calculation 
group_protein = u.select_atoms("protein and name CA") # use protein Cα atoms
group_polymer = u.select_atoms("resname PEGM and (name C1 or name C2)") # use PEG C atoms
####### alternatively use all the atoms within protein and polymer #######
# group_protein = u.select_atoms("protein")
# group_polymer = u.select_atoms("resname PEGM")
# 4. generate wavevectors for structure factor calculation (fine tune the grid)
my_box = u.dimensions[:3] # Angstroms from MDAnalysis
wavevectors = generate_wavevectors_short(
    box_dimensions=my_box,
    q_max=4,                 # Max q for "large scale"
    num_q_magnitudes=600,    # Number of q-shells
    points_per_shell=400     # Number of q-vectors per shell
)
print(f"Generated {wavevectors.shape[0]} wavevectors.")
if wavevectors.size > 0:
    wavenumbers = np.linalg.norm(wavevectors, axis=1)
print(f"Min/Max generated q-magnitudes: {np.min(wavenumbers):.4f} / {np.max(wavenumbers):.4f} Å⁻¹")
# 5. define the callable function to run for partial structure factor calculation
psf_Pp_def = StructureFactor(groups=(group_protein, group_polymer),grouping="residues", mode="partial",form="exp", wavevectors=wavevectors, parallel=True,verbose=False)
psf_Pp = psf_Pp_def.run(start=0, stop=20000, step=1)
# 6. Store the calculated Partial Structure Factor in dict.
cal_PSF = {}
cal_PSF['wavevectors'] = wavevectors
cal_PSF['wavenumbers'] = psf_Pp.results.wavenumbers
cal_PSF['PP_psf'] = psf_Pp.results.ssf[0]
cal_PSF['Pp_psf'] = psf_Pp.results.ssf[1]
cal_PSF['pp_psf'] = psf_Pp.results.ssf[2]
# 7. Save the PSF and npz object
try:
    # Use keyword arguments (**data_to_save) to map dict keys to array names
    np.savez_compressed(save_npz_file_path, **cal_PSF)
    print(f"\nData successfully saved to {save_npz_file_path} using np.savez_compressed.")
except IOError as e:
    print(f"Error saving file with np.savez_compressed: {e}")
