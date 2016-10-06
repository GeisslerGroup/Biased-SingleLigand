#!/bin/bash --login

biaslist=$(seq 0.30 0.05 1.60)

for bias in ${biaslist}
do
	python cos_th.py -bias ${bias} -save
done
