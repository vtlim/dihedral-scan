
import sys
import openeye.oechem as oechem
import quanformer.initialize_confs as initialize_confs
import quanformer.confs_to_psi as confs_to_psi

# Usage: python opt_mmff.py input_mol_file output_mol_file

def call_writer(mol):
    ofile = open('input.dat','w')
    ofile.write(confs_to_psi.make_psi_input(mol, 'chloroGBI', 'mp2', '6-31G*', 'opt', '2 Gb'))
    ofile.close()

def call_opt(infile, outfile):
    ifs = oechem.oemolistream()
    if not ifs.open(infile):
        oechem.OEThrow.Warning("Unable to open %s for reading" % smiles)
    ofs = oechem.oemolostream()
    if not ofs.open(outfile):
        oechem.OEThrow.Fatal("Unable to open %s for writing" % outfile)

    for mol in ifs.GetOEMols():
        oechem.OETriposAtomNames(mol)
        oechem.OEAddExplicitHydrogens(mol)
        initialize_confs.quick_opt(mol)
        oechem.OEWriteConstMolecule(ofs, mol)
        call_writer(mol)

    return mol

if __name__ == "__main__":
    xmol = call_opt(sys.argv[1],sys.argv[2])

