class LignePatient:

    Marqueur = None
    Allele = []
    Hauteur = []

class Mere(LignePatient):

    Homozygote = False
    Semblable = False

class Foetus(LignePatient):

    Echo = False
    Semblable = False

class Pere(LignePatient):
    pass


print(Foetus.Echo)