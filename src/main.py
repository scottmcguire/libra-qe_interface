#*********************************************************************************
#* Copyright (C) 2016 Kosuke Sato, Alexey V. Akimov
#*
#* This file is distributed under the terms of the GNU General Public License
#* as published by the Free Software Foundation, either version 2 of
#* the License, or (at your option) any later version.
#* See the file LICENSE in the root directory of this distribution
#* or <http://www.gnu.org/licenses/>.
#*
#*********************************************************************************/

## \file main.py
# This module sets initial parameters from GAMESS output, creates initial system, 
# and executes runMD script.
# 
# It returns the data from runMD for debugging the code.

import os
import sys
import math
import copy

import sys

if sys.platform=="cygwin":
    from cyglibra_core import *
elif sys.platform=="linux" or sys.platform=="linux2":
    from liblibra_core import *

from libra_py import *



# First, we add the location of the library to test to the PYTHON path
#sys.path.insert(1,os.environ["src_path"]) # Path the the source code
#sys.path.insert(1,os.environ["libra_mmath_path"])
#sys.path.insert(1,os.environ["libra_qchem_path"])
#sys.path.insert(1,os.environ["libra_dyn_path"])
#sys.path.insert(1,os.environ["libra_chemobjects_path"])
#sys.path.insert(1,os.environ["libra_hamiltonian_path"])

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
    # Used in:  main.py    

    nstates = len(params["excitations"])
    ninit = params["nconfig"]  
    ntraj = nstates*ninit

    ################# Step 0: Use the initial file to create a working input file ###############
 
    os.system("cp %s %s" %(params["gms_inp0"], params["gms_inp"]))

    ################# Step 1: Read initial input and run first GMS calculation ##################    
    
    params["gms_inp_templ"] = read_gms_inp_templ(params["gms_inp"])

    exe_gamess(params)

    label, Q, R, grad, e, c, ao = extract(params["gms_out"],params["debug_gms_unpack"])

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

    #sys.exit(0)

    print "Initializing nuclear configuration and electronic variables..."
    rnd = Random() # random number generator object
    syst = []
    el = []

    # all excitations fr each nuclear configuration
    for i in xrange(ninit):
        print "init_system..."
        #syst_ = init_system(data[i], Grad[i], rnd, params["Temperature"], params["sigma_pos"])        
        for i_ex in xrange(nstates):
            print "Create a copy of a system"  
            df = 0 # debug flag

            # Here we use libra_py module!
            x = init_system.init_system(label_list[i], R_list[i], grad_list[i], rnd, params["Temperature"], params["sigma_pos"], df, "elements.txt")
            syst.append(x)    

            print "Create an electronic object"
            el.append(Electronic(nstates,i_ex))
    

    #sys.exit(0)  #### DEBUG!!!


    print "Starting MD..."
    cnt = 0
    for i in xrange(ninit):
        for i_ex in xrange(nstates):
            print "Trajectory ", i, " initial excitation ",i_ex

            params["ene_file"] = params["ene_file_prefix"]+"_"+str(i)+"_"+str(i_ex)+".txt"
            params["traj_file"] = params["traj_file_prefix"]+"_"+str(i)+"_"+str(i_ex)+".txt"
            params["mu_file"] = params["mu_file_prefix"]+"_"+str(i)+"_"+str(i_ex)+".txt"
            params["se_pop_file"] = params["se_pop_file_prefix"]+"_"+str(i)+"_"+str(i_ex)+".txt"

            print "run MD"
            run_MD(syst[cnt],el[cnt],ao_list[cnt],e_list[cnt],c_list[cnt],params,label_list[i], Q_list[i])
            print "MD is done"
            cnt = cnt + 1

    #return data, test_data
