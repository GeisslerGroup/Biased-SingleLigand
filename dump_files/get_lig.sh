#!/bin/bash --login

biaslist=$(seq -80 5 -50)

for bias in ${biaslist}
do
	awk '/^2/ || /^1/' dump.340.${bias} > lig.${bias}
done
