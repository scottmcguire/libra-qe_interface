#*********************************************************************************
#* Copyright (C) 2016 Ekadashi Pradhan, Alexey V. Akimov
#*
#* This file is distributed under the terms of the GNU General Public License
#* as published by the Free Software Foundation, either version 2 of
#* the License, or (at your option) any later version.
#* See the file LICENSE in the root directory of this distribution
#* or <http://www.gnu.org/licenses/>.
#*^M
#*********************************************************************************/^M

## \file create_qe_input.py
# This module implements the functions which execute classical MD.
#

import math

from excited_state import*


def print_occupations(occ):
##
# This function transforms the list of occupations into a formatted
# text. The format is consistent with QE input
# \param[in] occ Occupation scheme representing an excitation (list of floats/integers)
#
    
    line = "OCCUPATIONS\n"
    count = 0
    for f in occ:
        line = line + "%5.3f " % f 
        count = count +1
        if count % 10 ==0:
            line = line + "\n"
    line = line + "\n"

    return line



def write_qe_input(label, params, mol):
##
# Creates the Quantum Espresso input using the data provided
# \param[in] label Element symbols for all atoms in the system (list of strings)
# \param[in] params The general control parameters (dictionary)
# \param[in] mol The object containing nuclear DOF
# \param[in] qe_inp Name of the input file to be written
#

    no_ex = params["no_ex"] 
    qe_inp_templ = params["qe_inp_templ"]

    for i in range(0, no_ex):
        qe_inp = params["qe_inp%i" %i]
        g = open(qe_inp, "w")    # open input file
        cell_dm = params["cell_dm"]

        # Write control parameters section
        tl = len(qe_inp_templ)
        for j in xrange(tl):
            g.write(qe_inp_templ[j])
        g.write("\n")

        # Write atom name and coordinatess
        Natoms = len(label)
        B_to_A = 1.0/cell_dm   # Bohr to Angstrom conversion
        for k in xrange(Natoms):
            atms = label[k]
            x = B_to_A*mol.q[3*k]
            y = B_to_A*mol.q[3*k+1]
            z = B_to_A*mol.q[3*k+2]
            g.write("%s    %12.7f    %12.7f    %12.7f  \n"  % (atms, x, y, z) )

        # Single excitations with no spin-polarization 
        occ = excited_state(params, i)
        g.write(print_occupations(occ))
        g.close()


