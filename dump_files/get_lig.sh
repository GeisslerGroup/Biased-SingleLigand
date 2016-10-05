#!/bin/bash --login

biaslist=$(seq 0.30 0.05 0.70)

for bias in ${biaslist}
do
	awk '/^2/ || /^1/' dump.340.${bias} > lig.${bias}
done
