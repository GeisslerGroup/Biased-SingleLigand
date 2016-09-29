import numpy as np
import matplotlib.pyplot as plt
import argparse

temp = 340.0
kBT = 0.6731
beta = 1/(kBT)
strength = 2500.0
# strength = 100.0

# namelist = np.arange(1.15, 1.405, 0.025)
namelist = np.arange(0.70, 1.45, 0.05)
# namelist = [-0.40]
N_sims = len(namelist)
bins = np.linspace(0.40, 1.70, 200)		# angles are between 60 and 90 degrees approximately
bins_OG = bins[1:] * 0.5 + bins[:-1] * 0.5 
N_theta = np.zeros(len(bins_OG))
M_alpha = np.zeros(N_sims)

color = iter(plt.cm.copper(np.linspace(0,1,N_sims)))

# pot_list = []
# populate M_alpha and N_theta
for count, i in enumerate(namelist):
    c = next(color)
    # decide whether to use ceil or int based on which one works (keeps changing :/)
#     if (np.ceil(i*1000)%100 == 0):
    if (int(i*1000)%100 == 0):
        data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/theta' + str(i) + '0.txt', delimiter=' ')
#     elif (np.ceil(i*1000)%100 == 0):
#         data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/theta' + str(i) + '00.txt', delimiter=' ')
    else:
        data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/theta' + str(i) + '.txt', delimiter=' ')

    total_prob, bins = np.histogram(data, bins=bins)
    bin_centres = 0.5 * bins[1:] + 0.5 * bins[:-1]

#     M_alpha[count] = np.sum(total_prob)
    M_alpha[count] = len(data)
    for j in range(len(bin_centres)):
        N_theta[j] = N_theta[j] + total_prob[j]

#     bias_en = 0.5 * strength * (bins_OG - i) * (bins_OG - i) * beta
#     plt.plot(bin_centres, bias_en)
#     pot_list.append(bias_en)

plt.show()

tol = 1.0e-6
en_diff = 1.0
en_list = np.ones(N_sims)
# pot_list = np.exp(-np.array(pot_list))
# print pot_list.shape
# print pot_list[0]
# print N_theta
# print M_alpha
# exit(0)
pot_list = np.zeros((N_sims, len(bins_OG)))
# print pot_list.shape
for count, i in enumerate(namelist):
#     pot_list[count] = np.exp(-beta * 0.5 * strength * (bins_OG - i) * (bins_OG - i))
    pot_list[count] = 0.5 * strength * (bins_OG - i) * (bins_OG - i)
# print pot_list[0]
# exit(0)

while (en_diff > tol):
    en_diff = 0.0
    old_en = np.zeros(len(en_list))
    old_en[:] = en_list[:]
    denominator = np.zeros(len(N_theta))

    # calculate denominator
    for t_i in range(len(N_theta)):
#     	denominator[t_i] = np.sum(M_alpha * (pot_list[:,t_i] / old_en))
#         free_en = np.exp(beta * old_en)
#         if (np.sum(free_en) != np.sum(free_en)):
#             print "SHIT"
#             exit(0)
    	denominator[t_i] = np.sum( M_alpha * np.exp(-beta * (pot_list[:,t_i] - old_en)) )

    # now update free energies
    for s_i in range(N_sims):
#         en_list[s_i] =  np.sum(N_theta * (pot_list[s_i,:] / denominator))
        en_list[s_i] =  -kBT * np.log( np.sum(N_theta * (np.exp(-beta * pot_list[s_i,:]) / denominator)) )

    difference = np.abs(en_list - old_en)
    en_diff = np.sum(difference)

    print count
#     print "numerator", numerator
#     print "denominator", denominator
    print en_list
    print en_diff
    count = count + 1

print en_list




