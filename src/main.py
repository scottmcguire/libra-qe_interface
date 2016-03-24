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

# Path the the source code
# First, we add the location of the library to test to the PYTHON path
sys.path.insert(1,os.environ["src_path"]) # Path the the source code
sys.path.insert(1,os.environ["libra_mmath_path"])
sys.path.insert(1,os.environ["libra_qchem_path"])
sys.path.insert(1,os.environ["libra_dyn_path"])
sys.path.insert(1,os.environ["libra_chemobjects_path"])
sys.path.insert(1,os.environ["libra_hamiltonian_path"])

#Import read_qe_inp_templ.py library
from read_qe_inp_templ import*
#Import exe_espresso.py library
from exe_espresso import*
#Import from unpack_file.py library
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
 
    os.system("cp %s %s" %(params["qe_inp0"], params["qe_inp"]))

    ################# Step 1: Read initial input and run first QS calculation ##################    
    
    cell_dm, params["qe_inp_templ"] = read_qe_inp_templ(params["qe_inp"])

    exe_espresso(params)
    Grad = []
    E, Grad, data = unpack_file(params["qe_out"], cell_dm)

    print data

    ################## Step 2: Initialize molecular system and run MD ###########################

    print "Initializing system..."
#    syst = init_system(data, Grad)
    syst = init_system(data, Grad, params["Temperature"])

    syst.show_info()

    # starting MD calculation
    test_data = run_MD(syst,data,params,cell_dm)
    return data, test_data
