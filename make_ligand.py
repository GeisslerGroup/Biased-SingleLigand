import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-fmt", type=str, choices=["xyz", "lmp"], help="output format")
args = parser.parse_args()

data = np.genfromtxt('/home/pratima/Biased-SingleLigand/coords.txt', delimiter=' ')
x0 = data[0,1]
y0 = data[0,2]
z0 = data[0,3]
nx = 20
nz = 12
n_surf = nx * nz * 16		# number of Cd, S atoms in 4 layers of 12x20 surface grids
xlo = -200.0
xhi =  200.0
ylo = -200.0
yhi =  200.0
zlo = -200.0
zhi =  200.0

# centre the octadecyl chain
centred_data = np.zeros( (len(data), 3) )
for i in range(len(data)):
    centred_data[i,0] = data[i,1] - x0
    centred_data[i,1] = data[i,2] - y0
    centred_data[i,2] = data[i,3] - z0
n_chain = len(centred_data)

rotate = np.array([ [np.cos(0.5 * np.pi), -np.sin(0.5 * np.pi), 0], [np.sin(0.5 * np.pi), np.cos(0.5 * np.pi), 0], [0, 0, 1.0] ])
for i in range(n_chain):
    centred_data[i,:] = rotate.dot(centred_data[i,:])

# now specify chain coordinates
# VMD input file generation
if args.fmt == "xyz":
    print "{}".format(n_chain + n_surf)
    print "Comment Line"
    coords = np.copy(centred_data)
    coords[:,0] = coords[:,0] + 4.12 * 6
    coords[:,2] = coords[:,2] + 6.75 * 4
    for i in range(n_chain):
        if (i == n_chain-1):
            print "1	{:4.5f}	{:4.5f}	{:4.5f}".format(coords[i,0], coords[i,1], coords[i,2])
        else:
            print "2	{:4.5f}	{:4.5f}	{:4.5f}".format(coords[i,0], coords[i,1], coords[i,2])

    # Cd-S surface coordinates
    for i in range(nx):
        for j in range(nz):
            coords = centred_data[0, :] - np.array([0.0, 1.56, 0.0])
            coords[0] = coords[0] + 4.12 * i 
            coords[2] = coords[2] + 6.75 * j 
            print "3    {:4.5f} {:4.5f} {:4.5f}".format( coords[0], coords[1], coords[2] )
            print "4    {:4.5f} {:4.5f} {:4.5f}".format( coords[0], coords[1], coords[2] + 2.5299 )
            print "3    {:4.5f} {:4.5f} {:4.5f}".format( coords[0] - 2.06073, coords[1] - 1.18977, coords[2] + 3.375 )
            print "4    {:4.5f} {:4.5f} {:4.5f}".format( coords[0] - 2.06073, coords[1] - 1.18977, coords[2] - 3.375 + 2.5299 )
            print "3    {:4.5f} {:4.5f} {:4.5f}".format( coords[0] - 2.06073, coords[1] - 3.5693, coords[2] )
            print "4    {:4.5f} {:4.5f} {:4.5f}".format( coords[0] - 2.06073, coords[1] - 3.5693, coords[2] + 2.5299 )
            print "3    {:4.5f} {:4.5f} {:4.5f}".format( coords[0], coords[1] - 3.5693 - 1.18977, coords[2] + 3.375 )
            print "4    {:4.5f} {:4.5f} {:4.5f}".format( coords[0], coords[1] - 3.5693 - 1.18977, coords[2] - 3.375 + 2.5299 )
    
            print "3    {:4.5f} {:4.5f} {:4.5f}".format( coords[0], coords[1] - 7.13848, coords[2] )
            print "4    {:4.5f} {:4.5f} {:4.5f}".format( coords[0], coords[1] - 7.13848, coords[2] + 2.5299 )
            print "3    {:4.5f} {:4.5f} {:4.5f}".format( coords[0] - 2.06073, coords[1] - 7.13848 - 1.18977, coords[2] + 3.375 )
            print "4    {:4.5f} {:4.5f} {:4.5f}".format( coords[0] - 2.06073, coords[1] - 7.13848 - 1.18977, coords[2] - 3.375 + 2.5299 )
            print "3    {:4.5f} {:4.5f} {:4.5f}".format( coords[0] - 2.06073, coords[1] - 7.13848 - 3.5693, coords[2] )
            print "4    {:4.5f} {:4.5f} {:4.5f}".format( coords[0] - 2.06073, coords[1] - 7.13848 - 3.5693, coords[2] + 2.5299 )
            print "3    {:4.5f} {:4.5f} {:4.5f}".format( coords[0], coords[1] - 7.13848 - 3.5693 - 1.18977, coords[2] + 3.375 )
            print "4    {:4.5f} {:4.5f} {:4.5f}".format( coords[0], coords[1] - 7.13848 - 3.5693 - 1.18977, coords[2] - 3.375 + 2.5299 )

