#!/bin/bash --login

biaslist=$(seq -0.75 0.05 -0.25)

for bias in ${biaslist}
do
	python cos_th.py -bias ${bias}
done
