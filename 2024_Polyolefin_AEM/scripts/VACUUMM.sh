#!/bin/bash
#SBATCH --job-name=VAC
#SBATCH --mail-type=ALL
#SBATCH --ntasks=32
#SBATCH --ntasks-per-socket=8
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=700mb
#SBATCH --time=24:00:00
#SBATCH --partition=hpg2-compute
#SBATCH --account=jsampath

module purge

#remove any solvents if available
#ml gcc/12.2.0 openmpi/4.1.5
#mpirun -n 1 /apps/gcc/12.2.0/openmpi/4.1.5/lammps/23Jun22el8/bin/lmp -echo screen -in remove_solvent.in

module purge

#first process datafile to generate pair.dat and Corrected_atoms.gfg
module load python/3.8
python3 process.py
python3 segment.py
echo "processing complete"

module purge
PPATH=$(pwd)
##second loading vacuumms, needs installation if the first time
cd ~/spack
. share/spack/setup-env.sh
spack load vacuumms/x2ct5f2
echo " VACUUMMS is loaded"

cd $PPATH
pwd

#substitution
file_path="after_21step.lmps"
# Read the 14th, 15th, and 16th lines from the file
line_14=$(sed -n '14p' "$file_path")
line_15=$(sed -n '15p' "$file_path")
line_16=$(sed -n '16p' "$file_path")

# Extract the second value from each line
value_14=$(echo "$line_14" | awk '{print $2}')
value_15=$(echo "$line_15" | awk '{print $2}')
value_16=$(echo "$line_16" | awk '{print $2}')

# Calculate the difference between the second and first values
Lx=$(echo "$value_14 - ${line_14%% *}" | bc)
Ly=$(echo "$value_15 - ${line_15%% *}" | bc)
Lz=$(echo "$value_16 - ${line_16%% *}" | bc)

# Output the differences
echo "Lx $Lx"
echo "Ly $Ly"
echo "Lz $Lz"

cram -box $Lx $Ly $Lz < Corrected2.gfg > system.gfg
echo " substitution completed"

pddx \
     -seed 56878 \
     -n_samples 500000 \
     -n_threads 32 \
     -box $Lx $Ly $Lz \
     < system.gfg \
     >> system_0.5M.cav
echo "cesa run completed, now remove overlapping spheres"

uniq \
     -box $Lx $Ly $Lz \
     < system_1M.cav \
     > system.unq
echo " duplicates are removed, 4th columns represent the diameters of the spheres"

echo "VACUMMS completed"

