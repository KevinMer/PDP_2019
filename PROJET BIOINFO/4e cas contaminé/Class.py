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
                Semblable = True
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
                    Echo = True
        elif Allele_semblable == 1:
            Allele_Echo = self.allele[Allele_semblable - 1]
            for Alleles_foetus in range(3):
                if foetus.allele[Alleles_foetus] - 1 == Allele_Echo:
                    Echo = True
        return Echo

    def verif_concordance(self, mere, foetus):
        Taille = 16
        concordance = 0
        for Alleles in range(Taille):
            for Allele_Foe in range(3):
                if foetus[Alleles].allele[Allele_Foe] in mere[Alleles].allele:
                    concordance = concordance + 1
                    break
                    # Garder en memoire a quelle ligne ce n'est pas concordant
        ecriture_log(concordance)
        return concordance


class Mere(Patient):

    def __init__(self, marqueur, allele, hauteur, informatif, homozygote):
        super().__init__(marqueur, allele, hauteur, informatif)
        self.homozygote = homozygote

    def homozygotie(self):
        self.homozygote = self.allele[1] == 0.0


class Foetus(Patient):

    def __init__(self, marqueur, allele, hauteur, informatif, echo, semblable, contamination):
        super().__init__(marqueur, allele, hauteur, informatif)
        self.echo = echo
        self.semblable = semblable
        self.contamination = contamination

    def foetus_pics(self):
        pic = 0
        if 0.0 not in self.allele:
            self.contamination = "contamine"
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


class Pere(Patient):

    def __init__(self, marqueur, allele, hauteur, informatif):
        super().__init__(marqueur, allele, hauteur,informatif)


def ecriture_log(concordance):
    Log = open("Log.txt", "w")
    Log.write("DPN3000\njeudi 21 Mars\nVersion 1.0\n")
    if concordance == 16:
        Log.write("Concordance OK\n")
    else:
        Log.write("Concordance PAS OK")
    Log.close()


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
                   Hauteur[ligne + 1], None, None, None, None)
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


if __name__ == "__main__":
    M, F, P = lecture_donnees("181836_xfra jb_200618_PP16.txt")
    # print(M[2].echo(F[2]))
    for i in range(16):
        M[i].homozygotie()
        print(M[i].homozygote)
    verif_concordance(M, F)
    #machin= Mere("truc","all1",36,True)
    # print(machin.marqueur)
