import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-w", action='store_true', help="add weights while shifting distributions")
parser.add_argument("-left_del", action='store_true', help="remove left endpoint of data")
args = parser.parse_args()

temp = 340.0
strength = 2500.0

namelist = np.arange(1.15, 1.405, 0.025)
# namelist = [-0.40]
N_sims = len(namelist)
bins = np.linspace(0.70, 1.70, 200)		# angles are between 60 and 90 degrees approximately
bins_OG = bins[1:] * 0.5 + bins[:-1] * 0.5 

color = iter(plt.cm.copper(np.linspace(0,1,N_sims)))
plt.figure(0)
en_list = []
prob_list = []
bin_list = []
err_list = []
pot_list = []

# get probability distributions and unbias them
for i in namelist:
    c = next(color)
    if (np.ceil(i*1000)%100 == 50):
        data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/theta' + str(i) + '0.txt', delimiter=' ')
    elif (np.ceil(i*1000)%100 == 0):
        data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/theta' + str(i) + '00.txt', delimiter=' ')
    else:
        data = np.genfromtxt('/home/pratima/Biased-SingleLigand/dump_files/theta' + str(i) + '.txt', delimiter=' ')
    total_prob, bins = np.histogram(data, bins=bins)

    bin_centres = 0.5 * bins[1:] + 0.5 * bins[:-1]
    norm = np.sum(total_prob) * 1.0
    total_prob = total_prob / norm
    err_prob = np.std(total_prob, ddof=1)
    bin_centres = bin_centres[total_prob!=0]
    total_prob = total_prob[total_prob!=0]

    free_en = -temp * np.log(total_prob)
    bias_en = 0.5 * strength * (bin_centres - i) * (bin_centres - i)
    free_en = free_en - bias_en
    err_en = temp * err_prob / total_prob
    prob_list.append(total_prob)
    en_list.append(free_en)
    bin_list.append(bin_centres)
    pot_list.append(bias_en)
    err_list.append(err_en)

    plt.plot(bin_centres, free_en, color=c)
#     plt.plot(bin_centres, total_prob, color=c)
#     plt.errorbar(bin_centres, free_en, err_en, color=c)

plt.show()

if args.left_del:
    print en_list[0]
    new_bins = [] 
    for row in bin_list:
        test = np.array([row[i] for i in range(1, len(row))])
        new_bins.append(test)
    new_en = [] 
    for row in en_list:
        test = np.array([row[i] for i in range(1, len(row))])
        new_en.append(test)
    new_err = [] 
    for row in err_list:
        test = np.array([row[i] for i in range(1, len(row))])
        new_err.append(test)
    bin_list = new_bins
    en_list = new_en
    err_list = new_en
    print en_list[0]

# shift distributions to get free energy
for i in range(1, len(bin_list)):
    mask_minus =  np.array([ x1 in bin_list[i] for x1 in bin_list[i-1] ])
    mask_plus  =  np.array([ x1 in bin_list[i-1] for x1 in bin_list[i] ])
    en_plus = en_list[i][mask_plus]
    en_minus = en_list[i-1][mask_minus]
    prob_plus = prob_list[i][mask_plus]
    prob_minus = prob_list[i-1][mask_minus]
    err_plus = err_list[i][mask_plus]
    err_minus = err_list[i-1][mask_minus]
#     print en_plus.shape
#     print en_minus.shape

    if args.w:
        weight = 1 / ( err_plus * err_plus + err_minus * err_minus )
        shift = np.mean( (en_plus - en_minus) * weight ) / np.mean(weight)
    else:
        shift = np.mean(en_plus - en_minus)
    en_list[i] = en_list[i] - shift

# en_list = np.array(en_list)
zero = min( [ min(arr) for arr in en_list ] )

log_prob = []
for row in prob_list:
    log_prob.append(-np.log(row))
zero_prob = min( [ min(arr) for arr in log_prob ] )

plt.figure(1)
for i in range(len(bin_list)):
#     plt.plot(bin_list[i], en_list[i] - zero, color='red')
    plt.plot(bin_list[i], log_prob[i] - zero_prob, color='red')
plt.show()



