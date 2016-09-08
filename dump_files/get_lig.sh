#!/bin/bash --login

biaslist=$(seq 1.15 0.025 1.40)

for bias in ${biaslist}
do
	awk '/^2/ || /^1/' dump.340.${bias} > lig.${bias}
done
