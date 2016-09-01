#!/bin/bash

biaslist=$(seq -0.20 0.05 0.10)

for bias in ${biaslist}
do
	python printcosine.py -bias ${bias} > cosine.plu
	lmp_plumed -in in.long -log log.${bias}.lammps
	mv dump.340 dump_files/dump.340.${bias}
	mv log.${bias}.lammps log_files/
done
