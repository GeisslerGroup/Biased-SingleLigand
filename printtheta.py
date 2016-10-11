import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description="")
parser.add_argument("-bias", type=float, default=2500.0, help="bias value for spring constant")
parser.add_argument("-lower", type=float, default=1.65, help="lower limit of order parameter in biased simulation")
parser.add_argument("-upper", type=float, default=1.10, help="upper limit of order parameter in biased simulation")
parser.add_argument("-step", type=float, default=-0.05, help="step between each consecutive umbrella")
parser.add_argument("-timestep", type=int, default=5000, help="timesteps after which umbrella is moved")
args   = parser.parse_args()

# at_range = np.arange(args.lower, args.upper+args.step, args.step)
steps = ((args.upper - args.lower) / args.step) + 1.0
steps = np.ceil(steps)
at_range = np.zeros(steps)
for i in np.arange(steps):
    at_range[i] = args.lower + args.step * i

str_out = ""

str_out = str_out + "UNITS ENERGY=kcal/mol\n"
str_out = str_out + "d1: DISTANCE ATOMS=1,9 COMPONENTS\n"

str_out = str_out + "\nMATHEVAL ...\n"
str_out = str_out + "LABEL=theta\nARG=d1.x,d1.y,d1.z\n"
str_out = str_out + "FUNC=atan(sqrt(x*x+z*z)/y)\n"
str_out = str_out + "PERIODIC={-pi,pi}\n"
str_out = str_out + "... MATHEVAL\n"

str_out = str_out + "\n\nMOVINGRESTRAINT ...\n"
str_out = str_out + "  ARG=theta\n"
for i in range(len(at_range)):
    str_out = str_out + "  STEP{}={} AT{}={} KAPPA{}={}\n".format(i, i*args.timestep, i, at_range[i], i, args.bias)
str_out = str_out + "... MOVINGRESTRAINT\n"

str_out = str_out + "\nPRINT ARG=theta STRIDE=10\n"

str_out = str_out.rstrip(",")
print str_out
