import numpy as np
import matplotlib.pyplot as plt

temp = 340.0
strength = 2500.0
weights = np.genfromtxt('/home/pratima/Biased-SingleLigand/analysis/pot.txt',delimiter=',')
log_weights = -temp * np.log(weights)

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

bins = np.linspace(0.70, 1.70, 200)
bin_centres = 0.5 * bins[1:] + 0.5 * bins[:-1]
namelist = np.arange(1.15, 1.405, 0.025)
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
    if (np.ceil(i*1000)%100 == 50):
        data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/theta' + str(i) + '0.txt', delimiter=' ')
    elif (np.ceil(i*1000)%100 == 0):
        data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/theta' + str(i) + '00.txt', delimiter=' ')
    else:
        data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/theta' + str(i) + '.txt', delimiter=' ')

    total_prob, bins = np.histogram(data, bins=bins)

    M_alpha[count] = len(data)
    count = count + 1
    for j in range(nbins):
        N_theta[j] = N_theta[j] + total_prob[j]
    bias_en = 0.5 * strength * (bin_centres - i) * (bin_centres - i)
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
        denominator = denominator + M_alpha[j] * np.exp(-(pot_list[j][i] - log_weights[j]) / temp)
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
plt.plot(prob_bins, log_prob,color='blue', label='after unbiasing')
plt.plot(long_bins, log_long, color='red', label='long simulation')
plt.xlabel(r'$\theta_z$', fontsize=20)
plt.ylabel(r'$\log{P(\theta_z)}$', fontsize=20)
plt.legend(loc='upper center')
plt.show()


