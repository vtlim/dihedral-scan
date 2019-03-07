# Generate psf file. Usage: "vmdt file.pdb -e file.tcl > psfgen.out"

mkdir temp
set segs [lsort -unique [[atomselect top "all"] get segname]]
	  foreach seg $segs {
	      [atomselect top "segname $seg"] writepdb ./temp/${seg}.pdb
	  }

package require psfgen
topology /DFS-L/DATA/mobley/limvt/toppar/cgenff4.0/top_all36_cgenff.rtf
topology ../../cgenff/gbi-neutral-02.str

segment GBIN {
    pdb ./temp/GBIN.pdb
}
coordpdb ./temp/GBIN.pdb

guesscoord
writepsf gbin_psfgen.psf
writepdb gbin_psfgen.pdb

exit

