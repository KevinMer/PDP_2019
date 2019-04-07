import pandas as pd
import numpy as np


class Echantillon:

    def __init__(self,liste_lignes,seuil_nbre_marqueurs = 2,seuil_taux_conta = 0.05,conclusion = None):
        self.liste_lignes = liste_lignes
        self.seuil_nbre_marqueurs = seuil_nbre_marqueurs
        self.seuil_taux_conta = seuil_taux_conta
        self.conclusion = conclusion

    def conclusion_echantillon(self,liste_foetus):
        compteur = 0
        for lignes in range(1,len(liste_foetus)):
            if liste_foetus[lignes].contamination != 0 and liste_foetus[lignes].taux > self.seuil_taux_conta:
                compteur = compteur + 1
        if compteur > self.seuil_nbre_marqueurs:
            self.conclusion = 0
        else:
            self.conclusion = 1

class Patient:

    def __init__(self, marqueur, allele, hauteur, informatif):
        self.marqueur = marqueur
        self.allele = allele
        self.hauteur = hauteur
        self.informatif = informatif

    def allele_semblable(self, mere): 
        #Entree : une ligne du foetus, la ligne mère correspondante
        #Détermine si les allèles sont les mêmes
        #Si c'est le cas, l'attribut informatif de la ligne foetus se voit attribuer la valeur 2
        Similarite = 0
        for Allele in range(3):
            if self.allele[Allele] in mere.allele and self.allele[Allele] != 0.0:
                Similarite = Similarite + 1
        if Similarite == 2:
            self.informatif = 2
        
#CODE Informatif:
# 0 Mere HMZ
# 1 Informatif
# 2 Memes Alleles
# 3 Echo

#CODE Contamine:
# 0 Pas conta
# 1 HMZ Conta
# 2 HTZ Conta

#CODE Conclusion:

#0 : contamine
#1 : non contamine


    def echo(self, foetus):
        #Entree : une ligne de la mère, la ligne foetus correspondante
        #Détermine si il y a écho
        # Si oui, l'attribut "informatif" de la ligne foetus se voit attribuer la valeur 3
        Allele_semblable = 0
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


class Mere(Patient):

    def __init__(self, marqueur, allele, hauteur, informatif, homozygote):
        super().__init__(marqueur, allele, hauteur, informatif)
        self.homozygote = homozygote

    def homozygotie(self):
        #Entree : une ligne mère
        #Détermine si pour cette ligne la mère est homozygote
        #Si oui, l'attribut homozygote de la ligne mère se voit attribuer la valeur true
        if self.allele[1] == 0.0:
            self.homozygote = True


class Foetus(Patient):

    def __init__(self, marqueur, allele, hauteur, informatif, contamination,taux,sexe):
        super().__init__(marqueur, allele, hauteur, informatif)
        self.contamination = contamination
        self.taux = taux
        self.sexe = sexe

    def foetus_pics(self):
        #Entree : une ligne du foetus
        #Détermine le nombre de pics pour cette ligne
        #Retourne le nombre de pic
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
        #Entree : une ligne du foetus, la ligne mère correspondante
        #Calcul le pourcentage de contamination hétérozygote
        #L'attribut taux de la ligne foetus se voit attribuer le pourcentage correspondant
        hauteur_allele_contaminant = 99999999999999999.0
        hauteur_allele_different = None
        taux_contamination = 0
        for allele in range(3):
            if self.hauteur[allele] < hauteur_allele_contaminant:
                hauteur_allele_contaminant = self.hauteur[allele]
        for alleles in range(3):
            if self.allele[alleles] not in mere.allele:
                hauteur_allele_different = self.hauteur[alleles]
        taux_contamination = ((hauteur_allele_contaminant) / (hauteur_allele_different + hauteur_allele_contaminant)) * 100
        self.taux = round(taux_contamination,2)

    def verif_homozygote_contamine(self):
        seuil = 1/3
        if self.hauteur[0] < self.hauteur[1] * seuil or self.hauteur[1] < self.hauteur[0] * seuil:
            self.contamination = 1
            self.informatif = 1
        else:
            self.taux = 0.0

    def homozygote_contamine(self):
        seuil = 1/3
        if self.hauteur[1] < self.hauteur[0] * seuil:
            allele_contaminant = 1
            taux = ((2 * self.hauteur[allele_contaminant]) / (self.hauteur[allele_contaminant] + self.hauteur[0])) * 100
        else:
            allele_contaminant = 0
            taux = ((2 * self.hauteur[allele_contaminant]) / (self.hauteur[allele_contaminant] + self.hauteur[1])) * 100
        self.taux = round(taux,2)
    


