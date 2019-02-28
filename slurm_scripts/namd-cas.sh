# VTL script to run namd2 jobs on GPU on Cassandra
# tsp -L [label] sh ../../namd-cas.sh

export NAMD="/home/limvt/local/lib/namd2.13"
export LD_LIBRARY_PATH="${NAMD}/libcudart.so.9.1"
echo $NAMD
echo $LD_LIBRARY_PATH

date 

$NAMD/namd2 +idlepoll +isomalloc_sync +p4 minimize.inp > minimize.out

date


