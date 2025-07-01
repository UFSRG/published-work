from pysimm import system, lmps, forcefield
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', required=True, help='Input Solute LAMMPS data File')
parser.add_argument('-o', '--output', required=True, help='Output LAMMPS data file')
parser.add_argument('-m', '--molsize', required=True, help='Number of atoms in solute')
parser.add_argument('-b', '--boxsize', default=100., help='Box length from center')
parser.add_argument('-c', '--counterion', default='ho_opt.lmps', help='Input Ion LAMMPS File')
parser.add_argument('-x', '--xions', default=100, help='Number of Counter ions')
parser.add_argument('-s', '--solvent', default='H2O_spce_flex.lmps', help='Input Solvent LAMMPS Data file')
parser.add_argument('-n', '--number', required=True, help='Number of solvents')
args = parser.parse_args()

fname_solute = args.input
fname_output = args.output
n_solute = int(args.molsize)
boxsize = args.boxsize
fname_ion = args.counterion
n_ion = int(args.xions)
fname_solvent = args.solvent
n_solvent = int(args.number)

s = system.read_lammps(fname_solute)
s.forcefield = 'gaff2'

s3 = system.read_lammps(fname_ion)
s3.ff_class = 2
s3.forcefield = 'gaff2'
s3.pair_style = 'lj'
s3.bond_style = 'harmonic'
s3.angle_style = 'harmonic'
s3.dihedral_style = 'fourier'
s4 = system.read_lammps(fname_solvent)

f_solute_xyz = 'solute_temp.xyz'
s_copy = s.copy()
s_copy.wrap()
s_copy.write_xyz(f_solute_xyz)

# f_lammps_template = 'lammps_template.lmps'
s_ = system.replicate([s3, s4], [n_ion, n_solvent], s_=s, density=None)
# s_.write_lammps(f_lammps_template)

f_ion_xyz = 'ion_temp.xyz'
s3.write_xyz(f_ion_xyz)

f_solvent_xyz = 'solvent_temp.xyz'
s4.write_xyz(f_solvent_xyz)

packmol_template = """
#
# A mixture of four different molecular fragments
#

# All the atoms from diferent molecules will be separated at least 2.0
# Anstroms at the solution.

tolerance 2.0

# The file type of input and output files is XYZ

filetype xyz

# The name of the output file

output OUTPUT_XYZ

# 100 mol1 and mol2 and 200 mol3 molecules will be put in a box
# defined by the minimum coordinates x, y and z = 0. 0. 0. and maximum
# coordinates 40. 40. 40. That is, they will be put in a cube of side
# 40. (the keyword "inside cube 0. 0. 0. 40.") could be used as well.

structure SOLUTE_XYZ 
  number 1
  # center
  fixed 0. 0. 0. 0. 0. 0.
end structure

structure ION_XYZ   
  number N_ION
  inside box -BOX_SIZE -BOX_SIZE -BOX_SIZE BOX_SIZE BOX_SIZE BOX_SIZE 
end structure

structure SOLVENT_XYZ 
  number N_SOLVENT
  inside box -BOX_SIZE -BOX_SIZE -BOX_SIZE BOX_SIZE BOX_SIZE BOX_SIZE
end structure

"""

f_packmol_xyz = 'packmol_temp.xyz'

packmol_inp = packmol_template.replace('OUTPUT_XYZ', f_packmol_xyz).replace('SOLUTE_XYZ', f_solute_xyz).replace('ION_XYZ', \
                  f_ion_xyz).replace('N_ION', str(n_ion)).replace('SOLVENT_XYZ', f_solvent_xyz).replace('N_SOLVENT', \
                  str(n_solvent)).replace('BOX_SIZE', boxsize)

f_temp = 'packmol_temp.inp'
with open(f_temp, 'w') as f:
    f.write(packmol_inp)

command = "packmol < packmol_temp.inp"

# Run the command
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

# Get the output and errors
output, error = process.communicate()

# Print the output and errors
print("Output:", output.decode())

# s = system.read_lammps(f_lammps_template)
sxyz = system.read_xyz(f_packmol_xyz)
count = 0
for ps, ps1 in zip(s_.particles, sxyz.particles):
    count += 1
    if count > n_solute:
        ps.x = ps1.x
        ps.y = ps1.y
        ps.z = ps1.z

s.write_lammps(fname_output)


