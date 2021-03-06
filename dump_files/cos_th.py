import sys
import numpy as np
import matplotlib.pyplot as plt
import argparse

temp = 340.0

parser = argparse.ArgumentParser(description="")
parser.add_argument("-bias", type=str, help="bias value to analyse")
parser.add_argument("-full", action='store_true', help="anaylse long unbiased trajectory?")
parser.add_argument("-save", action='store_true', help="save plot?")
parser.add_argument("-log", action='store_true', help="plot log of probability")
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

if args.full:
    start = 200 * 18
else:
    start = 2000 * 18

data_spaced = data[200*18::9, :]

for i in range (start,size,18):
  if (i + 17 < size):
    x0 = data[i,1]
    y0 = data[i,2]
    z0 = data[i,3]
    x1 = data[i+8,1]
    y1 = data[i+8,2]
    z1 = data[i+8,3]
    x_vec = x1 - x0
    y_vec = y1 - y0
    z_vec = z1 - z0
    norm = np.sqrt(x_vec*x_vec + y_vec*y_vec + z_vec*z_vec)
#     th = 180 * np.arccos(y_vec/norm)/np.pi
    th = np.arctan( np.sqrt(x_vec*x_vec + z_vec*z_vec) / y_vec )
    f.write("%4.5f\n" %(th))

f.close()

if args.full:
    hist_data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/theta-long.txt', delimiter=' ')
else:
    hist_data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/theta' + args.bias + '.txt', delimiter=' ')

print np.mean(hist_data)
print np.std(hist_data)
bins = np.linspace(-1.70, 1.70, 100)
hist, bins = np.histogram(hist_data, bins = bins, density = True)
bin_centres = bins[1:] * 0.5 + bins[:-1] * 0.5
plt.figure()
if args.log:
    bin_centres = bin_centres[hist != 0]
    hist = hist[hist != 0]
    plt.plot(bin_centres, -np.log(hist))
else:
    plt.plot(bin_centres, hist)
if args.save:
    plt.savefig(save)
else:
    plt.show()

