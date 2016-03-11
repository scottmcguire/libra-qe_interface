#Script for running Quantum espresso
#
import os
import sys

def exe_espresso(param):
    inp = param["qe_inp"]
    out = param["qe_out"]
    scr_dir = os.environ['SLURMTMPDIR']
    os.system("srun pw.x <%s> %s" % (inp,out))

#   Delete scratch directory and unecessary files
    os.system("rm *.dat *.wfc* *.igk* *.mix*")
    
    os.system("rm -r x.save")

