import os
import sys
import math

from path_libra_lib import * # import path_libra_lib module
import main # import main module of the libra-QE-interface code


################ System-specific settings ########################
# For Alexey
libra_bin_path = "/projects/academic/alexeyak/alexeyak/libra-dev/libracode-code/_build/src" # set the path name to the source files in libracode
libra_qe_int_path = "/user/alexeyak/Programming/libra-qe_interface/src"
res_dir =  "/user/alexeyak/Programming/libra-qe_interface/run/res/"

# For Ekadashi
#libra_bin_path = "/projects/academic/alexeyak/ekadashi/libracode-dev/libracode-code/_build/src"
#libra_qe_int_path = "/projects/academic/alexeyak/ekadashi/devel/libra-qe_interface/src"
#res_dir = "/projects/academic/alexeyak/ekadashi/devel/libra-qe_interface/run/res/"


path_libra_lib(libra_bin_path)               # Path to the libra libraries
os.environ["src_path"] = libra_qe_int_path   # Path to the source code
sys.path.insert(1,os.environ["src_path"])    # Path to the source code



########## Setup all manual parameters here ####################

params = {}

params["scr_dir"]=os.environ['SLURTMDIR']
params["qe_inp0"] = "x.md.in"    # initial input file
params["qe_inp"] = "x.md_wrk.in" # working input file 
params["qe_out"] = "x.md.out"    # output file
params["nproc"] = 1              # the number of processors
params["dt_nucl"]=20.0  # time step for nuclear dynamics  ex) 20 a.u. = 0.5 fsec
params["Nsnaps"]=2      # the number of MD rounds
params["Nsteps"]=1      # the number of MD steps per snap
params["res"]=res_dir   # the directory where the energies and NACs files will be printed out
params["traj_file"] = params["res"]+"md.xyz"
params["ene_file"] = params["res"]+"ene.dat"


########### Now start actual calculations ###########################

main.main(params)  # run actual calculations

