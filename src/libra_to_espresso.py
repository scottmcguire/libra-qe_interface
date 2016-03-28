def libra_to_espresso(data, params, mol):
##
# Creates quantum espresso input from libra output
#
#
    qe_inp_templ = params["qe_inp_templ"]
    qe_inp = params["qe_inp"]
    #
    cell_dm = params["cell_dm"]
 
    g = open(qe_inp, "w")    # open input file

    # Write control section
    tl = len(qe_inp_templ)
    for i in xrange(tl):
        g.write(qe_inp_templ[i])

    # Creating empty line
    g.write("\n")

    # Write atom name and coordinatess
    Natoms = len(data["l_atoms"])
    #B_to_A = 0.529177208    # Bohr to Angstrom conversion
    B_to_A = 1/cell_dm   # Bohr to Angstrom conversion
    for i in xrange(Natoms):
        atms = data["l_atoms"][i]
        x = B_to_A*mol.q[3*i]
        y = B_to_A*mol.q[3*i+1]
        z = B_to_A*mol.q[3*i+2]
        g.write("%s    %12.7f    %12.7f    %12.7f  \n"  % (atms, x, y, z) )

    g.write(" $END \n")
    g.close()


