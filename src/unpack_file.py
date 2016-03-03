# Defining what information to extract and store in the dictionary
#
import os
import sys
import math
#
def unpack_file(filename):
    f_qe = open(filename,"r")
    l_qe = f_qe.readlines()
    f_qe.close()

    data = {}    #creating empty dictionary

    N = len(l_qe)
    for i in range(0,N):
        s = l_qe[i].split()
        if len(s) > 0 and s[0] == "ATOMIC_POSITIONS":
            icoord = i
            break
    for i in range(0,N):
        s = l_qe[i].split()
        if len(s) > 0 and s[0] == "Forces" and s[1] == "acting":
            iforce = i
            break

    #Printing coordinate lines
    for i in xrange(icoord+1,icoord+7):
        print l_qe[i]
    #Reading atoms and xyz coordinates and writing into dictionary
    l_atoms = []
    coord_atoms = []
    for i in range(icoord+1,icoord+7):
        spline = l_qe[i].split()
        # specific atom
        l_atoms.append(spline[0])
        # atom coordinate
        coord = []
        for j in range(1,4):
            coord.append(float(spline[j]))
        coord_atoms.append(coord)

    data["l_atoms"] = l_atoms
    data["coord_atoms"] = coord_atoms
    print "l_atoms=", data["l_atoms"]
    print "coord_atoms=", data["coord_atoms"]
           
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



