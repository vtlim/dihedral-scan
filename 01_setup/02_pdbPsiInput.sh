#!/usr/bin/env bash

# With frozen dihedral, optimize structure.
# Change level of theory directory name and "set basis" label as needed.
# Run: ./file.sh
# Check for tautomer charge, dihedral atoms.

homedir=/DFS-L/old_beegfs_data/mobley/limvt/hv1/05_qmDihedScan/3_neutral/dihed_psi4
cd $homedir

for d in */; do
  echo "---------------- ${d%/} ------------------"
  wdir=${homedir}/${d}
  cd $wdir


  ### Read in cartesian coordinates from PDB
  PDB="$(ls ${wdir}/*.pdb)"
  COORDS=$(grep "GBI" $PDB | awk '{print " ",substr($3,0,1),"   ",$6,"   ",$7,"   ",$8}')

  #theory='mp2-def2tzvp'  
  theory='mp2-631Gd'  
  #theory='b3lyp'
  mkdir $theory
  INPUTF=${wdir}/${theory}/input.dat

  ### Print heading.
  printf "molecule GBIN_angle${d%/} {\n  0 1\n" > $INPUTF

  ### Print coordinates.
  echo "$COORDS" >> $INPUTF
  printf "}\n\nset optking {\n  frozen_dihedral = (\"\n    8 9 10 11\n  \")" >> $INPUTF

  printf "\n}\nset basis 6-31G*\noptimize('mp2')" >> $INPUTF
  #printf "\n}\nset basis def2-tzvp\noptimize('mp2')" >> $INPUTF
  #printf "\n}\nset basis def2-tzvp\noptimize('b3lyp-d3mbj')" >> $INPUTF

  cd ../

done

