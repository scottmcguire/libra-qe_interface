## \file unpack_file.py Defining what information to extract and store in the dictionary
#

import os
import sys
import math

def unpack_file(filename, cell_dm):
##
#  Function for reading and extracting quantum espresso
#  output. Extracted parameters are used in classical MD
#  calculation using LIBRA in the next step.
#
    f_qe = open(filename,"r")
    l_qe = f_qe.readlines()
    f_qe.close()

    data = {}    #creating empty dictionary

    N = len(l_qe)
    for i in range(0,N):
        s = l_qe[i].split()
        if len(s) > 0 and s[0] == "site"  and s[3] == "positions":
            icoord = i
            break
    for i in range(0,N):
        s = l_qe[i].split()
        if len(s) > 0 and s[0] == "Forces" and s[1] == "acting":
            iforce = i
            break
    # Extracting potential energy from QE
    for i in range(0,N):
        s  = l_qe[i].split()
        if len(s) > 0 and s[0] == "!" and s[1] == "total" and s[2] == "energy":
            data["tot_ene"] = float(s[4])
            break    

    #Printing coordinate lines
    for i in xrange(icoord+1,icoord+7):
        print l_qe[i]

    #Reading atoms and xyz coordinates and writing into dictionary
    l_atoms = []
    coord_atoms = []
#    A_to_B = data["cell_dm"]
#    A_to_B = data["tot_ene"]
    
    for i in range(icoord+1,icoord+7):
        spline = l_qe[i].split()

        # specific atom
        l_atoms.append(spline[1])

        # Convertingatom coordinate in Bohr, 1 Angstrom = 1.88973 Bohr
        #A_to_B = 1.88973
#        A_to_B = data["cell_dm"]
        coord = []
        for j in range(6,9):
            coord.append(cell_dm*(float(spline[j])))
        coord_atoms.append(coord)

    data["l_atoms"] = l_atoms
    data["coor_atoms"] = coord_atoms
    print "l_atoms=", data["l_atoms"]
    print "coor_atoms=", data["coor_atoms"]
           
    for i in xrange(iforce+1,iforce+10):
        print l_qe[i]

    #Detect and print Force
    force_atoms = []
    for i in range(iforce+4,iforce+10):
        spline = l_qe[i].split()
        # force acting on atoms
        force = []
        for j in range(6,9):
            force.append(float(spline[j]))
        force_atoms.append(force)

    data["force_atoms"] = force_atoms
    print "force_atoms=", data["force_atoms"]

    # return data["force_atoms"], data    
    return data["tot_ene"], data["force_atoms"], data    

