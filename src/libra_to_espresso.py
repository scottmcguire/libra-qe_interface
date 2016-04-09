import math

from excited_state import*


def libra_to_espresso(data, params, mol):
##
# Creates quantum espresso input from libra output
#
#
    no_ex = params["no_ex"]
  
    qe_inp_templ = params["qe_inp_templ"]
    for i in range(0, no_ex):
        qe_inp = params["qe_inp%i" %i]
        g = open(qe_inp, "w")    # open input file
        cell_dm = params["cell_dm"]

        # Write control section
        tl = len(qe_inp_templ)
        for j in xrange(tl):
            g.write(qe_inp_templ[j])

        # Creating empty line
        g.write("\n")

        # Write atom name and coordinatess
        Natoms = len(data["l_atoms"])
        #B_to_A = 0.529177208    # Bohr to Angstrom conversion
        B_to_A = 1/cell_dm   # Bohr to Angstrom conversion
        for k in xrange(Natoms):
            atms = data["l_atoms"][k]
            x = B_to_A*mol.q[3*k]
            y = B_to_A*mol.q[3*k+1]
            z = B_to_A*mol.q[3*k+2]
            g.write("%s    %12.7f    %12.7f    %12.7f  \n"  % (atms, x, y, z) )

        excitations = excited_state(params, i)

        # Single excitations with no spin-polarization calculation
        g.write("OCCUPATIONS"+'\n')
        count = 0
        for em in excitations:
            count = count +1
            if count % 10 ==0:
                g.write("%s " %em +'\n')
            elif count % 10 <= 10:
                g.write("%s " %em )
        g.write("\n")

        g.close()


