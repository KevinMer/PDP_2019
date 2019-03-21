import pandas as pd

<<<<<<< HEAD

class LignePatient:
=======
class Patient:
>>>>>>> e447102f82121aee59cec9917280a5a761e1e187

    def __init__(self,marqueur,allele,hauteur):
        self.marqueur = marqueur
        self.allele = allele
        self.hauteur = hauteur

class Mere(Patient):

    def __init__(self,marqueur,allele,hauteur,homozygote):
        super().__init__(marqueur,allele,hauteur)
        self.homozygote = homozygote


class Foetus(Patient):

    def __init__(self,marqueur,allele,hauteur,echo,semblable,contamination):
        super().__init__(marqueur,allele,hauteur)
        self.echo = echo
        self.semblable = semblable
        self.contamination = contamination

class Pere(Patient):
    def __init__(self,marqueur,allele,hauteur):
        super().__init__(marqueur,allele,hauteur)

<<<<<<< HEAD
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
=======
def verif_concordance(mere,foetus):
    Taille = 16
    Concordance = 0
    for Alleles in range(Taille):
        for Allele_Foe in range(3):
            if foetus[Alleles].allele[Allele_Foe] in mere[Alleles].allele:
                Concordance = Concordance + 1
                break
                #Garder en memoire a quelle ligne ce n'est pas concordant
    ecriture_log(Concordance)
    return Concordance

def ecriture_log(concordance):
    Log = open("Log.txt","w")
    Log.write("DPN3000\njeudi 21 Mars\nVersion 1.0\n")
    if concordance == 16:
        Log.write("Concordance OK\n")
    else:
        Log.write("Concordance PAS OK")
    Log.close()

def lecture_donnees(data_frame):
    #Differentier csv, txt -> regex
    Iterateur = 2
    Donnees_Mere = []
    Donnees_Foetus = []
    Donnees_Pere = []

    Donnees = pd.read_table(data_frame,sep = '\t',header = 0)
    if (Donnees.shape[0] > 32):
        Iterateur = 3
    Allele = Donnees[["Allele 1","Allele 2", "Allele 3"]].values
    Hauteur = Donnees[["Height 1","Height 2", "Height 3"]].values
    for ligne in range(0,Donnees.shape[0] - 1,Iterateur):
        M = Patient(Donnees["Marker"][ligne],Allele[ligne],Hauteur[ligne])
        F = Patient(Donnees["Marker"][ligne],Allele[ligne + 1],Hauteur[ligne + 1])
        if (Iterateur == 3):
            P = Patient(Donnees["Marker"][ligne],Allele[ligne + 2],Hauteur[ligne + 2])
            Donnees_Pere.append(P)
        Donnees_Mere.append(M)
        Donnees_Foetus.append(F)
    return Donnees_Mere, Donnees_Foetus,Donnees_Pere

def foetus_3_pics(foetus):
    Taille = 16
    for Alleles in range(Taille):
        if "nan" not in str(foetus[Alleles].allele):
            foetus[Alleles] = Foetus(foetus[Alleles].marqueur,foetus[Alleles].allele,foetus[Alleles].hauteur,False,False,"contamine")
        else:
            foetus[Alleles] = Foetus(foetus[Alleles].marqueur,foetus[Alleles].allele,foetus[Alleles].hauteur,False,False,"pas_contamine")


if __name__ == "__main__":
    M,F,P = lecture_donnees("181985_xfra_ja_200618_PP16.txt")
    verif_concordance(M,F)
    foetus_3_pics(F)
    for i in range(16):
        print(F[i].contamination)
    #machin= Mere("truc","all1",36,True)
    #print(machin.marqueur)
>>>>>>> e447102f82121aee59cec9917280a5a761e1e187
