import os
import sys
import math


libra_bin_path = "/projects/academic/alexeyak/ekadashi/libracode-dev/libracode-code/_build/src"
libra_espresso_int_path = "/projects/academic/alexeyak/ekadashi/devel/libra-qe_interface/src"
# Path the the source code
# sys.path.insert(1,"/projects/academic/alexeyak/kosukesa/dev/libra-gamess_interface/src")
os.environ["src_path"] = libra_espresso_int_path
sys.path.insert(1,os.environ["src_path"])    # path to the source code
#sys.path.insert(1,"/projects/academic/alexeyak/ekadashi/dev/libra-qe_interface/src")

cwd = "/projects/academic/alexeyak/ekadashi/libra-dev/libracode-code"
print "Using the Libra installation at", cwd
#sys.path.insert(1,cwd+"/_build/src/mmath")
#sys.path.insert(1,cwd+"/_build/src/qchem")
#sys.path.insert(1,cwd+"_build/src/dyn")
#sys.path.insert(1,cwd+"_build/src/chemobjects")
#sys.path.insert(1,cwd+"_build/src/hamiltonian")


########## Setup all manual parameters here ####################

params = {}

params["scr_dir"]=os.environ['SLURMTMPDIR']
#params["gms_inp0"] = "H2O.inp"    # initial input file
#params["gms_inp"] = "H2O_wrk.inp" # working input file 
#params["gms_out"] = "H2O.out"  # output file
params["qe_inp0"] = "x.md.in"    # initial input file
params["qe_inp"] = "x.md_wrk.in" # working input file 
params["qe_out"] = "x.md.out"  # output file
params["nproc"] = 1             # the number of processors
params["basis_option"]=2 # ab initio or Semi-Empirical calculation?  Options: \"ab_initio\" = 1 , \"semi_empirical\" = 2
params["dt_nucl"]=20.0  # time step for nuclear dynamics  ex) 20 a.u. = 0.5 fsec
params["Nsnaps"]=2  # the number of MD rounds
params["Nsteps"]=1  # the number of MD steps per snap
params["res"]="/projects/academic/alexeyak/ekadashi/devel/libra-qe_interface/run/res/" # the directory where the energies and NACs files will be printed out
params["traj_file"] = params["res"]+"md.xyz"
params["ene_file"] = params["res"]+"ene.dat"


################################################################

from path_libra_lib import * # import path_libra_lib module
path_libra_lib(libra_bin_path) # Path to the libra libraries


import main        # import main module of the libra-Gamess-interface code

main.main(params)  # run actual calculations

