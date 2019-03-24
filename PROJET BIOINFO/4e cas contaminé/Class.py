import pandas as pd
import numpy as np


class Patient:

    # Mettre attributs pour ecriture log

    def __init__(self, marqueur, allele, hauteur, informatif):
        self.marqueur = marqueur
        self.allele = allele
        self.hauteur = hauteur
        self.informatif = informatif

    def allele_semblable(self, mere):
        # /!\ ne pas passer la première ligne
        Similarite = 0
        Semblable = False
        for Allele in range(3):
            if self.allele[Allele] in mere.allele and self.allele[Allele] != 0.0:
                Similarite = Similarite + 1
            if Similarite == 2:
                self.informatif = 2
        return Semblable

    # Revoir contamination homozygote
    def verif_homozygote_contamine(self, mere, Semblable):
        Allele_different = None
        Allele_semblable = None
        if Semblable == True:
            for Allele in range(3):
                if self.allele[Allele] in mere.allele and self.allele[Allele] != "0":
                    Allele_semblable = Allele
                if self.allele[Allele] != mere.allele[Allele]:
                    Allele_different = Allele
                if self.allele[Allele] == mere.allele[Allele] and self.allele[Allele] != "0":
                    Allele_semblable = Allele
            if self.hauteur[Allele_different] < 1/3 * self.hauteur[Allele_semblable]:
                self.contamination = "contamine"
                # contamination_homozygote(self)
        else:
            pass

    def echo(self, foetus):
        Echo = False
        Allele_semblable = None
        for Allele in range(3):
            if self.allele[Allele] in foetus.allele and self.allele[Allele] != 0.0:
                Allele_semblable = Allele
        if Allele_semblable == 0:
            Allele_Echo = self.allele[Allele_semblable + 1]
            for Alleles_foetus in range(3):
                if foetus.allele[Alleles_foetus] - 1 == Allele_Echo:
                    foetus.informatif = 3
        elif Allele_semblable == 1:
            Allele_Echo = self.allele[Allele_semblable - 1]
            for Alleles_foetus in range(3):
                if foetus.allele[Alleles_foetus] - 1 == Allele_Echo:
                    foetus.informatif = 3
        return Echo


class Mere(Patient):

    def __init__(self, marqueur, allele, hauteur, informatif, homozygote):
        super().__init__(marqueur, allele, hauteur, informatif)
        self.homozygote = homozygote

    def homozygotie(self):
        reponse = False
        if self.allele[1] == 0.0:
            self.homozygote = True
            reponse = True
        return reponse


class Foetus(Patient):

    def __init__(self, marqueur, allele, hauteur, informatif, echo, semblable, contamination,taux):
        super().__init__(marqueur, allele, hauteur, informatif)
        self.echo = echo
        self.semblable = semblable
        self.contamination = contamination
        self.taux = taux

    def foetus_pics(self):
        pic = 0
        if 0.0 not in self.allele:
            self.contamination = 2
            pic = 3
            # contamination_heterozygote(self)
        elif 0.0 == self.allele[1]:
            pic = 1
            # foetus à un pic
        else:
            pic = 2
            # if self.marqueur ==
            # foetus à deux pics
        return pic

    def contamination_heterozygote(self,mere):
        hauteur_allele_contaminant = 99999999999999999.0
        hauteur_allele_different = None
        taux_contamination = 0
        for allele in range(3):
            if self.allele[allele] < hauteur_allele_contaminant:
                hauteur_allele_contaminant = self.hauteur[allele]
        for alleles in range(3):
            if self.allele[alleles] not in mere.allele:
                hauteur_allele_different = self.hauteur[alleles]
        taux_contamination = ((hauteur_allele_contaminant) / (hauteur_allele_different + hauteur_allele_contaminant)) * 100
        self.taux = taux_contamination
        


class Pere(Patient):

    def __init__(self, marqueur, allele, hauteur, informatif):
        super().__init__(marqueur, allele, hauteur,informatif)


