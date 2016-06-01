#*********************************************************************************
#* Copyright (C) 2016 Ekadashi Pradhan, Alexey V. Akimov
#*
#* This file is distributed under the terms of the GNU General Public License
#* as published by the Free Software Foundation, either version 2 of
#* the License, or (at your option) any later version.
#* See the file LICENSE in the root directory of this distribution
#* or <http://www.gnu.org/licenses/>.
#*
#*********************************************************************************/

## \file main.py
# This module defines the function which communicates QUANTUM ESPRESSO output data
# to Libra and vice versa.
# It outputs the files needed for excited electron dynamics simulation.
import os
import sys
import math


if sys.platform=="cygwin":
    from cyglibra_core import *
elif sys.platform=="linux" or sys.platform=="linux2":
    from liblibra_core import *

from libra_py import *



#Import libraries
from read_qe_inp_templ import*
from exe_espresso import*
from unpack_file import*
from md import *

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
<<<<<<< HEAD
    tot_ene, label, R, grads,params["norb"],params["nel"],params["nat"],params["alat"] = unpack_file(params["qe_out0"], params["qe_debug_print"],1)
=======
    tot_ene, label, R, grads = unpack_file(params["qe_out0"], params, params["qe_debug_print"])

>>>>>>> e8a78542f440390b41a1d078d0d386844e00a8ac
    ################## Step 2: Initialize molecular system and run MD ###########################

    print "Initializing system..."
    df = 0 # debug flag
    #Generate random number
    rnd = Random()

    # Here we use libra_py module!
    syst = init_system.init_system(label, R, grads, rnd, params["Temperature"], params["sigma_pos"], df, "elements.txt")      


    # starting MD calculation
    test_data = run_MD(label,syst,params)
    return test_data

