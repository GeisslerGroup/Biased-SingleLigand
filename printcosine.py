import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description="")
parser.add_argument("-bias", type=float, help="bias value for spring constant")
args   = parser.parse_args()

str_out = ""

str_out = str_out + "d1: DISTANCE ATOMS=1,9 COMPONENTS\n"

str_out = str_out + "\nMATHEVAL ...\n"
str_out = str_out + "LABEL=theta\nARG=d1.x,d1.y,d1.z"
str_out = str_out.rstrip(",")
str_out = str_out + "\nFUNC=atan(sqrt(x*x+z*z)/y)\n"
str_out = str_out + "PERIODIC={-pi,pi}\n"
str_out = str_out + "... MATHEVAL\n"

str_out = str_out + "\nRESTRAINT ARG=theta AT={} KAPPA=2500.0 LABEL=restraint\n\nPRINT ARG=theta STRIDE=10\n".format(args.bias)

str_out = str_out.rstrip(",")
print str_out
