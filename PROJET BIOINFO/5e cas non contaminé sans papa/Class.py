import pandas as pd


class Patient:

    #Mettre attributs pour ecriture log

    def __init__(self,marqueur,allele,hauteur,informatif):
        self.marqueur = marqueur
        self.allele = allele
        self.hauteur = hauteur
        self.informatif = informatif

    def allele_semblable(self,mere):
        Similarite = 0
        Semblable = False
        for Allele in range(3):
            if str(self.allele[Allele]) in mere.allele and str(self.allele[Allele]) != 0.0:
                Similarite = Similarite + 1
            if Similarite == 2:
                Semblable = True
        return Semblable


    ## Revoir contamination homozygote
    def verif_homozygote_contamine(self,mere,Semblable):
        Allele_different = None
        Allele_semblable = None
        if Semblable == True:
            for Allele in range(3):
                if str(self.allele[Allele]) in mere.allele and str(self.allele[Allele]) != 0.0:
                    Allele_semblable = Allele
                if str(self.allele[Allele]) != str(mere.allele[Allele]):
                    Allele_different = Allele
                if str(self.allele[Allele]) == str(mere.allele[Allele]) and str(self.allele[Allele]) != 0.0:
                    Allele_semblable = Allele
            if self.hauteur[Allele_different] < 1/3 * self.hauteur[Allele_semblable]:
                self.contamination = "contamine"
                #contamination_homozygote(self)
        else:
            pass

    def echo(self,foetus):
        Echo = False
        Allele_semblable = None
        for Allele in range(3):
            if str(self.allele[Allele]) in foetus.allele and str(self.allele[Allele]) != 0.0:
                Allele_semblable = Allele
        if Allele_semblable == 0:
            Allele_Echo = self.allele[Allele_semblable + 1]
            for Alleles_foetus in range(3):
                if float(foetus.allele[Alleles_foetus]) - 1 == Allele_Echo:
                    Echo = True
        else:
            Allele_Echo = self.allele[Allele_semblable - 1]
            for Alleles_foetus in range(3):
                if float(foetus.allele[Alleles_foetus]) - 1 == float(Allele_Echo):
                    Echo = True
        return Echo

class Mere(Patient):

    def __init__(self,marqueur,allele,hauteur,informatif,homozygote):
        super().__init__(marqueur,allele,hauteur,informatif)
        self.homozygote = homozygote

    def homozygotie(self):
        if "nan" in str(self.allele[1]):
            self.homozygote = True


class Foetus(Patient):

    def __init__(self,marqueur,allele,hauteur,informatif,echo,semblable,contamination):
        super().__init__(marqueur,allele,hauteur,informatif)
        self.echo = echo
        self.semblable = semblable
        self.contamination = contamination
    
    def foetus_3_pics(self):
        if "nan" not in str(self.allele):
            self.contamination = "contamine"
            #contamination_heterozygote(self)
        elif "nan" in str(self.allele[1]):
            return
            #foetus à un pic
        else:
            #if self.marqueur == 
            return
            #foetus à deux pics




class Pere(Patient):
    
    def __init__(self,marqueur,allele,hauteur,informatif):
        super().__init__(marqueur,allele,hauteur)


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

    Donnees_na = pd.read_table(data_frame,sep = '\t',header = 0)
    Donnees = Donnees_na.fillna(0)
    if (Donnees.shape[0] > 32):
        Iterateur = 3
    Allele = Donnees[["Allele 1","Allele 2", "Allele 3"]].values
    Hauteur = Donnees[["Height 1","Height 2", "Height 3"]].values
    for ligne in range(0,Donnees.shape[0] - 1,Iterateur):
        M = Mere(Donnees["Marker"][ligne],Allele[ligne],Hauteur[ligne],None,None)
        F = Foetus(Donnees["Marker"][ligne],Allele[ligne + 1],Hauteur[ligne + 1],None,None,None,None)
        if (Iterateur == 3):
            P = Patient(Donnees["Marker"][ligne],Allele[ligne + 2],Hauteur[ligne + 2],None)
            Donnees_Pere.append(P)
        Donnees_Mere.append(M)
        Donnees_Foetus.append(F)
    return Donnees_Mere, Donnees_Foetus,Donnees_Pere



if __name__ == "__main__":
    M,F,P = lecture_donnees("PP16_DMPK_MARTIN_061118_PP16.txt")
    verif_concordance(M,F)
    print(M[3].allele)
    print(F[3].allele)
    print(float(M[3].allele[1]) - 1)
    for i in range(1,16):
        A = M[i].echo(F[i])
        print(A)
    #machin= Mere("truc","all1",36,True)
    #print(machin.marqueur)
