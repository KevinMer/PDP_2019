class LignePatient:

    def __init__(self,marqueur,allele,hauteur):
        self.marqueur = marqueur
        self.allele = allele
        self.hauteur = hauteur

class Mere(LignePatient):

    def __init__(self,marqueur,allele,hauteur,homozygote):
        super().__init__(marqueur,allele,hauteur)
        self.homozygote = False


class Foetus(LignePatient):

    def __init__(self,marqueur,allele,hauteur,echo,semblable,contamination):
        super().__init__(marqueur,allele,hauteur)
        self.echo = False
        self.semblable = False
        self.contamination = "pas_contamine"

class Pere(LignePatient):
    def __init__(self,marqueur,allele,hauteur):
        super().__init__(marqueur,allele,hauteur)

if __name__ == "__main__":
    machin= Mere("truc","all1",36,True)
    print(machin.marqueur)
