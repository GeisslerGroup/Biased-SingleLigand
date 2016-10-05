#!/bin/bash

biaslist=$(seq 0.30 0.05 1.60)

for bias in ${biaslist}
do
	python printtheta.py -bias 2000.0 -at_lower 1.65 -at_upper ${bias} > cosine.plu
	lmp_plumed -in in.long -log log.${bias}.lammps
	mv dump.340 dump_files/dump.340.${bias}
	mv log.${bias}.lammps log_files/
done