def ecriture_log(concordance,liste_F):
    Log = open("Log.txt", "w")
    Log.write("DPN3000\njeudi 21 Mars\nVersion 1.0\nEchantillon")
    if concordance == 16:
        Log.write("Concordance OK\n")
    else:
        Log.write("Concordance PAS OK")
        Log.close()
    for nbres in range(len(liste_F)):
        if F[nbres].informatif == 0:
            Log.write("Le marqueur {} est NON INFORMATIF car la mère est homozygote.".format(F[nbres].marqueur))
            Log.write("\n")
        elif F[nbres].informatif == 1:
            if F[nbres].contamination == 0:
                Log.write("Le marqueur {} est NON CONTAMINE".format(F[nbres].marqueur))
                Log.write("\n")
            elif F[nbres].contamination == 1:
                Log.write("Le marqueur {} est HMZ CONTAMINE".format(F[nbres].marqueur))
                Log.write("\n")
            else:
                Log.write("Le marqueur {} est HTZ CONTAMINE à hauteur de {} %".format(F[nbres].marqueur,F[nbres].taux))
                Log.write("\n")
        elif F[nbres].informatif == 2:
            Log.write("Le marqueur {} est NON INFORMATIF car le foetus et la mère possèdent les mêmes allèles.".format(F[nbres].marqueur))
            Log.write("\n")
        else:
            Log.write("Le marqueur {} est NON INFORMATIF car dans l'écho".format(F[nbres].marqueur))
            Log.write("\n")
    Log.write("Processus achevé.")
    Log.close()
#CODE Infor:
# 0 Mere HMZ
# 1 Informatif
# 2 Memes Alleles
# 3 Echo

#CODE CONTA:
# 0 Pas conta
# 1 HMZ Conta
# 2 HTZ Conta







def lecture_fichier(path_data_frame):
    # Differentier csv, txt -> regex
    Iterateur = 2
    Donnees_Mere = []
    Donnees_Foetus = []
    Donnees_Pere = []
    Donnees_na = pd.read_table(path_data_frame, sep='\t', header=0)
    Donnees = Donnees_na.replace(np.nan, 0.0, regex=True)
    if (Donnees.shape[0] > 32):
        Iterateur = 3
    Allele_na = Donnees[["Allele 1", "Allele 2", "Allele 3"]].values
    Hauteur_na = Donnees[["Height 1", "Height 2", "Height 3"]].values
    Allele, Hauteur = homogeneite_type(Allele_na, Hauteur_na)
    for ligne in range(0, Donnees.shape[0] - 1, Iterateur):
        M = Mere(Donnees["Marker"][ligne], Allele[ligne],
                 Hauteur[ligne], None, None)
        F = Foetus(Donnees["Marker"][ligne], Allele[ligne + 1],
                   Hauteur[ligne + 1], None, None, None, None,None)
        if (Iterateur == 3):
            P = Patient(Donnees["Marker"][ligne],
                        Allele[ligne + 2], Hauteur[ligne + 2], None)
            Donnees_Pere.append(P)
        Donnees_Mere.append(M)
        Donnees_Foetus.append(F)
    return Donnees_Mere, Donnees_Foetus, Donnees_Pere


def homogeneite_type(list_allele: list, list_hauteur: list) -> tuple:
    """
    docstring here
        :param list_allele:
        :param list_hauteur:
    """
    Allele = []
    Hauteur = []
    Allele.append(list_allele[0])
    Allele.append(list_allele[1])
    Hauteur.append(list_hauteur[0])
    Hauteur.append(list_hauteur[1])
    for i in range(2, len(list_allele)):
        Al = []
        Ht = []
        for j in range(3):
            Al.append(float(list_allele[i][j]))
            Ht.append(float(list_hauteur[i][j]))
        Allele.append(Al)
        Hauteur.append(Ht)
    return Allele, Hauteur

def verif_concordance(mere, foetus):
        Taille = 16
        concordance = 0
        for Alleles in range(Taille):
            for Allele_Foe in range(3):
                if foetus[Alleles].allele[Allele_Foe] in mere[Alleles].allele:
                    concordance = concordance + 1
                    break
                    # Garder en memoire a quelle ligne ce n'est pas concordant
        return concordance

