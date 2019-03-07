# Generating PSF file from CHARMM
Last updated: Mar 07 2019  

Generate PSF/PDB files for NAMD using CHARMM instead of VMD. 
VMD does not have lone pair support on halogen atoms in accordance with CGenFF v2.2.0. 
An example is provided in this directory.

1. From the mol2 file, generate PDB file. 
    * Can use VMD, or this Python script: <https://github.com/vtlim/off_psi4/blob/master/tools/convertExtension.py>
    * `python /beegfs/DATA/mobley/limvt/openforcefield/pipeline/github/tools/convertExtension.py -i clgbi_down_mmff.mol2 -o clgbi_down.pdb`
    * Edited PDB to have resname and segname of `GBIC`.
    * Changed "HETATM" to "ATOM  " for proper reading by CHARMM else it says no residues read.

2. Separate the stream file to two separate files: topology (.rtf) and parameter (.prm). VTL had trouble getting CGenFF to read the .str file properly.
    * The .rtf topology file is most of the top half of the stream file, and the .prm parameter file is most of the second half.
    * Formatted w/ref from examples from Sunhwan in [forum](https://www.charmm.org/ubbthreads/ubbthreads.php?ubb=showflat&Number=30257)

3. Add the lone pair details in the charmm input file. I also took this out of the .rtf and .prm completely. 
    * See CHARMM docs for more formatting information.

4. Edit the filenames for input PDB and output PSF/PDB. Then call the script (use your own charmm executable):
    * `/data11/home/limn1/charmm/c40b1_gnu/exec/gnu/charmm -i namdpsf-from-charmm.inp > psfgen.out`

## Contents
```
.
├── cl-gbi_pos_up.mol2          [1] coords of initial mol2
├── clgbi_up_mmff.mol2          [2] coords after opt_mmff.py 
├── clgbi_up.pdb                [3] coords after convertExtension.py, manually pasting optimized QM coords
├── gbi_chloro-00.prm           parameter file from str file 
├── gbi_chloro-00.rtf           topology file from str file
├── gbi_chloro-00.str           str file from CGenFF
├── namdpsf-from-charmm.inp     CHARMM input file
├── psfgen.out                  output after calling CHARMM
├── README.md                   this document
├── test.pdb                    final result after CHARMM
└── test.psf                    final result after CHARMM

0 directories, 11 files
```
