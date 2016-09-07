#!/bin/bash
set -o nounset
set -o errexit

tempfile=$(mktemp in_XXXXX.txt)
tempcode=$(echo $tempfile | cut -d"_" -f2 | cut -d'.' -f1)
echo $tempcode
biastemp="bias_${tempcode}.plu"
TargetT=340

biasval=${1?Pass bias mean(?????) to execute}

cat << BIAS > $biastemp
d1: DISTANCE ATOMS=1,9 COMPONENTS

MATHEVAL ...
LABEL=theta
ARG=d1.x,d1.y,d1.z
FUNC=atan(sqrt(x*x+z*z)/y)
PERIODIC={-pi,pi}
... MATHEVAL

RESTRAINT ARG=theta AT=${biasval} KAPPA=500.0 LABEL=restraint

PRINT ARG=theta STRIDE=10
BIAS

#d1: DISTANCE ATOMS=1,9 COMPONENTS
#
#MATHEVAL ...
#LABEL=xdist
#ARG=d1.x,d1.z
#FUNC=sqrt(x*x+y*y)
#PERIODIC=NO
#... MATHEVAL
#
#RESTRAINT ARG=xdist AT=${biasval} KAPPA=5000.0 LABEL=restraint
#
#PRINT ARG=xdist STRIDE=10
#BIAS

cat << HERE > $tempfile
# Hex xtal + ligands + ligand-xtal interactions

# initialization
units 		real
boundary 	p p p

atom_style	molecular  			# Allows for bonds, angles and torsions to be specified.
bond_style 	harmonic			# E = K(r-r0)^2
angle_style	harmonic			# E = K(t-t0)^2
dihedral_style	opls				# E = K1/2(1+cos(phi)) + K2/2(1-cos(2phi)) + K3/2(1+cos(3phi))
# atom_modify first command may be useful for full system, put ligands first

# variable	TargetT equal 340

read_data	singlelig.data
# read_data	solvatedlig.data
#read_restart	../restart.${TargetT}

group		ligand type 1 2
group		solvent type 5 6
group		ligand/solvent type 1 2 5 6
group		xtal type 3 4

compute		MyTemp ligand/solvent temp

# density calculations
variable	TargetDens equal 0.02587
variable	xlo equal 40
variable	xhi equal 65
variable	ylo equal 30
variable	yhi equal 45
variable	zlo equal 40
variable	zhi equal 65
# region		BulkSolv block \${xlo} \${xhi} \${ylo} \${yhi} \${zlo} \${zhi} side in units box
# variable        SolvDens equal count(solvent,BulkSolv)/((v_xhi-v_xlo)*(v_yhi-v_ylo)*(v_zhi-v_zlo))

# Main run

pair_style	lj/cut 14.0			# Cutoff distance in A for the LJ potential.

pair_modify 	shift yes mix arithmetic	# Shift the potential at the cutoff and use
						# arithmetic mixing rules to determine the 
						# interaction parameters for different 'atom'
						# types.

pair_coeff      1 1 0.195  3.75                 # For i-j interactions, define eps_ij and sigma_ij
pair_coeff      1 3 0.143  3.54    
pair_coeff      1 4 0.143  3.54    
pair_coeff      2 2 0.0914 3.95
pair_coeff      2 3 0.111  3.54    
pair_coeff      2 4 0.111  3.54    
pair_coeff      3 3 0.0    0.0 
pair_coeff      3 5 0.143 3.54
pair_coeff      3 6 0.111 3.54
pair_coeff      4 4 0   0.0 
pair_coeff      4 5 0.143 3.54
pair_coeff      4 6 0.111 3.54
pair_coeff      5 5 0.195 3.75
pair_coeff      6 6 0.0914 3.95

bond_coeff	* 95.9 1.54			# For all bonds, define K and r0

angle_coeff	* 62.1 114			# For all angles, define K and theta0

dihedral_coeff	* 1.4114 -0.2711 3.1458 0	# For all dihedrals, define Ki, note that K4=0 needs to be defined

#special_bonds	lj 0.0 0.0 0.0			# For some reason this command produces an error message complaining that the number of arguments is incorrect. Since the default should be the same I have left it out.
						# Turns off the lj interaction btw 1st, 2nd,
						# and 3rd nearest neighbours.

thermo		1000
thermo_style	custom step temp c_MyTemp etotal ke pe
#thermo_modify 	flush yes

reset_timestep	1
fix		1 ligand/solvent nvt temp ${TargetT} ${TargetT} 50
fix_modify	1 temp MyTemp
fix 		plumed all plumed plumedfile ${biastemp} outfile cosine${biasval}.out
dump		1 all xyz 1000 dump${biasval}-${tempcode}.${TargetT}
run		1000000 post no
write_restart	restart.${TargetT}
unfix		1
undump		1
HERE

lmp_plumed -in ${tempfile} -log log-${biasval}.lammps
cp dump${biasval}-${tempcode}.340 dump.xyz
