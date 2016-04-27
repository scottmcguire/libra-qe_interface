#*********************************************************************************
#* Copyright (C) 2015 Alexey V. Akimov
#*
#* This file is distributed under the terms of the GNU General Public License
#* as published by the Free Software Foundation, either version 2 of
#* the License, or (at your option) any later version.
#* See the file LICENSE in the root directory of this distribution
#* or <http://www.gnu.org/licenses/>.
#*
#*********************************************************************************/

##
# \file text_context.py This file demonstrates to read QE wavfunctions using
# context class of the libra package. We also show how to use the created object 
#
import os
import sys
import math

# Fisrt, we add the location of the library to test to the PYTHON path
#print os.getcwd()
cwd = "/projects/academic/alexeyak/ekadashi/libracode-dev/libracode-code/_build" # "/home/Alexey_2/Programming/Project_libra/_build" #os.getcwd()
print "Current working directory", cwd
sys.path.insert(1,cwd+"/src/mmath")
sys.path.insert(1,cwd+"/src/context")


print "\nTest 1: Importing the library and its content"
from libmmath import *
from libcontext import *

def read_qe_wfc(filename, upper_tag):
##
# This function reads an ASCII/XML format file contaiing wavefunction
# and returns the coefficients of the plane wave that constitute the
# wavefunction
#
# \param[in] filename This is the name of the file we will be reading to construct a wavefunction
#
#
    ctx = Context(filename)
    ctx.set_path_separator("/")
    print "path=", ctx.get_path()
#    ctx.save_xml("x.export/wfc1.xml")
    ctx.show_children(upper_tag)  # ("Kpoint.1") #

    ngw = int(float(ctx.get("Info/<xmlattr>/ngw","n")))
    nbnd = int(float(ctx.get("Info/<xmlattr>/nbnd","n")))
    print ngw, nbnd
    #sys.exit(0)
    coeff = CMATRIX(ngw,nbnd)
    #print coeff.show_matrix()
    #sys.exit(0)
    for band in range(1,nbnd+1):

        c = []
        all_coeff = ctx.get("Wfc."+str(band), "n").split(',')
        sz = len(all_coeff)

        for i in xrange(sz):
            a = all_coeff[i].split()
            for j in xrange(len(a)):
                c.append(a[j])
        sz = len(c)
        n = sz/2  # this should be equal to ngw


        for i in xrange(n):
            coeff.set(i, band-1, float(c[2*i]), float(c[2*i+1]))

    return coeff
#sys.exit(0)

coeff_1 = read_qe_wfc("x0.export/wfc.1", "Kpoint.1")
coeff_2 = read_qe_wfc("x0.export/wfc.1", "Kpoint.1")

nbnd = coeff_1.num_of_cols
print "nbnd = ",nbnd
#ovlp_1 = CMATRIX(nbnd, nbnd)
#ovlp_2 = CMATRIX(nbnd, nbnd)
#ovlp_12 = CMATRIX(nbnd, nbnd)
#print ovlp_1.show_matrix()
#ovlp_1 = coeff_1.T() * coeff_1
#ovlp_2 = coeff_1.T() * coeff_1

#print coeff_1.H().show_matrix()

#ovlp_2 = coeff_2.H() * coeff_2
#ovlp_12 = coeff_1.H() * coeff_2

ovlp_1  = CMATRIX(nbnd, nbnd)
ovlp_2  = CMATRIX(nbnd, nbnd)
ovlp_12 = CMATRIX(nbnd, nbnd)

ovlp_1  = coeff_1.H() * coeff_1
ovlp_2  = coeff_2.H() * coeff_2
ovlp_12 = coeff_1.H() * coeff_2

print ovlp_1.show_matrix()

##
# Print diagonal elements of overlap matrixes
for n in xrange(nbnd):
    print n, ovlp_1.get(n,n),ovlp_2.get(n,n),ovlp_12.get(n,n)





