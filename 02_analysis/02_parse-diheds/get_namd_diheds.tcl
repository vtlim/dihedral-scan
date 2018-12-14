
# --------------------------------------------------------------
# get_namd_diheds.tcl
#
# Purpose: Measure dihedral angle of specified four atoms in
#   NAMD output .coor files. This is so that the the dihedral
#   reference angle for restraint can be subtracted from the
#   actual measured angle to plot dihedral scan profile.
#
# Usage:
#   1. cd to directory with the angles
#   2. vmdt -e get_namd_diheds.tcl -args inpsf ind1 ind2 ind3 ind4
#
# By:       Victoria T. Lim
# Version:  Dec 12 2018
# --------------------------------------------------------------

set inpsf [lindex $argv 0]
set ind1 [lindex $argv 1]
set ind2 [lindex $argv 2]
set ind3 [lindex $argv 3]
set ind4 [lindex $argv 4]

# get list of all subdirectories
set dirlist [glob */ ]

# open output file
set f [open diheds-from-coor.dat w]

set molid 0
foreach i $dirlist {

    # get file names
    set angle_dir [string trim $i "/"]
    set coorF [glob ${angle_dir}/*coor]

    # load files into vmd
    mol new $inpsf
    mol addfile $coorF

    # measure and write to file
    set angle [measure dihed [list [list $ind1 $molid] [list $ind2 $molid] [list $ind3 $molid] [list $ind4 $molid] ]]
    puts $f "$angle_dir $angle"

    mol delete all
    set molid [expr $molid+1 ]
}
close $f
exit

