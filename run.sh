#!/bin/bash

biaslist=$(seq 1.150 0.025 1.400)

for bias in ${biaslist}
do
	python printcosine.py -bias ${bias} > cosine.plu
	lmp_plumed -in in.long -log log.${bias}.lammps
	mv dump.340 dump_files/dump.340.${bias}
	mv log.${bias}.lammps log_files/
done