# LAMMPS input file generation
if args.fmt == "lmp":
    print "LAMMPS coordinates for single octadecyl chain on a CdS slab"
    print "{}	atoms".format( n_chain + n_surf )
    print "{}	bonds".format( n_chain )
    print "{}	angles".format( n_chain - 2 )
    print "{}	dihedrals\n".format( n_chain - 3 )

    print "4	atom types"
    print "1	bond types"
    print "1	angle types"
    print "1	dihedral types\n"

    print "{} {}	xlo xhi".format(xlo, xhi)
    print "{} {}	ylo yhi".format(ylo, yhi)
    print "{} {}	zlo zhi\n".format(zlo, zhi)

    print "Masses\n"
    print "1 15.034"
    print "2 14.027"
    print "3 112.411"
    print "4 32.065\n"

    # start printing atomic coordinates
    print "Atoms\n"
    natom = 1
    coords = np.copy(centred_data)
    coords[:,0] = coords[:,0] + 4.12 * 6
    coords[:,2] = coords[:,2] + 6.75 * 4
    for i in range(n_chain):
        if (i == n_chain-1):
            print "{}	1	1	{:4.5f}	{:4.5f}	{:4.5f}".format( natom, coords[i, 0], coords[i, 1], coords[i, 2]  )
        else:
            print "{}	1	2	{:4.5f}	{:4.5f}	{:4.5f}".format( natom, coords[i, 0], coords[i, 1], coords[i, 2]  )
        natom = natom + 1
    for i in range(nx):
        for j in range(nz):
            coords = centred_data[0, :] - np.array([0.0, 1.56, 0.0])
            coords[0] = coords[0] + 4.12 * i
            coords[2] = coords[2] + 6.75 * j
            print "{}   2      3       {:4.5f} {:4.5f} {:4.5f}".format( natom, coords[0], coords[1], coords[2] )
            print "{}   2      4       {:4.5f} {:4.5f} {:4.5f}".format( natom + 1, coords[0], coords[1], coords[2] + 2.5299 )
            print "{}   2      3       {:4.5f} {:4.5f} {:4.5f}".format( natom + 2, coords[0] - 2.06073, coords[1] - 1.18977, coords[2] + 3.375 )
            print "{}   2      4       {:4.5f} {:4.5f} {:4.5f}".format( natom + 3, coords[0] - 2.06073, coords[1] - 1.18977, coords[2] - 3.375 + 2.5299 )
            print "{}   2      3       {:4.5f} {:4.5f} {:4.5f}".format( natom + 4, coords[0] - 2.06073, coords[1] - 3.5693, coords[2] )
            print "{}   2      4       {:4.5f} {:4.5f} {:4.5f}".format( natom + 5, coords[0] - 2.06073, coords[1] - 3.5693, coords[2] + 2.5299 )
            print "{}   2      3       {:4.5f} {:4.5f} {:4.5f}".format( natom + 6, coords[0], coords[1] - 3.5693 - 1.18977, coords[2] + 3.375 ) 
            print "{}   2      4       {:4.5f} {:4.5f} {:4.5f}".format( natom + 7, coords[0], coords[1] - 3.5693 - 1.18977, coords[2] - 3.375 + 2.5299 )

            print "{}   2      3       {:4.5f} {:4.5f} {:4.5f}".format( natom + 8, coords[0], coords[1] - 7.13848, coords[2] )
            print "{}   2      4       {:4.5f} {:4.5f} {:4.5f}".format( natom + 9, coords[0], coords[1] - 7.13848, coords[2] + 2.5299 )
            print "{}   2      3       {:4.5f} {:4.5f} {:4.5f}".format( natom + 10, coords[0] - 2.06073, coords[1] - 7.13848 - 1.18977, coords[2] + 3.375 ) 
            print "{}   2      4       {:4.5f} {:4.5f} {:4.5f}".format( natom + 11, coords[0] - 2.06073, coords[1] - 7.13848 - 1.18977, coords[2] - 3.375 + 2.5299 )
            print "{}   2      3       {:4.5f} {:4.5f} {:4.5f}".format( natom + 12, coords[0] - 2.06073, coords[1] - 7.13848 - 3.5693, coords[2] )
            print "{}   2      4       {:4.5f} {:4.5f} {:4.5f}".format( natom + 13, coords[0] - 2.06073, coords[1] - 7.13848 - 3.5693, coords[2] + 2.5299 )
            print "{}   2      3       {:4.5f} {:4.5f} {:4.5f}".format( natom + 14, coords[0], coords[1] - 7.13848 - 3.5693 - 1.18977, coords[2] + 3.375 ) 
            print "{}   2      4       {:4.5f} {:4.5f} {:4.5f}".format( natom + 15, coords[0], coords[1] - 7.13848 - 3.5693 - 1.18977, coords[2] - 3.375 + 2.5299 )
            natom = natom + 16

    # define atomic bonds for octadecyl and between ligand and corresponding Cd atom
    print "\nBonds\n"
    nbond = 1
    for i in range(n_chain-1):
        print "{}	1	{}	{}".format( nbond, i + 1, i + 2 )
        nbond = nbond + 1
    print "{}	1	{}	{}".format( nbond, 1, n_chain + 1 )

    # define octadecyl angles
    print "\nAngles\n"
    nangle = 1
    for i in range(n_chain-2):
        print "{}	1	{}	{}	{}".format( nangle, i + 1, i + 2, i + 3 )
        nangle = nangle + 1

    # define octadecyl dihedrals
    print "\nDihedrals\n"
    ndihedral = 1
    for i in range(n_chain-3):
        print "{}	1	{}	{}	{}	{}".format( ndihedral, i + 1, i + 2, i + 3, i + 4 )
        ndihedral = ndihedral + 1







