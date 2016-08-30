import numpy as np
import matplotlib.pyplot as plt

k = 2.0
temp = 2.0
weights = np.genfromtxt('/home/pratima/UmbrellaSampling-Test/pot.txt',delimiter=',')
log_weights = -temp * np.log(weights)

# x = np.linspace(-22,22,len(weights))
# plt.figure()
# plt.plot(x, weights)
# plt.show()

bins = np.linspace(-20, 20, 400)
bin_centres = 0.5 * bins[1:] + 0.5 * bins[:-1]
namelist = np.arange(-20.0, 21.0, 1.0)
N_sims = len(namelist)
nbins = len(bin_centres)
N_theta = np.zeros(nbins)
M_alpha = np.zeros(N_sims)
pot_list = []

# get M_alpha and N_theta
count = 0
for i in namelist:
    data = np.genfromtxt('/home/pratima/UmbrellaSampling-Test/traj' + str(i) + '00000.txt',delimiter=' ')
    total_prob, bins = np.histogram(data[:,1], bins=bins)
    M_alpha[count] = len(data)
    count = count + 1
    for j in range(nbins):
        N_theta[j] = N_theta[j] + total_prob[j]
    bias_en = 0.5 * 20.0 * k * (bin_centres - i) * (bin_centres - i)
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

print k
print temp
a = 20.0
Z_alpha = np.zeros(N_sims)
P_theta = np.zeros(nbins)
for i in range(N_sims):
    Z_alpha[i] = -temp * np.log( ( 1.0/np.sqrt(1+a) ) * np.exp( -0.5 * k * (a/(1+a)) * namelist[i] * namelist[i] / temp ) )
print Z_alpha

for i in range(nbins):
    denominator = 0.0
    for j in range(N_sims):
        denominator = denominator + M_alpha[j] * np.exp(-(pot_list[j][i] - Z_alpha[j]) / temp)
    P_theta[i] = N_theta[i] / denominator

expected_P = np.exp(-0.5 * k * bin_centres * bin_centres / temp) / np.sqrt(2*np.pi*temp / k)
plt.figure(2)
plt.plot(bin_centres, P_theta, color='red')
# plt.plot(bin_centres, expected_P, color='blue')
plt.show()
