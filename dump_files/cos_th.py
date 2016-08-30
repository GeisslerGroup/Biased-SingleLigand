import sys
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description="")
parser.add_argument("-bias", type=str, help="bias value to analyse")
args = parser.parse_args()

data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/lig.' + args.bias, delimiter=' ')
size = len(data)
x0 = 0.0
y0 = 0.0
z0 = 0.0
x1 = 0.0
y1 = 0.0
z1 = 0.0
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