class Pere(Patient):

    def __init__(self, marqueur, allele, hauteur, informatif):
        super().__init__(marqueur, allele, hauteur,informatif)


def resultat(concordance,liste_F,echantillon):
    #Entree : le resultat de la concordance, une liste contenant toutes les lignes du foetus
    #Ecrit dans un fichier texte la conclusion pour chaque marqueur respectif
    #Ne renvoie rien
    affichage = ""
    if concordance == 16:
        affichage = affichage + "Concordance OK\n"
    else:
        affichage = affichage + "Concordance PAS OK\n"
        return affichage
    if liste_F[0].sexe == "F":
        affichage = affichage + "Le foetus est de sexe féminin\n"
    else:
        affichage = affichage + "Le foetus est de sexe masculin\n"
    for nbres in range(1,len(liste_F)):
        if liste_F[nbres].informatif == 0:
            affichage = affichage + "Le marqueur " + str(liste_F[nbres].marqueur) + " est NON INFORMATIF car la mère est homozygote\n"
        elif liste_F[nbres].informatif == 1:
            if liste_F[nbres].contamination == 0:
                affichage = affichage + "Le marqueur " + str(liste_F[nbres].marqueur) + " est NON CONTAMINE\n"
            elif liste_F[nbres].contamination == 1:
                affichage = affichage + "Le marqueur " + str(liste_F[nbres].marqueur) + " est HMZ CONTAMINE à hauteur de " + str(liste_F[nbres].taux) + "%\n"
            else:
                affichage = affichage + "Le marqueur " + str(liste_F[nbres].marqueur) + " est HTZ CONTAMINE à hauteur de " + str(liste_F[nbres].taux) + "%\n"
        elif liste_F[nbres].informatif == 2:
            affichage = affichage + "Le marqueur " + str(liste_F[nbres].marqueur) + " est NON INFORMATIF car le foetus et la mère possèdent les mêmes allèles.\n"
        else:
            affichage = affichage + "Le marqueur " + str(liste_F[nbres].marqueur) + " est NON INFORMATIF car dans l'écho\n"
    if echantillon.conclusion == 0:
        affichage = affichage + "L'échantillon est contaminé\n"
    else:
        affichage = affichage + "L'échantillon n'est pas contaminé\n"
    return affichage
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
    #Entree : le fichier que l'on souhaite ouvrir
    #Lis le data frame et appelle les constructeurs correspondants pour chaque ligne (foetus,mère,père). Les instances sont stockées dans des listes distinces.
    #Retourne la listes des instances pour les lignes mère, foetus et père.
    # Differentier csv, txt -> regex
    Iterateur = 2
    Donnees_Mere = []
    Donnees_Foetus = []
    Donnees_Pere = []
    S_File_p = ""
    Donnees_na = pd.read_csv(path_data_frame, sep='\t', header=0)
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
                   Hauteur[ligne + 1], None, None, None,None)
        if (ligne<=2):
            S_File_m = Donnees["Sample File"][0]
            S_File_f = Donnees["Sample File"][1]
        if (Iterateur == 3):
            if (ligne<=2):
                S_File_p = Donnees["Sample File"][2]
            P = Patient(Donnees["Marker"][ligne],
                        Allele[ligne + 2], Hauteur[ligne + 2], None)
            Donnees_Pere.append(P)
        Donnees_Mere.append(M)
        Donnees_Foetus.append(F)
    Echantillon_F = Echantillon(F,2,0.05,None)
    return Donnees_Mere, Donnees_Foetus, Donnees_Pere,Echantillon_F, S_File_m, S_File_f, S_File_p


