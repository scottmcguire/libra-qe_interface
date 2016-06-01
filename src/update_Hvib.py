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

import os
import sys
import math
import numpy

if sys.platform=="cygwin":
    from cyglibra_core import *
elif sys.platform=="linux" or sys.platform=="linux2":
    from liblibra_core import *



def find_det(A0,A1,n_mo):
##
# Find the ovelap between two wavefunction, designated by two coefficient matrix
# A0 and A1
# First the overlap matrix is constructed by A0.H()*A1
# Then the determinant of the matrix is calculated using linalg.det module of numpy library
# return determinant, detaa

    ovlp_01 = CMATRIX(n_mo,n_mo)
    ovlp_01 = A0.H()*A1

    deta = []
    for na in xrange(n_mo):    
        detb = []
        for nb in xrange(n_mo):   
            detb.append(ovlp_01.get(na,nb))
        deta.append(detb)
    detaa = numpy.linalg.det(deta)
    return detaa


def find_nac(A0,A1,Ao0,Ao1,dt,n_mo):
##
# \param[in] A0 one of the coefficient matrix of molecular orbital 0 at time t+dt
# \param[in] A1 one of the coefficient matrix of molecular orbital 1 at time t+dt
# \param[in] Ao0 one of the coefficient matrix of molecular orbital 0 at time t
# \param[in] Ao1 one of the coefficient matrix of molecular orbital 1 at time t
# \param[in] params["dt_nucl"] nuclear time step
# \param[in] params["num_MO"] number of molecular orbital included in the electronic basis set for the dynamics
# \param[out] nac Non-Adiabatic coupling between these two state 0 and 1 is returned as output

    ds_ab = find_det(Ao0,A1,n_mo)
    ds_ba = find_det(A0,Ao1,n_mo)
    nac = (ds_ab-ds_ba)/(2.0*dt)

    return nac

def update_H_vib(D_mat,E_mat,no_ex):
##
# Updates vibronic hamiltonian

    H_vib = CMATRIX(no_ex,no_ex)
    for i in xrange(no_ex):
            H_vib.set(i,i,E_mat.get(i,i))

    for i in xrange(no_ex):
        for j in xrange(no_ex):
            if j != i:
                H_vib.set(i,j,0.0,D_mat.get(i,j).imag)

    return H_vib

def update_E_mat(params):
##
# This is later termed as ham_adi
    no_ex = len(params["excitations"])
    E_mat = MATRIX(no_ex,no_ex)

    for i in xrange(no_ex):
        E_mat.set(i,i,params["epot%i"%i])

    return E_mat

def update_S_matrix(wfc,no_ex,n_mo):
##
# This updates overlap matrix
    S_mat = CMATRIX(no_ex,no_ex)
    for i in xrange(no_ex):
        for j in xrange(no_ex):
            S_mat.set(i,j,1.0)
            if j != i :
                detaa = find_det(wfc["coeff_%i"%i],wfc["coeff_%i"%j],n_mo)
                S_mat.set(i,j,detaa)

    return S_mat

def update_D_matrix(wfc,dt,no_ex,n_mo):
##
# Updates NACs
    D_mat = CMATRIX(no_ex,no_ex)  #no_ex being number of excited states
    for i in xrange(no_ex):
        for j in xrange(no_ex):
            if j != i :
                nac = find_nac(wfc["coeff_%i"%i],wfc["coeff_%i"%j],wfc["coeff_old_%i"%i],wfc["coeff_old_%i"%j],dt,n_mo)
                if i < j:
                    D_mat.set(i,j,-1.0*nac)
                else:
                    D_mat.set(i,j,nac)

    return D_mat
                                                 

def update_vibronic_hamiltonian(ham_adi, ham_vib, S_mat, wfc, params):
    ##
    # \param[out] ham_adi Electronic (adiabatic) Hamiltonian (MATRIX), diagonal energies
    # \param[out] ham_vib Vibronic Hamiltonian (CMATRIX)
    # \param[out] S_mat Overlap matrix (CMATRIX)
    # \param[in] params  contains the dictionary of the input parameters
    # \param[in] wfc dictionary containing wave function coefficients of MO basis
    #
    # Used in: md.py/run_MD
    # Update vibronic hamiltonian, S_matrix, ham_adi

    dt = params["dt_nucl"]
    no_ex = len(params["excitations"])
    n_mo = params["num_MO"]

    # Update S_mat the overlap matrix (CMATRIX)
    S_mat = update_S_matrix(wfc, no_ex, n_mo)

    # Update NAC matrix  (CMATRIX)
    D_mat = update_D_matrix(wfc,dt,no_ex,n_mo)

    # Update adiabatic hamiltonian (ham_adi)
    ham_adi = update_E_mat(params)

    #Update Vibronic hamiltonian  (CMATRIX)
    ham_vib = update_H_vib(D_mat,ham_adi,no_ex)

