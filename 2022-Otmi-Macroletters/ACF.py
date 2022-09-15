#!/usr/bin/env python
#    Bond vector autocorrelation 
#    Author : Janani Sampath
#.   Edited by: Mohammed Al Otmi
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.


#Importing modules after converting into python3. Variables( their values are assigned after)
import sys
import numpy as np
import math
import pandas as pd


frames = 482

def read_header(f): #comments correspond to dump file headings
	f.readline() # ITEM: TIMESTEP
	timestep = int(f.readline())

	f.readline() # ITEM: NUMBER OF ATOMS
	num_atoms = int(f.readline())

	f.readline() # ITEM: BOX BOUNDS xx yy zz
	line = f.readline()
	line = line.split()
	xlo = float(line[0])
	xhi = float(line[1])
	line = f.readline()
	line = line.split()
	ylo = float(line[0])
	yhi = float(line[1])
	line = f.readline()
	line = line.split()
	zlo = float(line[0])
	zhi = float(line[1])

	return timestep, num_atoms, xlo, xhi, ylo, yhi, zlo, zhi



# In[7]:


#initialize system

fname = 'noH2_prod.lammpstrj'
f = open(fname, 'r')
file = 'bacf_nH2_all_PMP.csv'

# read in the initial header
frame = 0
init_timestep, num_atoms, xlo, xhi, ylo, yhi, zlo, zhi = read_header(f)

# it is not possible to preallocate arrays (or to know number of frames in advance)
num_frames = float('inf')
alloc = 1
inf_frames = True

timestep = np.zeros(alloc,int) # 1D array of timesteps
box_bounds = np.zeros([alloc,3,2],float) # 3D array to store boundaries of the box, indexed by frame, x/y/z, then lower/upper
print(timestep)
print(box_bounds)
print(frame)
timestep[frame] = init_timestep
box_bounds[frame][0][0] = xlo
box_bounds[frame][0][1] = xhi
box_bounds[frame][1][0] = ylo
box_bounds[frame][1][1] = yhi
box_bounds[frame][2][0] = zlo
box_bounds[frame][2][1] = zhi

# NOTE: using num_atoms+1 here so that the arrays are indexed by their LAMMPS atom id
r = np.zeros([alloc, num_atoms+1, 3],float) # 3D array of x, y, z coordinates, r[frame][id][coordinate]
ir = np.zeros([alloc, num_atoms+1, 3],int) # 3D array of x, y, z image flags, r[frame][id][coordinate]

id2mol = np.zeros(num_atoms+1,int) # array to map from atom id to molecule id, builds this from the first frame, if available
id2type = np.zeros(num_atoms+1,int) # array to map from atom id to type, builds this from the first frame, if available


# In[8]:



# separately do the first ATOMS section so that we can initialize things, build the id2mol and id2type arrays, and so that the main loop starts with reading in the header
line = f.readline()
line = line.split()
id_index = line.index("id") - 2   #position of id-2
if "mol" in line:
	mol_index = line.index("mol") - 2
else:
	mol_index = None
if "type" in line:
	type_index = line.index("type") - 2
else:
	type_index = None
if "x" in line:
	scaled = False
	x_index = line.index("x") - 2
	y_index = line.index("y") - 2
	z_index = line.index("z") - 2
elif "xs" in line:
	scaled = True
	x_index = line.index("xs") - 2
	y_index = line.index("ys") - 2
	z_index = line.index("zs") - 2
if "ix" in line:
	ix_index = line.index("ix") - 2
	iy_index = line.index("iy") - 2
	iz_index = line.index("iz") - 2


# In[9]:



# loop over the atoms lines
for atom in range(num_atoms):
	line = f.readline()
	line = line.split()
	# get the atom id
	my_id = int(line[id_index])
	# x, y, z coordinates
	r[frame][my_id][0] = float(line[x_index])
	r[frame][my_id][1] = float(line[y_index])
	r[frame][my_id][2] = float(line[z_index])

	# unscale, if necessary
	if scaled:
		r[frame][my_id][0] = r[frame][my_id][0]*(box_bounds[frame][0][1]-box_bounds[frame][0][0]) + box_bounds[frame][0][0]
		r[frame][my_id][1] = r[frame][my_id][1]*(box_bounds[frame][1][1]-box_bounds[frame][1][0]) + box_bounds[frame][1][0]
		r[frame][my_id][2] = r[frame][my_id][2]*(box_bounds[frame][2][1]-box_bounds[frame][2][0]) + box_bounds[frame][2][0]

	# x, y, z image flags
	ir[frame][my_id][0] = int(line[ix_index])
	ir[frame][my_id][1] = int(line[iy_index])
	ir[frame][my_id][2] = int(line[iz_index])

	# if available, build the i2mol and id2type arrays
	if mol_index is not None:
		id2mol[my_id] = int(line[mol_index])
	if type_index is not None:
		id2type[my_id] = int(line[type_index])


# In[10]:



# build the reverse of the id2mol array
# this is a 2D array with rows of (potentially) varying length, so nest a numpy array into a python list
if mol_index is not None:
	num_mols = id2mol.max()	
	mol2ids = [[]]
	for molid in range(1, num_mols+1):
		mol2ids.append(np.where(id2mol==molid)[0]) ## mol2ids :[[1,2,3,4...*nmonomers{atom id}],...*npoly {mol id}]
else:
	num_mols = None
	mol2ids = None

# loop over number of num_frames frames, if num_frames is infinite, will look over all the frames in the file
frame = 1
while frame < num_frames:
	#print frame
	# try to read in a new header
	try:
		my_timestep, my_num_atoms, my_xlo, my_xhi, my_ylo, my_yhi, my_zlo, my_zhi = read_header(f)
	except:
        #print >> sys.stderr, "WARNING: hit end of file when reading in", fname, "at frame", frame
        	break

	# if we don't know how many frames to read in, have to allocate more memeory for the arrays
	if inf_frames:
		timestep = np.append(timestep, 0)
		box_bounds = np.concatenate( ( box_bounds, np.zeros([1,3,2], float) ) )
		r = np.concatenate( ( r, np.zeros([1, num_atoms+1, 3], float) ) )
		ir = np.concatenate( ( ir, np.zeros([1, num_atoms+1, 3], float) ) )
		
	# update the timestep and box size arrays
	timestep[frame] = my_timestep
	box_bounds[frame][0][0] = my_xlo
	box_bounds[frame][0][1] = my_xhi
	box_bounds[frame][1][0] = my_ylo
	box_bounds[frame][1][1] = my_yhi
	box_bounds[frame][2][0] = my_zlo
	box_bounds[frame][2][1] = my_zhi

	f.readline() # ITEM: ATOMS
	# loop over the atoms lines
	for atom in range(num_atoms):
		line = f.readline()
		line = line.split()

		# get the atom id
		my_id = int(line[id_index])
	
		# x, y, z coordinates
		r[frame][my_id][0] = float(line[x_index])
		r[frame][my_id][1] = float(line[y_index])
		r[frame][my_id][2] = float(line[z_index])

		# unscale, if necessary
		if scaled:
			r[frame][my_id][0] = r[frame][my_id][0]*(box_bounds[frame][0][1]-box_bounds[frame][0][0]) + box_bounds[frame][0][0]
			r[frame][my_id][1] = r[frame][my_id][1]*(box_bounds[frame][1][1]-box_bounds[frame][1][0]) + box_bounds[frame][1][0]
			r[frame][my_id][2] = r[frame][my_id][2]*(box_bounds[frame][2][1]-box_bounds[frame][2][0]) + box_bounds[frame][2][0]

		# x, y, z image flags
		ir[frame][my_id][0] = int(line[ix_index])
		ir[frame][my_id][1] = int(line[iy_index])
		ir[frame][my_id][2] = int(line[iz_index])
	
	frame += 1



# In[11]:



if len(mol2ids[0]) == 0:
	del mol2ids[0]
navg = 1  
##Make a list of bonds from .lmps file#
df = pd.read_csv('noH2_1M_equil.lmps')

#lines between word bonds and angles in datafile.......................
line1 = df.index[df['LAMMPS data file via write_data'].str.contains("Bonds")][0]
line2 = df.index[df['LAMMPS data file via write_data'].str.contains("Angles")][0]
df=df.iloc[line1:line2]
df.drop(index=line1,inplace=True)
ndf=df.drop(df.columns[1:3],axis=1)   
bondlist=[]                #bondlist only contains a specific type
for i in ndf['LAMMPS data file via write_data']:
    test_list=i.split()
    test_list = [int(i) for i in test_list]
    bondlist.append(test_list)       #for all 
    
# ............Filter by type............cp:3=CH, 15 or 17=cp-cp, 27 c-c
#     if test_list[1]==15:
#         bondlist.append(test_list)

## Now calculate bonds at different times
# bond = np.zeros([frames,(len(bondlist)+1),3],float)          

bacf_autocorr = np.zeros([navg,frames],float)
bacf_autocorr_final = np.zeros([frames],float)

# #Over all frames and all bonds. We can define a if condition based on the type..................... 
results = np.zeros([frames, len(bondlist)+1 ,3])
for t in range(frames):
    for i, bond in enumerate(bondlist):
#       get the coordinates of the two atoms and subtract them
        Bbond = r[t][bond[2]]-r[t][bond[3]]
        
#       Normalize the difference and store it in results
        results[t][i] = (Bbond/(np.sqrt(np.dot(Bbond,Bbond))))

        
for t in range(0,navg):
    t1 = 21*t
    for t2 in range(t1,int((frames/navg)+t1)):
        dt = t2 - t1
        for b in range(len(bondlist)):
            bacf_autocorr[t][dt] += np.dot(results[t1][b], results[t2][b])

for avg in range(0,navg):
    for dt in range(int(frames/navg)):
        bacf_autocorr_final[dt] += bacf_autocorr[avg][dt]/navg

# Write output to file
OUT = open(file, 'w')
OUT.write("timesteps,BACF\n")
for t in range(int(frames/navg)):
    OUT.write("%7i, %7f\n" % ((timestep[t]), ((bacf_autocorr_final[t])/len(bondlist)))) ###
OUT.close()