def homogeneite_type(list_allele, list_hauteur):
    #Entree : liste de tout les allèles du fichier, liste de toutes les hauteurs du fichier
    #Transforme toutes les valeurs, exceptées celles des deux premières lignes en float.
    #Retourne les listes d'allèles et de hauteurs nouvellement modifiées en float.
    iteration = 2
    Allele = []
    Hauteur = []
    Allele.append(list_allele[0])
    Allele.append(list_allele[1])
    Hauteur.append(list_hauteur[0])
    Hauteur.append(list_hauteur[1])
    if len(list_allele) > 32:
        iteration = 3
        Allele.append(list_allele[2])
        Hauteur.append(list_hauteur[2])
    for i in range(iteration, len(list_allele)):
        Al = []
        Ht = []
        for j in range(3):
            Al.append(float(list_allele[i][j]))
            Ht.append(float(list_hauteur[i][j]))
        Allele.append(Al)
        Hauteur.append(Ht)
    return Allele, Hauteur

def verif_concordance(mere, foetus):
    #Entree : la liste qui contient toutes les lignes de la mère, la liste qui contient toutes les lignes du foetus
    #Vérifie pour chaque position de la liste si un allèle est en commmun entre les deux listes. La concordance est incrémentée de 1 si c'est le cas.
    #Retourne la concordance.
        Taille = 16
        concordance = 0
        for Alleles in range(Taille):
            for Allele_Foe in range(3):
                if foetus[Alleles].allele[Allele_Foe] in mere[Alleles].allele:
                    concordance = concordance + 1
                    break
                    # Garder en memoire a quelle ligne ce n'est pas concordant
        return concordance


def traitement_donnees(mere,foetus,echantillon):
    #Entree : la liste qui contient toutes les lignes de la mère, la liste qui contient toutes les lignes du foetus
    #Chaine de traitement des informations permettant de mettre en place une conclusion.
    concordance = verif_concordance(mere,foetus)
    if concordance != 16:
        return
    else:
        if foetus[0].allele[1] == 0.0:
            foetus[0].sexe = "F"
        for nbre_lignes in range(1,len(mere)):
            pic = foetus[nbre_lignes].foetus_pics()
            mere[nbre_lignes].homozygotie()
            foetus[nbre_lignes].allele_semblable(mere[nbre_lignes])
            foetus[nbre_lignes].taux = 0.0
            if foetus[nbre_lignes].informatif != 2:
                mere[nbre_lignes].echo(foetus[nbre_lignes])
            if pic == 3:
                foetus[nbre_lignes].contamination_heterozygote(mere[nbre_lignes])
                foetus[nbre_lignes].informatif = 1
                foetus[nbre_lignes].contamination = 2
            elif mere[nbre_lignes].homozygote:
                foetus[nbre_lignes].informatif = 0
            elif pic == 2:
                if foetus[nbre_lignes].informatif == 2:
                    foetus[nbre_lignes].verif_homozygote_contamine()
                    if foetus[nbre_lignes].contamination == 1:
                        foetus[nbre_lignes].homozygote_contamine()
                else:
                    if foetus[nbre_lignes].informatif != 3:
                        foetus[nbre_lignes].informatif = 1
                        foetus[nbre_lignes].contamination = 0
            else:
                if foetus[nbre_lignes].informatif != 3:
                    foetus[nbre_lignes].informatif = 1
                    foetus[nbre_lignes].contamination = 0
    echantillon.conclusion_echantillon(foetus)
    concl = resultat(concordance,foetus,echantillon)
    return concl
        

#CODE Informatif:
# 0 Mere HMZ
# 1 Informatif
# 2 Memes Alleles
# 3 Echo

#CODE Contamine:
# 0 Pas conta
# 1 HMZ Conta
# 2 HTZ Conta




if __name__ == "__main__":
    #M, F, P = lecture_fichier("181985_xfra_ja_200618_PP16.txt")
    M, F, P, Echantillon_F,S_File_m, S_File_f, S_File_p = lecture_fichier("2018-03-27 foetus 90-10_PP16.txt")
    concl = traitement_donnees(M,F,Echantillon_F)
    print(concl)
