#
def read_qe_inp_templ(inp_filename):
##
# Add the function documentation here...
#

    f = open(inp_filename,"r")
    templ = f.readlines()
    f.close()

    N = len(templ)
    for i in range(0,N):
        s = templ[i].split()
        if len(s) > 0 and s[0] == "ATOMIC_POSITIONS":
            ikeep = i
            break

    templ[ikeep+1:N] = []
    for i in xrange(ikeep+1):
        print templ[i]

    return templ

