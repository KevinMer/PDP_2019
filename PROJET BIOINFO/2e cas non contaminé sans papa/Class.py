import pandas as pd


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

def pere_ou_pas(data_frame):
    if data_frame.shape[0] > 32:
        return True
    else:
        return False

def concordance(data_frame,pere):
    Iterateur = 2
    if(pere):
        Iterateur = 3
    Alleles = data_frame[["Allele 1","Allele 2", "Allele 3"]].values
    for val in range(0,data_frame.shape[0] - 1,Iterateur):
        for allele in range(len(Alleles[val + 1])):
            if Alleles[val + 1][allele] not in Alleles[val]:
                print("Concordance")

        if Alleles[val] in Alleles[val + 1]:
            
            print("Ok")
        else:
            print("Pas concordant")


if __name__ == "__main__":
    donnees = pd.read_table("181985_xfra_ja_200618_PP16.txt",sep = '\t',header = 0)
    concordance(donnees,pere)
    machin= Mere("truc","all1",36,True)
    print(machin.marqueur)
