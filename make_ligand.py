import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-fmt", type=str, choices=["xyz", "lmp"], help="output format")
parser.add_argument("-addsol", action='store_true', help="whether to add solvent or not")
args = parser.parse_args()

data = np.genfromtxt('/home/pratima/Biased-SingleLigand/coords.txt', delimiter=' ')
hex_data = np.genfromtxt('/home/pratima/Biased-SingleLigand/solvent.txt', delimiter=' ')
bottom_data = np.genfromtxt('/home/pratima/Biased-SingleLigand/solv_bot.txt', delimiter=' ')
x0 = data[0,1]
y0 = data[0,2]
z0 = data[0,3]
nx = 9
nz = 6
n_surf = nx * nz * 16		# number of Cd, S atoms in 4 layers of 12x20 surface grids
xlo = -5.0
xhi =  31.0
ylo = -60.0
yhi =  60.0
zlo = -1.0
zhi =  37.5

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

sol_start = n_chain + n_surf
# shift hexane molecules up by 30 A in y-direction
centred_hex = np.zeros( (len(hex_data), 3) )
for i in range(len(hex_data)):
    centred_hex[i,0] = hex_data[i,1]
    centred_hex[i,1] = hex_data[i,2]
    centred_hex[i,2] = hex_data[i,3]
n_hex = len(centred_hex) / 6

bot_start = sol_start + n_hex * 6
# format bottom hexane molecules
bottom_hex = np.zeros( (len(bottom_data), 3) )
for i in range(len(bottom_data)):
    bottom_hex[i,0] = bottom_data[i,1]
    bottom_hex[i,1] = bottom_data[i,2]
    bottom_hex[i,2] = bottom_data[i,3]
n_bottom = len(bottom_hex) / 6

if (not(args.addsol)):
    n_hex = 0
    n_bottom = 0

# now specify chain coordinates
# VMD input file generation
if args.fmt == "xyz":
    print "{}".format(n_chain + n_surf + n_hex * 6 + n_bottom * 6)
    print "Comment Line"
    coords = np.copy(centred_data)
    coords[:,0] = coords[:,0] + 4.12 * 4
    coords[:,2] = coords[:,2] + 6.75 * 3
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

    if args.addsol:
        # top hexane molecules
        for i in range(n_hex * 6):
            if (i%6 == 0 or (i+1)%6 == 0):
                print "5	{:4.5f}	{:4.5f}	{:4.5f}".format( centred_hex[i,0], centred_hex[i,1], centred_hex[i,2] )
            else:
                print "6	{:4.5f}	{:4.5f}	{:4.5f}".format( centred_hex[i,0], centred_hex[i,1], centred_hex[i,2] )
    
        # bottom hexane molecules
        for i in range(n_bottom * 6):
            if (i%6 == 0 or (i+1)%6 == 0):
                print "5	{:4.5f}	{:4.5f}	{:4.5f}".format( bottom_hex[i,0], bottom_hex[i,1], bottom_hex[i,2] )
            else:
                print "6	{:4.5f}	{:4.5f}	{:4.5f}".format( bottom_hex[i,0], bottom_hex[i,1], bottom_hex[i,2] )

