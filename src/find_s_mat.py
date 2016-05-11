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
import numpy

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
    #coeff = CMATRIX(ngw,nbnd)
    coeff = CMATRIX(ngw,3)
    #print coeff.show_matrix()
    #sys.exit(0)
    k = 0
    for band in [6,7,8]: #range(1,nbnd+1):

        c = []
        print "band=",band
        all_coeff = ctx.get("Wfc."+str(band), "n").split(',')
        sz = len(all_coeff)

        for i in xrange(sz):
            a = all_coeff[i].split()
            for j in xrange(len(a)):
                c.append(a[j])
        sz = len(c)
        n = sz/2  # this should be equal to ngw
        #n = sz

        for i in xrange(n):
            coeff.set(i, k, float(c[2*i]), float(c[2*i+1]))
            #coeff.set(i, band-1, float(c[2*i]), float(c[2*i+1]))
            #coeff.set(i, band-1, float(c[i]), float(c[i+1]))
        k = k+1
    nbnd = coeff.num_of_cols
    ngw = coeff.num_of_rows
    ovlp  = CMATRIX(nbnd, nbnd)
    ovlp  = coeff.H() * coeff

    for i in xrange(ngw):
        for j in [0,1,2]:
            coeff.set(i,j,(1/math.sqrt((ovlp.get(j,j)).real))*coeff.get(i,j))

    # This returns normalized coefficients of MO
    return coeff
#sys.exit(0)

def find_det(ovlp):

    deta = []
    for na in [0,1,2]: #range(5,7):
        detb = []
        for nb in [0,1,2]: #range(5,7):
            detb.append(ovlp.get(na,nb))
        deta.append(detb)
    detaa = numpy.linalg.det(deta)
    return detaa


def find_nac(params):
    dt = params["dt_nucl"]
    s01 = CMATRIX(3,3)
    s10 = CMATRIX(3,3)
    coeff_01 = params["coeff_0"]
    coeff_11 = params["coeff_1"]
    coeff_00 = params["coeff_old_0"]
    coeff_10 = params["coeff_old_1"]
    s01 = params["coeff_old_0"].H()*params["coeff_1"]
    s10 = params["coeff_0"].H()*params["coeff_old_1"]   
    ds01 = find_det(s01)
    ds10 = find_det(s10)
    print "ds01 = " , ds01 , "ds10 = " , ds10
    nac = (ds01-ds10)/(2.0*dt)
    print "nac = ",nac
    return nac




