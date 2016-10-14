import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-lower", type=float, default=0.70, help="lowest bias value in simulation")
parser.add_argument("-upper", type=float, default=1.40, help="highest bias value in simulation")
parser.add_argument("-step", type=float, default=0.05, help="steps between bias values in simulation")
args = parser.parse_args()

namelist = np.arange(args.lower, args.upper+args.step, args.step)

bins = np.linspace(0.0, 1.70, 100)
bins_OG = bins[1:] * 0.5 + bins[:-1] * 0.5

N_sims = len(namelist)
color = iter(plt.cm.copper(np.linspace(0,1,N_sims)))
plt.figure(0)

for i in namelist:
    c = next(color)
    string ="/home/pratima/Biased-SingleLigand/dump_files/theta{:1.2f}.txt".format(i)
    data = np.genfromtxt("/home/pratima/Biased-SingleLigand/dump_files/theta{:1.2f}.txt".format(i), delimiter=' ')

    total_prob, bins = np.histogram(data, bins=bins, density=True)
    theta = i 
    plt.plot(bins_OG, -np.log(total_prob), color=c, label="centred at theta = %3.2f" %theta, linewidth=2)
# plt.legend(loc='best')
plt.xlabel('theta', fontsize=30)
plt.ylabel('-log P', fontsize=30)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.xlim(0.0,1.6)
plt.show()