# LAMMPS input file generation
if args.fmt == "lmp":
    print "LAMMPS coordinates for single octadecyl chain on a CdS slab"
    print "{}	atoms".format( n_chain + n_surf + n_hex * 6 + n_bottom * 6 )
    print "{}	bonds".format( n_chain + n_hex * 5 + n_bottom * 5 )
    print "{}	angles".format( n_chain - 2 + n_hex * 4 + n_bottom * 4 )
    print "{}	dihedrals\n".format( n_chain - 3 + n_hex * 3 + n_bottom * 3 )

    print "6	atom types"
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
    print "4 32.065"
    print "5 15.034"
    print "6 14.027\n"

    # start printing atomic coordinates
    print "Atoms\n"
    natom = 1
    coords = np.copy(centred_data)
    coords[:,0] = coords[:,0] + 4.12 * 4
    coords[:,2] = coords[:,2] + 6.75 * 3
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

    if args.addsol:
        # top hexane molecules
        nmol = 3
        for i in range(n_hex * 6):
            if (i%6 == 0 or (i+1)%6 == 0):
                print "{}	{}	5	{:4.5f}	{:4.5f}	{:4.5f}".format( natom, nmol, centred_hex[i, 0], centred_hex[i, 1], centred_hex[i, 2] )
            else:
                print "{}	{}	6	{:4.5f}	{:4.5f}	{:4.5f}".format( natom, nmol, centred_hex[i, 0], centred_hex[i, 1], centred_hex[i, 2] )
            natom = natom + 1
            if ((i+1)%6 == 0):
                nmol = nmol + 1
    
        # bottom hexane molecules
        for i in range(n_bottom * 6):
            if (i%6 == 0 or (i+1)%6 == 0):
                print "{}	{}	5	{:4.5f}	{:4.5f}	{:4.5f}".format( natom, nmol, bottom_hex[i, 0], bottom_hex[i, 1], bottom_hex[i, 2] )
            else:
                print "{}	{}	6	{:4.5f}	{:4.5f}	{:4.5f}".format( natom, nmol, bottom_hex[i, 0], bottom_hex[i, 1], bottom_hex[i, 2] )
            natom = natom + 1
            if ((i+1)%6 == 0):
                nmol = nmol + 1

    # define atomic bonds for octadecyl and between ligand and corresponding Cd atom
    bound_index = 451
    print "\nBonds\n"
    nbond = 1
    for i in range(n_chain-1):
        print "{}	1	{}	{}".format( nbond, i + 1, i + 2 )
        nbond = nbond + 1
    print "{}	1	{}	{}".format( nbond, 1, bound_index )
    nbond = nbond + 1

    if args.addsol:
        for i in range(n_hex):
            for j in range(5):
                print "{}	1	{}	{}".format( nbond, sol_start + i * 6 + j, sol_start + i * 6 + j + 1 )
                nbond = nbond + 1
        for i in range(n_bottom):
            for j in range(5):
                print "{}	1	{}	{}".format( nbond, bot_start + i * 6 + j, bot_start + i * 6 + j + 1 )
                nbond = nbond + 1

    # define octadecyl angles
    print "\nAngles\n"
    nangle = 1
    for i in range(n_chain-2):
        print "{}	1	{}	{}	{}".format( nangle, i + 1, i + 2, i + 3 )
        nangle = nangle + 1

    if args.addsol:
        for i in range(n_hex):
            for j in range(4):
                print "{}	1	{}	{}	{}".format( nangle, sol_start + i * 6 + j, sol_start + i * 6 + j + 1, sol_start + i * 6 + j + 2 )
                nangle = nangle + 1
        for i in range(n_bottom):
            for j in range(4):
                print "{}	1	{}	{}	{}".format( nangle, bot_start + i * 6 + j, bot_start + i * 6 + j + 1, bot_start + i * 6 + j + 2 )
                nangle = nangle + 1

    # define octadecyl dihedrals
    print "\nDihedrals\n"
    ndihedral = 1
    for i in range(n_chain-3):
        print "{}	1	{}	{}	{}	{}".format( ndihedral, i + 1, i + 2, i + 3, i + 4 )
        ndihedral = ndihedral + 1

    if args.addsol:
        for i in range(n_hex):
            for j in range(3):
                print "{}	1	{}	{}	{}	{}".format( ndihedral, sol_start + i * 6 + j, sol_start + i * 6 + j + 1, sol_start + i * 6 + j + 2, sol_start + i * 6 + j + 3 )
                ndihedral = ndihedral + 1
        for i in range(n_bottom):
            for j in range(3):
                print "{}	1	{}	{}	{}	{}".format( ndihedral, bot_start + i * 6 + j, bot_start + i * 6 + j + 1, bot_start + i * 6 + j + 2, bot_start + i * 6 + j + 3 )
                ndihedral = ndihedral + 1







