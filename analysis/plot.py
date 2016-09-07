import numpy as np
import matplotlib.pyplot as plt

temp = 340.0
strength = 2500.0
weights = np.genfromtxt('/home/pratima/Biased-SingleLigand/analysis/pot.txt',delimiter=',')
log_weights = -temp * np.log(weights)

bins = np.linspace(60.0, 90.0, 200)
bin_centres = 0.5 * bins[1:] + 0.5 * bins[:-1]
namelist = np.arange(1.10, 1.45, 0.05)
N_sims = len(namelist)
nbins = len(bin_centres)
N_theta = np.zeros(nbins)
M_alpha = np.zeros(N_sims)
pot_list = []

# get M_alpha and N_theta
count = 0
for i in namelist:
    if (int(i*100)%10 == 0):
        data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/theta' + str(i) + '0.txt', delimiter=' ')
    else:
        data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/theta' + str(i) + '.txt', delimiter=' ')
    total_prob, bins = np.histogram(data, bins=bins)

    M_alpha[count] = len(data)
    count = count + 1
    for j in range(nbins):
        N_theta[j] = N_theta[j] + total_prob[j]
    bias_en = 0.5 * strength * (bin_centres - i) * (bin_centres - i)
    pot_list.append(bias_en)

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
print norm, norm2
prob_dist = prob_dist / norm
# print prob_dist
plt.figure()
# plt.plot(bin_centres, prob_dist,color='red')
plt.plot(bin_centres, -temp*np.log(prob_dist),color='blue')
plt.show()

