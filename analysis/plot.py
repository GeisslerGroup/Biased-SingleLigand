import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-temp", type=float, help="temperature of simulation")
parser.add_argument("-strength", type=float, help="spring constant used in simulation")
parser.add_argument("-lower", type=float, default=0.70, help="lowest bias value in simulation")
parser.add_argument("-upper", type=float, default=1.40, help="highest bias value in simulation")
parser.add_argument("-step", type=float, default=0.05, help="steps between bias values in simulation")
args = parser.parse_args()

temp = args.temp
kBT = 0.593 * temp / 298 
beta = 1 / (kBT)
# print beta * beta
strength = args.strength 

namelist = np.arange(args.lower, args.upper+args.step, args.step)

weights = np.genfromtxt('/home/pratima/Biased-SingleLigand/analysis/pot.txt',delimiter=',')
# log_weights = -np.log(weights) / beta

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

bins = np.linspace(0.0, 1.70, 100)
bin_centres = 0.5 * bins[1:] + 0.5 * bins[:-1]
N_sims = len(namelist)
nbins = len(bin_centres)
N_theta = np.zeros(nbins)
M_alpha = np.zeros(N_sims)
pot_list = []

# plt.figure(1)
# plt.plot(namelist*180/np.pi, log_weights)
# plt.show()

# get M_alpha and N_theta
count = 0
for i in namelist:
    data = np.genfromtxt("/home/pratima/Biased-SingleLigand/dump_files/theta{:1.2f}.txt".format(i), delimiter=' ')

    total_prob, bins = np.histogram(data, bins=bins)

    M_alpha[count] = len(data)
    count = count + 1
    for j in range(nbins):
        N_theta[j] = N_theta[j] + total_prob[j]
    bias_en = 0.5 * strength * (bin_centres - i) * (bin_centres - i) * beta
    pot_list.append(bias_en)

# unbiased distribution from long trajectory
long_data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/theta-long.txt', delimiter=' ')
long_hist, long_bins = np.histogram(long_data, bins = bins, density=True)
long_bins = bin_centres[long_hist != 0]
long_hist = long_hist[long_hist != 0]
log_long = -np.log(long_hist)
zero = min(log_long)
log_long = log_long - zero

# reconstruct probability distribution

prob_dist = np.zeros(nbins)
norm = 0.0
for i in range(nbins):
    denominator = 0.0
    for j in range(N_sims):
        denominator = denominator + M_alpha[j] * np.exp(-(pot_list[j][i] - beta * weights[j]))
    prob_dist[i] = N_theta[i] / denominator
    norm = norm + prob_dist[i]

norm2 = np.sum(prob_dist)
# print norm, norm2
prob_dist = prob_dist / norm
prob_bins = bin_centres[prob_dist != 0]
prob_dist = prob_dist[prob_dist != 0]
log_prob = -np.log(prob_dist)
zero = min(log_prob)
log_prob = log_prob - zero

# print prob_dist
plt.figure()
# plt.plot(bin_centres, prob_dist,color='red')
plt.plot(prob_bins, log_prob,color='blue', label='after WHAM unbiasing', linewidth=2)
plt.plot(long_bins, log_long, color='red', label='long simulation', linewidth=2)
plt.ylim(0,20)
plt.xlabel(r'$\theta$', fontsize=32)
plt.ylabel(r'$-\log{P(\theta)}$', fontsize=32)
# plt.legend(loc='upper center', fontsize=28)
plt.xticks(fontsize=28, fontweight='bold')
plt.yticks(fontsize=28, fontweight='bold')
plt.show()


