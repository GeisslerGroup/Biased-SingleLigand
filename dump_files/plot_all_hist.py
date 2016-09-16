import numpy as np
import matplotlib.pyplot as plt

namelist = np.arange(1.15,1.405,0.025)
bins = np.linspace(0.70, 1.70, 100)
bins_OG = bins[1:] * 0.5 + bins[:-1] * 0.5

N_sims = len(namelist)
color = iter(plt.cm.copper(np.linspace(0,1,N_sims)))
plt.figure(0)

for i in namelist:
    c = next(color)
    if (np.ceil(i*1000)%100 == 50):
        data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/theta' + str(i) + '0.txt', delimiter=' ')
    elif (np.ceil(i*1000)%100 == 0): 
        data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/theta' + str(i) + '00.txt', delimiter=' ')
    else:
        data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/theta' + str(i) + '.txt', delimiter=' ')
    total_prob, bins = np.histogram(data, bins=bins, density=True)

    theta = i 
    plt.plot(bins_OG, total_prob, color=c, label="centred at theta = %3.1f" %theta)
plt.legend(loc='upper left')
plt.show()

