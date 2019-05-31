#!/usr/bin/python

"""
dihed_parser.py

Purpose:    Extract energies from QM and/or MM dihedral scans.
            Supports Psi4 for QM, and NAMD for MM.

Example:    python dihedParser.py --qdir /path/to/qdir --qfile output.dat --mdir /path/to/mdir --mfile minimize.log --show --save
By:         Victoria T. Lim
Version:    Dec 12 2016, with light editing Dec 2018

"""

import os, glob, re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import argparse


# --------------------------------------------- #

def numericalSort(value):

   """
   Parses some number. 5 would return ['5']. 5.4 would return ['5', '4'].
   Only used for sorting in cat_* functions.

   """
   numbers = re.compile(r'(\d+)') # parses a given value
   parts = numbers.split(value)
   parts[1::2] = list(map(int, parts[1::2]))

   return parts

def read_summary(filename):
    angs = []
    enes = []
    with open(filename) as ff:
        for line in ff:
            parts = line.split()
            angs.append(float(parts[0]))
            enes.append(float(parts[1]))
    angs = np.asarray(angs)
    enes = np.asarray(enes)
    return angs, enes


def cat_qm(qmdir, fname, theory='mp2-631Gd'):

    """
    For a directory containing subdirectories of all angles,
       get the final energy of the angle from the output fname.

    Parameters
    ----------
    qmdir : string
        Directory containing QM angle directories
    fname: string | name of the output file. assumed same for all angle jobs.
    theory: string | part of the path with the level of theory identifier.

    Returns
    -------
    angs: numpy array of reference dihedral angle of scan
    enes: numpy array with final energy of QM optimization (if completed)

    """

    # Get list of all angles' output files
    # One * for angle and one * for level of theory
    qmfiles = sorted(glob.glob(qmdir+'/*/'+theory+'/'+fname), key=numericalSort)
    outfile = 'summary-qm.dat'
    angs = np.zeros(len(qmfiles))
    enes = np.zeros(len(qmfiles))

    # don't write file if already exists
    if os.path.exists(outfile):
       print("!!! WARNING: {} already exists. Reading from summary file.".format(outfile))
       angs, enes = read_summary(outfile)
       return angs, enes

    # open the output file for summarized results
    with open(outfile, 'w') as output:
        # loop over all angle output files
        for i, filename in enumerate(qmfiles):
            with open(filename) as fname:
                # for this file, look for the line with the final energy
                for line in fname:
                    if "Final energy" in line:
                        angle = filename.split(qmdir)[1].split('/')[0]
                        energy = float(re.sub(' +', ' ', line).split(' ')[3])

                        angs[i] = angle
                        enes[i] = energy
                        output.write('{}\t{}\n'.format(angle, energy))
    return angs, enes




def cat_mm(mmdir, fname):

    """
    For a directory containing subdirectories of all angles,
       get the final energy of the angle from the output fname.

    Parameters
    ----------
    mmdir : string
        Directory containing MM angle directories
    fname: string | name of the output file. assumed same for all angle jobs.

    Returns
    -------
    angs: numpy array of reference (not actual) dihedral angle of scan
    enes: numpy array with potential energy term from NAMD log files

    """
    # Get list of all angles' output files
    mmfiles = sorted(glob.glob(mmdir+'/*/'+fname), key=numericalSort)
    outfile = 'summary-mm.dat'
    angs = np.zeros(len(mmfiles))
    enes = np.zeros(len(mmfiles))

    # don't write file if already exists
    if os.path.exists(outfile):
       print("!!! WARNING: {} already exists. Reading from summary file.".format(outfile))
       angs, enes = read_summary(outfile)
       return angs, enes

    # open the output file for summarized results
    with open(outfile, 'w') as output:
        # loop over all angle output files
        for i, filename in enumerate(mmfiles):
            # for this file, look for the line with the final energy
            for line in reversed(open(filename).readlines()):
                if line.startswith('ENERGY:'):
                    angle = filename.split(mmdir)[1].split('/')[0]
                    energy = float(re.sub(' +', ' ', line).split(' ')[13])

                    angs[i] = angle
                    enes[i] = energy
                    output.write('{}\t{}\n'.format(angle, energy))
                    break
    return angs, enes



def subtract_restraint(filename, fConst):
    """

    Subtract restraint energy for MM energies. Using harmonic (not cos)
    potential based on setup in the extra bonds file.
                 k * (x_actual - x_reference) ^ 2

    Parameters
    ----------
    filename : string
        filename with actual, measured dihedral angles from minimization
    fConst: float
        value of the spring constant k declared in NAMD extra bonds file

    Returns
    -------
    xact
    rpe: numpy array with restraint potential energies for all dihedral angles in filename

    """
    xref = []   # reference dihedral angles
    xact = []   # actual dihedral angles

    with open(filename) as ff:
        for line in ff:
            parts = line.split()
