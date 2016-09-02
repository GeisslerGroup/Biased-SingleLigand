import sys
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description="")
parser.add_argument("-bias", type=str, help="bias value to analyse")
parser.add_argument("-full", action='store_true', help="anaylse long unbiased trajectory?")
args = parser.parse_args()

if args.full:
    save = "hist_nobias.png"
else:
    save = "hist" + args.bias + ".png"

if args.full:
    data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/lig.long', delimiter=' ')
else:
    data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/lig.' + args.bias, delimiter=' ')

size = len(data)
x0 = 0.0
y0 = 0.0
z0 = 0.0
x1 = 0.0
y1 = 0.0
z1 = 0.0
if args.full:
    f = open("theta-long.txt","w")
else:
    f = open("theta" + args.bias + ".txt","w")

for i in range (0,size,18):
  if (i + 17 < size):
    x0 = data[i,1]
    y0 = data[i,2]
    z0 = data[i,3]
    x1 = data[i+9,1]
    y1 = data[i+9,2]
    z1 = data[i+9,3]
    x_vec = x1 - x0
    y_vec = y1 - y0
    z_vec = z1 - z0
    norm = np.sqrt(x_vec*x_vec + y_vec*y_vec + z_vec*z_vec)
    th = 180 * np.arccos(y_vec/norm)/np.pi
    f.write("%4.5f\n" %(th))

f.close()

if args.full:
    hist_data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/theta-long.txt', delimiter=' ')
else:
    hist_data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/theta' + args.bias + '.txt', delimiter=' ')
bins = np.linspace(0, 100, 100)
hist, bins = np.histogram(hist_data, bins = bins, density = True)
bin_centres = bins[1:] * 0.5 + bins[:-1] * 0.5
plt.figure()
plt.plot(bin_centres, hist)
# plt.show()
plt.savefig(save)

