import numpy as np
import matplotlib.pyplot as plt
import argparse

temp = 340.0

namelist = np.arange(-0.80, -0.25, 0.05)
# namelist = [-0.40]
N_sims = len(namelist)
bins = np.linspace(-0.85, -0.2, 200)
bins_OG = bins[1:] * 0.5 + bins[:-1] * 0.5 
N_theta = np.zeros(len(bins_OG))
M_alpha = np.zeros(N_sims)

color = iter(plt.cm.copper(np.linspace(0,1,N_sims)))

pot_list = []
count = 0
# populate M_alpha and N_theta
for i in namelist:
    c = next(color)
    data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/theta' + str(i) + '.txt', delimiter=' ')
    total_prob, bins = np.histogram(data[:,1], bins=bins)
    bin_centres = 0.5 * bins[1:] + 0.5 * bins[:-1]

#     M_alpha[count] = np.sum(total_prob)
    M_alpha[count] = len(data)
    count = count + 1
    for j in range(len(bin_centres)):
        N_theta[j] = N_theta[j] + total_prob[j]

    bias_en = 0.5 * 5000.0 * (bin_centres - i) * (bin_centres - i)
    pot_list.append(bias_en)

tol = 1.0e-6
en_diff = 1.0
en_list = np.ones(N_sims)
count = 1
pot_list = np.array(pot_list)
# print pot_list.shape
# print pot_list[0]
# print N_theta
# print M_alpha
# exit(0)

while (en_diff > tol):
    en_diff = 0.0
    old_en = np.copy(en_list)
    denominator = np.zeros(len(N_theta))

    # calculate denominator
    for i in range(len(N_theta)):
        for j in range(N_sims):
#             denominator[i] = denominator[i] + M_alpha[j] * np.exp((-pot_list[j][i] - old_en[j]) / temp)
            denominator[i] = denominator[i] + (M_alpha[j] * np.exp((-pot_list[j][i]) / temp) / old_en[j])
        if (denominator[i] == 0.0):
            denominator[i] = 1.0e-6

    # now update free energies
    for i in range(N_sims):
        term = 0.0
        numerator = 0.0
        for l in range(len(N_theta)):
            numerator = N_theta[l] * np.exp(-pot_list[i][l] / temp)
            term = term + (numerator / denominator[l])
#         term = np.sum(numerator / denominator)
#         en_list[i] = -temp * np.log(term)
        en_list[i] = term

    difference = np.zeros(N_sims)
    for i in range(len(old_en)):
#         difference[i] = np.abs(en_list[i] - old_en[i])
        difference[i] = np.abs(en_list[i] / old_en[i])
        en_diff = en_diff + difference[i]
    print count
#     print "numerator", numerator
#     print "denominator", denominator
    print en_list
    print en_diff
    count = count + 1

print en_list