#            i = int(parts[0])/5  # get index for list. assumes ALL angles are present & in order
            xref.append( parts[0] )
            xact.append( parts[1] )

    # Convert to numpy arrays
    xref = np.asarray(xref, dtype=np.int32)
    xact = np.asarray(xact, dtype=np.float32)

    # If the angle is negative, add 360.
    for i,ang in enumerate(xact):
        if ang < 0: xact[i] = ang+360

    # for the first angle, make ~0 if it's ~360
    if abs(xact[0]) > 5:
        xact[0] = xact[0] - 360

    # Get the restraint energies.
    rpe = float(fConst)*np.subtract(xact,xref)**2.
    np.set_printoptions(suppress=True,precision=2)
    for k in range(xact.shape[0]):
        print(xact[k], xref[k], rpe[k])
    return xact, rpe


def plot_dihed(x, y, pdict, toSave, toShow, x2=None, y2=None):

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    xlabel = "angle (degrees)"
    ylabel = "energy (kcal/mol)"

    ### Label the figure, larger font
    ax1.set_title(pdict['title'],fontsize=20)
    ax1.set_xlabel(xlabel,fontsize=18)
    ax1.set_ylabel(ylabel,fontsize=18)

    ### Increase font size of tick labels
    #ax1.set_xticklabels(xticks,fontsize=14)
    for ytick in ax1.get_yticklabels():
        ytick.set_fontsize(14)
    for xtick in ax1.get_xticklabels():
        xtick.set_fontsize(14)

    if x2 is None and y2 is None:
        ax1.scatter(x, y,edgecolors='none')

    elif x2 is not None and y2 is not None:
        ax1.scatter(x, y, edgecolors='none',  color=pdict['color1'],label=pdict['label1'])
        ax1.scatter(x2, y2, edgecolors='none',color=pdict['color2'],label=pdict['label2'])

    else:
        print("Either none or both x2 and y2 should be defined.")
        return

    plt.grid()
    plt.grid(which='both', color='0.65',linestyle='-')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    if opt['save'] == True: plt.savefig(pdict['figname'],bbox_inches='tight')
    if opt['show'] == True: plt.show()
    plt.ioff()
    plt.close()

def process_plot_qm(qdir, qfile, qtheory, savefig, showfig):
    ang_qm, ene_qm = cat_qm(qdir, qfile, qtheory)

    indices = np.nonzero(ene_qm)
    ang_qm = ang_qm[indices]
    ene_qm = ene_qm[indices]

    minE = min(ene_qm)
    rel_ene_qm = [627.5095*(i - minE) for i in ene_qm] # convert Hartrees -> kcal/mol

    pdict = {}
    pdict['title'] = "Dihedral Scan - QM"
    pdict['figname'] = "plot_relDihed-qm.png"
    plot_dihed( ang_qm, rel_ene_qm, pdict, savefig, showfig)

    return ang_qm, ene_qm, rel_ene_qm

def process_plot_mm(mdir, mfile, force_const):
    ang_mm, ene_mm = cat_mm(mdir, mfile)

    ### Subtract actual energies minus restraint energies.
    if force_const is not None:
        xact, rpe = subtract_restraint(mdir+'/diheds-from-coor.dat', force_const)
        ene_mm = np.subtract(ene_mm,rpe)

    ### Take relative energies from minimum.
    minE = min(ene_mm)
    rel_ene_mm = [i - minE for i in ene_mm]

    ### Plot MM results.
    pdict = {}
    pdict['title'] = "Dihedral Scan - MM"
    pdict['figname'] = "plot_relDihed-mm.png"
    plot_dihed( ang_mm, rel_ene_mm, pdict, opt['save'], opt['show'] )

    return ang_mm, ene_mm, rel_ene_mm


# ------------------------- Script ---------------------------- #

