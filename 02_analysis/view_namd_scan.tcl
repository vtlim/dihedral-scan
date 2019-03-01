
# --------------------------------------------------------------
# view_namd_scan.tcl
#
# Purpose: View optimized geometries after a dihedral scan
#   from structures in NAMD output .coor files.
#
# Usage:
#   1. Set resname and file prefix parameters in this script.
#   1. cd to directory with the angles
#   2. vmd -e view_namd_scan.tcl -args together inpsf
#      > together is boolean; value of 1 (True) loads all frames into single molecule object in VMD
#
# By:       Victoria T. Lim
# Version:  Feb 28 2019
# --------------------------------------------------------------

# Parameters to change before using
set resname GBI2
set fileprefix gbi2-

# --------------------------------------------------------------

# parse inputs
set together [lindex $argv 0]
set inpsf [lindex $argv 1]

# list directories
set dirlist [glob */ ]

if {$together} {
  # load all coordinates into one mol, like a movie
  mol new $inpsf
  mol delrep 0 0
  mol addrep 0
  mol modselect 0 0 resname $resname
  mol modstyle 0 0 Licorice 0.200000 12.000000 30.000000
  mol modcolor 0 0 Name

  foreach i $dirlist {
      set dir [string trim $i "/"]
      mol addfile ${dir}/${fileprefix}${dir}.coor
  }

} else {
  # load all coordinates separately to show all frames at once
  set count 0
  foreach i $dirlist {
      set dir [string trim $i "/"]
      mol new $inpsf
      mol addfile ${dir}/${fileprefix}${dir}.coor

      mol delrep 0 $count
      mol addrep $count
      mol modselect 0 $count resname $resname
      mol modstyle 0 $count Licorice 0.200000 12.000000 30.000000
      mol modcolor 0 $count Name

      #mol off $count ;# don't display anything to start
      incr count
      cd ../
  }
}

