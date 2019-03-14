# Purpose: Generate input pdbs with varying dihedral angle.
# Usage: "vmdt -e file.tcl"
# Check: guanidino atom numbers, set_dihedral atom numbers

proc set_dihedral {molid movesel newval ind1 ind2 ind3 ind4} {
  set tmpmolid $molid
  set dihedral [measure dihed [list [list $ind1 $tmpmolid] [list $ind2 $tmpmolid] [list $ind3 $tmpmolid] [list $ind4 $tmpmolid] ]]

  ### Validate input.
  if {$ind1 == "" || $ind2 == "" || $ind3 == "" || $ind4 == ""} {
    puts "WARNING: Couldn't find one or more atoms for set_dihedral"
    return
  }

  ### Set both atoms of the central bond.
  set bsel1 [atomselect $tmpmolid "index $ind2"]
  set bsel2 [atomselect $tmpmolid "index $ind3"]

  ### Get degree to move by, and the move matrix.
  set delta [expr $dihedral - $newval]
  set mat [trans bond [lindex [$bsel1 get {x y z}] 0] [lindex [$bsel2 get {x y z}] 0] $delta deg]

  ### Move the selection by that matrix.
  $movesel move $mat
  $bsel1 delete
  $bsel2 delete

  ### User information.
  set dihedral [measure dihed [list [list $ind1 $tmpmolid] [list $ind2 $tmpmolid] [list $ind3 $tmpmolid] [list $ind4 $tmpmolid] ]]
  puts $dihedral
}


mol new "orig.pdb" type {pdb} first 0 last -1 step 1 waitfor -1
set guanidino [atomselect 0 "index 21 12 10 11 20 19 18"]

for {set angle 0} {$angle < 360} {incr angle 5} {
    set_dihedral 0 $guanidino $angle 10 9 8 7
    mkdir ../dihed_namd/$angle
    [atomselect top "all"] writepdb ../dihed_namd/$angle/dihed-$angle.pdb
}

