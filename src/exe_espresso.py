#Script for running Quantum espresso
#
import os
import sys

def exe_espresso(params, a):
    print "i = ", a
    inp = params["qe_inp%i" % (a)]
    out = params["qe_out%i" %(a)]
    scr_dir = os.environ['SLURMTMPDIR']
    os.system("srun pw.x <%s> %s" % (inp,out))

#   Delete scratch directory and unecessary files
    os.system("rm *.dat *.wfc* *.igk* *.mix*")
    #os.system("rm -r *.save")

