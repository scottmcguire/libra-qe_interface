#*********************************************************************************
<<<<<<< HEAD
#* Copyright (C) 2016 Ekadashi Pradhan, Alexey V. Akimov
=======
#* Copyright (C) 2016 Kosuke Sato, Alexey V. Akimov
>>>>>>> 0780160722fa3c91c7b4f5c4512ca2cbb02d1481
#*
#* This file is distributed under the terms of the GNU General Public License
#* as published by the Free Software Foundation, either version 2 of
#* the License, or (at your option) any later version.
#* See the file LICENSE in the root directory of this distribution
#* or <http://www.gnu.org/licenses/>.
#*
#*********************************************************************************/

## \file main.py
<<<<<<< HEAD
# This module defines the function which communicates QUANTUM ESPRESSO output data
# to Libra and vice versa.
# It outputs the files needed for excited electron dynamics simulation.
import os
import sys
import math

=======
# This module sets initial parameters from GAMESS output, creates initial system, 
# and executes runMD script.
# 
# It returns the data from runMD for debugging the code.

import os
import sys
import math
import copy
>>>>>>> 0780160722fa3c91c7b4f5c4512ca2cbb02d1481

if sys.platform=="cygwin":
    from cyglibra_core import *
elif sys.platform=="linux" or sys.platform=="linux2":
    from liblibra_core import *

from libra_py import *
<<<<<<< HEAD



#Import libraries
from read_qe_inp_templ import*
from exe_espresso import*
from create_qe_input import*
from unpack_file import*
from md import *
from export_wfc import *


def main(params):
##
# Finds the keywords and their patterns and extracts the parameters
# \param[in] params : the input data from "submit_templ.slm", in the form of dictionary
# This function prepares initial parameters from QUANTUM ESPRESSO output file
# and executes classical MD in Libra and Electronic Structure Calculation in QUANTUM ESPRESSO
# iteratively.
#
# Used in:  main.py

    ################# Step 0: Use the initial file to create a working input file ###############
    os.system("cp %s %s" %(params["qe_inp00"], params["qe_inp0"]))

    ################# Step 1: Read initial input and run first QS calculation ##################    

    params["qe_inp_templ"] = read_qe_inp_templ(params["qe_inp0"])

    exe_espresso(params["qe_inp0"], params["qe_out0"])
    tot_ene, label, R, grad,params["norb"],params["nel"],params["nat"],params["alat"] = unpack_file(params["qe_out0"], params["qe_debug_print"],1)

    ################## Step 2: Initialize molecular system and run MD ###########################

    print "Initializing system..."
    df = 0 # debug flag
    #Generate random number
    rnd = Random()

    # Here we use libra_py module!
    syst = init_system.init_system(label, R, grad, rnd, params["Temperature"], params["sigma_pos"], df, "elements.txt")      

    # Create a variable that will contain propagated nuclear DOFs
    mol = Nuclear(3*syst.Number_of_atoms)
    syst.extract_atomic_q(mol.q)
    syst.extract_atomic_p(mol.p)
    syst.extract_atomic_f(mol.f)
    syst.extract_atomic_mass(mol.mass)

    
    n_el = params["nel"]
    n_mo = params["num_MO"]
    wfc = {}  # wavefunction dictionary, where all the coefficients of the MO basis will be saved
    # Running SCF calculation for different excited states, extracting their Energies, Forces and wavefucntion coefficients
    # savings coefficients as coeff_old
    for i in xrange(len(params["excitations"])):
        write_qe_input(params["qe_inp%i" %i],label,mol,params["excitations"][i],params)
        exe_espresso(params["qe_inp%i" % i], params["qe_out%i" % i] )
        wfc["coeff_old_%i"%i] = read_qe_wfc("x%i.export/wfc.1"%i, "Kpoint.1", n_el, n_mo)



    # starting MD calculation
    test_data = run_MD(label,syst,params,wfc)
    return test_data

=======
from gamess_to_libra import *
from md import *
from create_gamess_input import *


def main(params):
    ##
    # Finds the keywords and their patterns and extracts the parameters
    # \param[in] params  the input data from "submit_templ.slm", in the form of dictionary
    # Returned data:
    # test_data - the output data for debugging, in the form of dictionary
    # data - the data extracted from gamess output file, in the form of dictionary
    #
    # This function prepares initial parameters from GAMESS output file
    # and executes classical MD in Libra and Electronic Structure Calculation in GAMESS 
    # iteratively.
    # Parallelly, it executes TD-SE and SH calculation for simulating excited eletronic dynamics.
    #
    # Used in:  run.py

    dt_nucl = params["dt_nucl"]
    nstates = len(params["excitations"])
    ninit = params["nconfig"]  
    SH_type = params["tsh_method"]

    num_SH_traj = 1
    if SH_type >= 1: # calculate no SH probs.  
        num_SH_traj = params["num_SH_traj"]

    ntraj = nstates*ninit*num_SH_traj

    ################# Step 0: Use the initial file to create a working input file ###############
 
    os.system("cp %s %s" %(params["gms_inp0"], params["gms_inp"]))

    ################# Step 1: Read initial input and run first GMS calculation ##################    
    
    params["gms_inp_templ"] = read_gms_inp_templ(params["gms_inp"])

    #sys.exit(0)
    exe_gamess(params)

    label, Q, R, grad, e, c, ao, tot_ene = extract(params["gms_out"],params["debug_gms_unpack"])

    ao_list = []
    e_list = []
    c_list = []
    grad_list = []
    label_list = []
    Q_list = []
    R_list = []

    for i in xrange(ntraj):
        # AO
        ao_tmp = []
        for x in ao:
            ao_tmp.append(AO(x))
        ao_list.append(ao_tmp)

        # E and C
        e_list.append(MATRIX(e))
        c_list.append(MATRIX(c))        

        # Gradients
        grd = []
        for g in grad:
            grd.append(VECTOR(g))
        grad_list.append(grd)

        # Coords
        rr = []
        for r in R:
            rr.append(VECTOR(r))
        R_list.append(rr)

        # Labels and Q
        lab = []
        qq  = []
        for i in xrange(len(label)):
            lab.append(label[i])
            qq.append(Q[i])
        label_list.append(lab)
        Q_list.append(qq)
        

    ################## Step 2: Initialize molecular system and run MD part with TD-SE and SH####

    print "Initializing nuclear configuration and electronic variables..."
    rnd = Random() # random number generator object
    syst = []
    el = []

    # all excitations for each nuclear configuration
    for i in xrange(ninit):
        print "init_system..." 
        for i_ex in xrange(nstates):
            for itraj in xrange(num_SH_traj):
                print "Create a copy of a system"  
                df = 0 # debug flag
                # Here we use libra_py module!
                x = init_system.init_system(label_list[i], R_list[i], grad_list[i], rnd, params["Temperature"], params["sigma_pos"], df, "elements.txt")
                syst.append(x)    

                print "Create an electronic object"
                el.append(Electronic(nstates,i_ex))
    
    # set list of SH state trajectories

    print "run MD"
    run_MD(syst,el,ao_list,e_list,c_list,params,label_list, Q_list)
    print "MD is done"
    sys.exit(0)

    #return data, test_data
>>>>>>> 0780160722fa3c91c7b4f5c4512ca2cbb02d1481