def main(**kwargs):

    if opt['qm_only']:
        ang_qm, ene_qm, rel_ene_qm = process_plot_qm(opt['qdir'], opt['qfile'], opt['theory'], opt['save'], opt['show'])
        return
    elif opt['mm_only']:
        ang_mm, ene_mm, rel_ene_mm = process_plot_mm(opt['mdir'], opt['mfile'], opt['fConst'])
        return
    else:
        ang_qm, ene_qm, rel_ene_qm = process_plot_qm(opt['qdir'], opt['qfile'], opt['theory'], opt['save'], opt['show'])
        ang_mm, ene_mm, rel_ene_mm = process_plot_mm(opt['mdir'], opt['mfile'], opt['fConst'])

    ### Plot both QM and MM results.
    pdict = {}
    pdict['title'] = "Dihedral Scan
    pdict['figname'] = "plot_relDihed.png"
    pdict['label1'] = "MM (NAMD, CGenFF)"      # MM line label
    pdict['label2'] = "QM (Psi4, MP2/6-31G*)"  # QM line label
    #pdict['label2'] = "QM (Psi4, MP2/def2-tzvp)"  # QM line label
    pdict['color1'] = 'b'      # MM line color
    pdict['color2'] = 'r'      # QM line color
    plot_dihed( ang_mm, rel_ene_mm, pdict, opt['save'], opt['show'], ang_qm, rel_ene_qm)


    ### Write out results.
    if not os.path.exists("summary.dat"):
        with open("summary.dat",'w') as writeout:

            writeout.write("\n\tRESULTS FOR QM DIHEDRAL SCAN")
            writeout.write("\n\t----------------------------")
            writeout.write("\nangle_ref\ttotE(Har)\t\trelE(kc/mol)")
            for i in range(len(rel_ene_qm)):
                writeout.write("\n\t%.1f\t\t%.3f\t%.3f" % (ang_qm[i], ene_qm[i], rel_ene_qm[i]))

            if not opt['qm_only']:
                writeout.write("\n\n\tRESULTS FOR MM DIHEDRAL SCAN")
                writeout.write("\n\t----------------------------")
                writeout.write("\nangle_ref\tangle_act\ttotalE\t\trestrE\t(tot-restr)\torigTotE (rel)")
                for i in range(len(rel_ene_mm)):
                    writeout.write("\n\t%.2f\t%f\t%.3f\t%.3f\t%.3f\t%.3f" % (ang_mm[i], ang_mm[i], ene_mm[i], rpe[i], rs_ene_mm[i],rel_ene_mm[i]))
    else:
        print("!!! WARNING: {} already exists. Skip writing summary results.".format('summary.dat'))


#    ### Plot total, restraint, and tot-restr energies for MM scan.
#    fig = plt.figure()
#    ax1 = fig.add_subplot(111)
#    plttitle = "Energies of MM dihedral Scan"
#    FormatPlot(plttitle)
#    figname = "plot_totRestrEnes.png"
#    ax1.plot(x, rpe, label='harmonic restraint E')
#    ax1.plot(x, enes, label='total original E')
#    ax1.plot(x, fins, label='total - restraint E')
#    plt.legend(loc='center right')
#    if opt['save'] == True: plt.savefig(figname,bbox_inches='tight')
#    if opt['show'] == True: plt.show()
#    plt.ioff()
#    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # QM-related arguments
    parser.add_argument("--qdir",
                        help="Name of directory containing QM angles")
    parser.add_argument("--qfile", default='output.dat',
                        help="Name of QM output file (should be same name for all angles)")
    parser.add_argument("-t", "--theory", default='mp2-631Gd',
                        help="Part of the path with the level of theory subdirectory")
    parser.add_argument("--qm_only", action="store_true", default=False,
                        help="Only process QM results.")

    # MM-related arguments
    parser.add_argument("--mdir",
                        help="Name of directory containing MM angles")
    parser.add_argument("--mfile",
                        help="Name of MM output file (should be same name for all angles)")
    parser.add_argument("--mm_only", action="store_true", default=False,
                        help="Only process MM results.")
    parser.add_argument("-k", "--fConst", type=float,
                        help="Value of force constant used to restrain dihedral"
                             " in MM calculation. NOTE: This is NOT currently "
                             "used. The dihedral scan makes no sense when subtracting"
                             " the k(x-x0)^2 energy. It could be that the potential"
                             " energy term in NAMD output file already doesn't "
                             "include the restraint term when implemented via "
                             "the extraBonds parameter.")
    # https://www.ks.uiuc.edu/Research/namd/2.13/ug/node27.html
    # should be in MISC column:
    # https://www.ks.uiuc.edu/Research/namd/mailing_list/namd-l.2010-2011/1906.html

    # Plot-related arguments
    parser.add_argument("--show", action="store_true", default=False,
                        help="Display all plots generated.")
    parser.add_argument("--save", action="store_true", default=False,
                        help="Save all plots.")


    args = parser.parse_args()
    opt = vars(args)
    main(**opt)

