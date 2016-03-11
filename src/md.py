#*********************************************************************************
#* Copyright (C) 2016 Ekadashi Pradhan, Kosuke Sato, Alexey V. Akimov
#*
#* This file is distributed under the terms of the GNU General Public License
#* as published by the Free Software Foundation, either version 2 of
#* the License, or (at your option) any later version.
#* See the file LICENSE in the root directory of this distribution
#* or <http://www.gnu.org/licenses/>.
#*
#*********************************************************************************/

## \file md.py
# This module implements the functions which execute classical MD.
#
import os
import sys
import math

# First, we add the location of the library to test to the PYTHON path
sys.path.insert(1,os.environ["libra_mmath_path"])
sys.path.insert(1,os.environ["libra_chemobjects_path"])
sys.path.insert(1,os.environ["libra_hamiltonian_path"])
sys.path.insert(1,os.environ["libra_dyn_path"])

from libmmath import *
from libchemobjects import *
from libhamiltonian import *
from libdyn import *
from LoadPT import * 
from exe_espresso import*
from unpack_file import*
from libra_to_espresso import*

##############################################################

def run_MD(syst,data,params):
    ##
    # Finds the keywords and their patterns and extracts the parameters
    # \param[in,out] syst System object that includes atomic system information.
    # \param[in,out] el   The list of the objects containig electronic DOFs for the nuclear coordinate
    #                     given by syst, but may correspond to differently-prepared coherent
    # wavefunctions (different superpositions or sampling over the wfc phase, initial excitations).
    # Under CPA, the propagation of several such variables corresponds to the same nuclear dynamics,
    # we really don't need to recompute electronic structure for each one, which can be used to 
    # accelerate the computations. Now, if you want to go beyond CPA - just use only one object in
    # the el list and run several copies of the run_MD function to average over initial conditions.
    # Also note that even under the CPA, we need to run this function several times - to sample
    # over initial nuclear distribution
    # \param[in,out] data Data extracted from GAMESS output file, in the dictionary form.
    # \param[in,out] params Input data containing all manual settings and some extracted data.
    # \param[out] test_data  the output data for debugging, in the form of dictionary

    # This function executes classical MD in Libra and electronic structure calculation
    # in Quantum Espresso iteratively.
    #
    # Used in:  main.py/main
    # Open and close energy and trajectory files - this will effectively 
    # make them empty (to remove older info, in case we restart calculations)
    fe = open(params["ene_file"],"w")
    fe.close()
    ft = open(params["traj_file"],"w")
    ft.close()
    
    dt_nucl = params["dt_nucl"]
    Nsnaps = params["Nsnaps"]
    Nsteps = params["Nsteps"]

    # Create a variable that will contain propagated nuclear DOFs
    mol = Nuclear(3*syst.Number_of_atoms)
    syst.extract_atomic_q(mol.q)
    syst.extract_atomic_p(mol.p)
    syst.extract_atomic_f(mol.f)
    syst.extract_atomic_mass(mol.mass)

    # Rydberg to Hartree conversion factor
    Ryd_to_Hrt = 0.5

    # Run actual calculations
    for i in xrange(Nsnaps):

        for j in xrange(Nsteps):
            # >>>>>>>>>>> Nuclear propagation starts <<<<<<<<<<<<
            mol.propagate_p(0.5*dt_nucl)
            mol.propagate_q(dt_nucl) 
            libra_to_espresso(data, params, mol)
            exe_espresso(params)         
            E, Grad, data = unpack_file(params["qe_out"])
            epot = Ryd_to_Hrt*E    # total energy from QE, the potential energy acting on nuclei

            # Ry/au unit of Force in Quantum espresso
            # So, converting Rydberg to Hartree
            for k in xrange(syst.Number_of_atoms):
                mol.f[3*k]   = Ryd_to_Hrt*Grad[k][0]
                mol.f[3*k+1] = Ryd_to_Hrt*Grad[k][1]
                mol.f[3*k+2] = Ryd_to_Hrt*Grad[k][2]

            mol.propagate_p(0.5*dt_nucl)
            # >>>>>>>>>>> Nuclear propagation ends <<<<<<<<<<<<
            ekin = compute_kinetic_energy(mol)
            t = dt_nucl*(i*Nsteps + j) # simulation time in a.u.
        ################### Printing results ############################
        fe = open(params["ene_file"],"a")
        fe.write("i= %3i ekin= %8.5f  epot= %8.5f  etot= %8.5f\n" % (i, ekin, epot, ekin+epot)) 
        syst.set_atomic_q(mol.q)
        syst.print_xyz(params["traj_file"],i)
        fe.close()
    # input test_data for debugging
    test_data = {}

    return test_data

def init_system(data, g):
    ##
    # Finds the keywords and their patterns and extracts the parameters
    # \param[in] data   The list of variables, containing atomic element names and coordinates
    # \param[in] g      The list of gradients on all atoms
    # This function returns System object which will be used in classical MD.
    #
    # Used in:  main.py/main

    # Create Universe and populate it
    U = Universe();   Load_PT(U, "elements.txt", 0)

    syst = System()

    sz = len(data["coor_atoms"])
    for i in xrange(sz):
        atom_dict = {} 
        atom_dict["Atom_element"] = data["l_atoms"][i]

        # warning: below we take coordinates in Angstroms, no need for conversion here - it will be
        # done inside
        atom_dict["Atom_cm_x"] = data["coor_atoms"][i][0]
        atom_dict["Atom_cm_y"] = data["coor_atoms"][i][1]
        atom_dict["Atom_cm_z"] = data["coor_atoms"][i][2]

        print "CREATE_ATOM ",atom_dict["Atom_element"]
        at = Atom(U, atom_dict)
        at.Atom_RB.rb_force = VECTOR(-g[i][0], -g[i][1], -g[i][2])

        syst.CREATE_ATOM(at)

    syst.show_atoms()
    print "Number of atoms in the system = ", syst.Number_of_atoms

    return syst



