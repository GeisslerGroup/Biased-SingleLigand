#!/bin/bash --login

biaslist=$(seq 0.70 0.05 1.40)

for bias in ${biaslist}
do
	python cos_th.py -bias ${bias} -log
done
