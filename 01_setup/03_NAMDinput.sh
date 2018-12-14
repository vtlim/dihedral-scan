#!/usr/bin/env bash

# With frozen dihedral, optimize structure.
# Run: ./file.sh

homedir=/DFS-L/old_beegfs_data/mobley/limvt/hv1/05_qmDihedScan/3_neutral/dihed_namd
cd $homedir

for d in */; do
  echo "---------------- ${d%/} ------------------"
  wdir=${homedir}/${d}
  cd $wdir

  ### Copy base input file and edit.
#  if [ -f minimize.inp ]; then
#    echo "Input already exists."
#    continue
#  fi
  
  # Changing to hpc config file to copy and run there. (cp -i to check overwrite)
  cp /DFS-L/old_beegfs_data/mobley/limvt/hv1/05_qmDihedScan/3_neutral/11_setup-namd/minimize.inp minimize.inp
  sed -i "s/-0/-${d%/}/g" minimize.inp  

  ### Generate dihedral constraint file.
  DIHF=dihed-${d%/}.cnst
  printf "dihedral 7 8 9 10 2000. ${d%/}.\n" > $DIHF  

  cd ../

done

