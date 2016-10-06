import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-w", action='store_true', help="add weights while shifting distributions")
parser.add_argument("-left_del", action='store_true', help="remove left endpoint of data")
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
# namelist = np.arange(1.20, 1.40, 0.05)
# namelist = [-0.40]
N_sims = len(namelist)
bins = np.linspace(0.0, 1.70, 100)		# angles are between 60 and 90 degrees approximately
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
#     if ("{:1.2f}".format(i) == "1.15"):
# 	continue
    string ="/home/pratima/Biased-SingleLigand/dump_files/theta{:1.2f}.txt".format(i)
    print string , i  
    data = np.genfromtxt("/home/pratima/Biased-SingleLigand/dump_files/theta{:1.2f}.txt".format(i), delimiter=' ')
    total_prob, bins = np.histogram(data, bins=bins)

    bin_centres = 0.5 * bins[1:] + 0.5 * bins[:-1]
    err_prob = np.sqrt(total_prob)
    norm = np.sum(total_prob) * 1.0
    total_prob = total_prob / norm
    err_prob = err_prob / norm
    bin_centres = bin_centres[total_prob!=0]
    err_prob = err_prob[total_prob != 0]
    total_prob = total_prob[total_prob!=0]

    free_en = np.log(total_prob)
#     plt.plot(bin_centres, free_en)
    bias_en = 0.5 * strength * (bin_centres - i) * (bin_centres - i) * beta 
#     plt.plot(bin_centres, -bias_en)
    free_en = free_en + bias_en
    err_en = err_prob / total_prob
    prob_list.append(total_prob)
    en_list.append(free_en)
    bin_list.append(bin_centres)
    pot_list.append(bias_en)
    err_list.append(err_en)

    plt.plot(bin_centres, free_en, color=c)
#     plt.plot(bin_centres, total_prob)
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
zero = max( [ max(arr) for arr in en_list ] )

log_prob = []
for row in prob_list:
    log_prob.append(-np.log(row))
zero_prob = min( [ min(arr) for arr in log_prob ] )

plt.figure(1)
for i in range(len(bin_list)):
    plt.plot(bin_list[i], -en_list[i] + zero)
#     plt.plot(bin_list[i], -en_list[i])
#     plt.plot(bin_list[i], np.exp(-beta * (en_list[i] - zero)), color='red')
plt.show()



