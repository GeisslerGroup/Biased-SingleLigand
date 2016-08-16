import numpy as np
import matplotlib.pyplot as plt
import argparse

data = np.genfromtxt('/home/pratima/Biased-SingleLigand/coords.txt', delimiter=' ')


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