def traitement_donnees(mere,foetus):
    concordance = verif_concordance(mere,foetus)
    if concordance != 16:
        return
        #echantillon non conforme
    else:
        for nbre_lignes in range(len(foetus)):
            nbre_pics = foetus[nbre_lignes].foetus_pics()
            if nbre_pics == 3:
                foetus[nbre_lignes].informatif = 1
                print("Le marqueur ",foetus[nbre_lignes].marqueur," est", foetus[nbre_lignes].contamination)
                foetus[nbre_lignes].contamination_heterozygote(mere[nbre_lignes])
                print("Le taux de contamination est",foetus[nbre_lignes].informatif,"taux =",foetus[nbre_lignes].contamination," %")
                print("\n")
            elif nbre_pics != 3:
                mere[nbre_lignes].homozygotie()
                if mere[nbre_lignes].homozygote:
                    mere[nbre_lignes].informatif = 0
                    foetus[nbre_lignes].informatif = 0
                    print("Le marqueur ", mere[nbre_lignes].marqueur, " est", mere[nbre_lignes].informatif)
                    print("\n")
                elif nbre_pics == 2:
                    foetus[nbre_lignes].allele_semblable(mere[nbre_lignes])
                    if foetus[nbre_lignes].informatif == 2:
                        print("Allele Semblable")
                        print("Contamination homozygote à paramétrer")
                        print("\n")
                    mere[nbre_lignes].echo(foetus[nbre_lignes])
                    if foetus[nbre_lignes].informatif == 3:
                        mere[nbre_lignes].informatif = 3
                        print("Le marqueur ", mere[nbre_lignes].marqueur, " est", mere[nbre_lignes].informatif)
                        print("\n")
                    mere[nbre_lignes].informatif = 1
                    foetus[nbre_lignes].informatif = 1
                    print("Le marqueur ", mere[nbre_lignes].marqueur, " est", mere[nbre_lignes].informatif)
                    print("\n")
                    if nbre_pics == 1:
                        mere[nbre_lignes].echo(foetus[nbre_lignes])
                        if foetus[nbre_lignes].informatif == 3:
                            mere[nbre_lignes].informatif = 3
                            print("Le marqueur ", mere[nbre_lignes].marqueur, " est", mere[nbre_lignes].informatif)
                            print("\n")
                        mere[nbre_lignes].informatif = 1
                        foetus[nbre_lignes].informatif = 1
                        print("Le marqueur ", mere[nbre_lignes].marqueur, " est", mere[nbre_lignes].informatif)
                        print("\n")
    ecriture_log(concordance,foetus)
#11 12
#8 12
def traitement_donnees_2(mere,foetus):
    concordance = verif_concordance(mere,foetus)
    if concordance != 16:
        return
    else:
        for nbre_lignes in range(1,len(mere)):
            pic = foetus[nbre_lignes].foetus_pics()
            mere[nbre_lignes].homozygotie()
            foetus[nbre_lignes].allele_semblable(mere[nbre_lignes])
            mere[nbre_lignes].echo(foetus[nbre_lignes])
            if pic == 3:
                foetus[nbre_lignes].contamination_heterozygote(mere[nbre_lignes])
                foetus[nbre_lignes].informatif = 1
                foetus[nbre_lignes].contamination = 2
            elif mere[nbre_lignes].homozygote:
                foetus[nbre_lignes].informatif = 0
            elif pic == 2:
                #foetus[nbre_lignes].allele_semblable(mere[nbre_lignes])
                if foetus[nbre_lignes].informatif == 2:
                    print("Contamination HMZ à faire")
                    print(foetus[nbre_lignes].informatif)
                    #mere[nbre_lignes].echo(foetus[nbre_lignes])
                else:
                    if foetus[nbre_lignes].informatif != 3:
                        foetus[nbre_lignes].informatif = 1
                        foetus[nbre_lignes].contamination = 0
            else:
                if foetus[nbre_lignes].informatif != 3:
                    foetus[nbre_lignes].informatif = 1
                    foetus[nbre_lignes].contamination = 0
    ecriture_log(concordance,foetus)
        

#CODE Infor:
# 0 Mere HMZ
# 1 Informatif
# 2 Memes Alleles
# 3 Echo

#CODE CONTA:
# 0 Pas conta
# 1 HMZ Conta
# 2 HTZ Conta




if __name__ == "__main__":
    #/!\ penser à mettre contamination pour mère
    M, F, P = lecture_fichier("181985_xfra_ja_200618_PP16.txt")
    traitement_donnees_2(M,F)
    # print(M[2].echo(F[2]))
    #for i in range(16):
     #   M[i].homozygotie()
      #  print(M[i].homozygote)
    #machin= Mere("truc","all1",36,True)
    # print(machin.marqueur)
