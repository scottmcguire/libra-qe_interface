# Libra-QuantumEspresso_interface

   Getting started with libra-QE interface
## Required softwares
   Libra and Quantum Espresso
   >Download and install [Libra] and [Quantum Espresso]  <br/>
   >Instructions for Libra installation are provided in Libra website [link1].

## Clone or Download libra-qe_interface
   You can download ZIP file in to your computer or clone entire folder in to your local working directory.
   > For cloning, Copy path to clipboard, then go to your local working directory and type <br/>
   > git clone path-of-libra-qe_interface <br/>

## Working with Libra-QuantumEspresso interface
   Go to libra-qe_interface. In this directory, you will find "src" and "run" folders.
 - src : Where all the source codes are placed. You don't need to change any files in this directory. If new updates are
         available, git pull will automatically update it.
 - run : Contains submission and run scripts. System specific details can be provided in the run_qe.py script. 

### Step-by-Step
1. Copy run to a working directory, name it as you like, say run0
2. Edit run_qe.py script as required.
3. Edit x_i.scf.in,x_i.exp.in files, which are Quantum espresso input file for
   SCF and wavefunction export calculations respectively.
4. submit submit_templ_qe.slm submission script. If it is a small calculation, you can run on the head
   node by just "python run_qe.py"

  
----------------------------------------------
----------------------------------------------
# Libra-GAMESS_interface
   
   This file introduces how to execute Libra-GAMESS_interface.

0. Install Libra and GAMESS on your PC or server.
   For installation, access the websites below:
    Libra:  http://www.acsu.buffalo.edu/~alexeyak/libra/index.html
   GAMESS:  http://www.msg.ameslab.gov/gamess/

1. Create a working directory,say, /home/work . 

2. There, create input files(*.inp).(H2O.inp and 23waters.inp in ".../libra-gamess_interface/run" are the simple examples.)
   For more details about how to create that, 
   please see the website http://www.msg.ameslab.gov/gamess/GAMESS_Manual/input.pdf .
   Here, Keep in mind 3 things.
   A. Only semi-empirical methods have been connected to libra so far;
      set GBASIS=MNDO, AM1, PM3, or RM1 in $BASIS section. 
   B. Set RUNTYP=GRADIENT in $CONTROL section.
   C. Use cartesian coordinates in $DATA section like this:

      Cn 1

      C  6.000000 4.377921 -4.769170 -2.758971
      C  6.000000 3.858116 -4.331728 -3.995136
      C  6.000000 2.478331 -4.387937 -4.267327
                           .
                           .
                           .
   
   * set blank line between "Cn 1" and 1st coordinate line.

3. For convinience, copy run_gms.py in ".../libra-gamess_interface/run" to the working place.

4. Modify copied run_gms.py for calculation.
   Concretely, set variables for GAMESS, Molecular Dynamics(MD), excited electron dynamics, and debugs.
   See the input manual in ".../libra-gamess_interface/run" to know more about the variables.

5. copy elements.txt in ".../libra-gamess_interface/run" to the working directory.

6. Create "res" and "sd_ham" directories under the working place, where the results will be output.

7. When the precedures above are finished, it is the time to execute this program.
   Here, 2 types of execution can be used.
   A. Only invoke "python run_gms.py" in the working place.
   B. Use queuing system. submit_templ_gms.lsf or submit_templ_gms.slurm in ".../libra-gamess_interface/run" are the simple examples for using this.
      Modify the files following your queuing system.   
   
8. After the calculation finished, the results will be set in "res" directory.

[Quantum Espresso]: <http://www.msg.ameslab.gov/gamess/>
[Libra]: <http://www.acsu.buffalo.edu/~alexeyak/libra/index.html>
[link1]: <http://www.acsu.buffalo.edu/~alexeyak/libra/installation.html>
