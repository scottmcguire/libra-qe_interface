##
#
def excited_state(params, el):

    nband = params["nband"]
    homo = params["HOMO"]
    excitations = []
    for em in range(0,nband):
        excitations.append(0) # creating empty bands
    for em in range(0,homo):     # ground state occupations
        excitations[em] = 2  

    if el > 0: # consider excited states
    ##
    # Single excitations are considered from HOMO to LUMO + i
        for emx in range(homo-1,homo-1+el+1,el):
            excitations[emx] = 1

    return excitations
