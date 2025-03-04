import pandas as pd
import numpy as np


class Echantillon:

    def __init__(self,liste_lignes,seuil_nbre_marqueurs = 2,seuil_taux_conta = 0.05,seuil_hauteur = 1/3,conclusion = None):
        self.liste_lignes = liste_lignes
        self.seuil_nbre_marqueurs = seuil_nbre_marqueurs
        self.seuil_taux_conta = seuil_taux_conta
        self.conclusion = conclusion
        self.seuil_hauteur = seuil_hauteur

    def conclusion_echantillon(self,liste_foetus):
        compteur = 0
        for lignes in range(1,len(liste_foetus)):
            if liste_foetus[lignes].contamination != 0 and liste_foetus[lignes].taux > self.seuil_taux_conta:
                compteur = compteur + 1
        if compteur > self.seuil_nbre_marqueurs:
            self.conclusion = 0
        else:
            self.conclusion = 1

    def get_seuil_nbre_marqueurs(self):
        return self.seuil_nbre_marqueurs

    def get_seuil_taux_conta(self):
        return self.seuil_taux_conta

    def get_seuil_hauteur(self):
        return self.seuil_hauteur

    def set_seuil_nbre_marqueurs(self,nb):
        self.seuil_nbre_marqueurs = nb

    def set_seuil_taux_conta(self,taux):
        self.seuil_taux_conta = taux

    def set_seuil_hauteur(self,hauteur):
        self.seuil_hauteur = hauteur

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

    def verif_homozygote_contamine(self,echantillon):
        seuil = echantillon.get_seuil_hauteur()
        if self.hauteur[0] < self.hauteur[1] * seuil or self.hauteur[1] < self.hauteur[0] * seuil:
            self.contamination = 1
            self.informatif = 1
        else:
            self.taux = 0.0

    def homozygote_contamine(self,echantillon):
        seuil = echantillon.get_seuil_hauteur()
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
        if F[nbres].informatif == 0:
            affichage = affichage + "Le marqueur " + str(F[nbres].marqueur) + " est NON INFORMATIF car la mère est homozygote\n"
        elif F[nbres].informatif == 1:
            if F[nbres].contamination == 0:
                affichage = affichage + "Le marqueur " + str(F[nbres].marqueur) + " est NON CONTAMINE\n"
            elif F[nbres].contamination == 1:
                affichage = affichage + "Le marqueur " + str(F[nbres].marqueur) + " est HMZ CONTAMINE à hauteur de " + str(F[nbres].taux) + "%\n"
            else:
                affichage = affichage + "Le marqueur " + str(F[nbres].marqueur) + " est HTZ CONTAMINE à hauteur de " + str(F[nbres].taux) + "%\n"
        elif F[nbres].informatif == 2:
            affichage = affichage + "Le marqueur " + str(F[nbres].marqueur) + " est NON INFORMATIF car le foetus et la mère possèdent les mêmes allèles.\n"
        else:
            affichage = affichage + "Le marqueur " + str(F[nbres].marqueur) + " est NON INFORMATIF car dans l'écho\n"
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
    log = "#### DPNMaker 1.0..............\n### Mirna Marie-Joseph, Théo Gauvrit, Kévin Merchadou\n#### Date : 1 avril 2019\n\n"
    log = log + "Ouverture du fichier.......................................\n"
    log = log + "Chargement des données.......................................\n"
    #Entree : le fichier que l'on souhaite ouvrir
    #Lis le data frame et appelle les constructeurs correspondants pour chaque ligne (foetus,mère,père). Les instances sont stockées dans des listes distinces.
    #Retourne la listes des instances pour les lignes mère, foetus et père.
    # Differentier csv, txt -> regex
    Iterateur = 2
    Donnees_Mere = []
    Donnees_Foetus = []
    Donnees_Pere = []
    Donnees_na = pd.read_csv(path_data_frame, sep='\t', header=0)
    Donnees = Donnees_na.replace(np.nan, 0.0, regex=True)
    if (Donnees.shape[0] > 32):
        Iterateur = 3
    Allele_na = Donnees[["Allele 1", "Allele 2", "Allele 3"]].values
    Hauteur_na = Donnees[["Height 1", "Height 2", "Height 3"]].values
    Allele, Hauteur, log = homogeneite_type(Allele_na, Hauteur_na,log)
    for ligne in range(0, Donnees.shape[0] - 1, Iterateur):
        M = Mere(Donnees["Marker"][ligne], Allele[ligne],
                 Hauteur[ligne], None, None)
        F = Foetus(Donnees["Marker"][ligne], Allele[ligne + 1],
                   Hauteur[ligne + 1], None, None, None,None)
        if (Iterateur == 3):
            P = Patient(Donnees["Marker"][ligne],
                        Allele[ligne + 2], Hauteur[ligne + 2], None)
            Donnees_Pere.append(P)
        Donnees_Mere.append(M)
        Donnees_Foetus.append(F)
    Echantillon_F = Echantillon(F)
    log = log + "Donnees chargees.......................................\n"
    return Donnees_Mere, Donnees_Foetus, Donnees_Pere,Echantillon_F, log


def homogeneite_type(list_allele, list_hauteur, log):
    log = log + "Normalisation des données..........................\n"
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
    log = log + "Normalisation effectuée..............................\n"
    return Allele, Hauteur, log

def verif_concordance(mere, foetus, log):
    #Entree : la liste qui contient toutes les lignes de la mère, la liste qui contient toutes les lignes du foetus
    #Vérifie pour chaque position de la liste si un allèle est en commmun entre les deux listes. La concordance est incrémentée de 1 si c'est le cas.
    #Retourne la concordance.
        Taille = 16
        concordance = 0
        liste_non_concordant = []
        log = log + "Vérification concordance des ADNs..............................\n"
        for Alleles in range(Taille):
            for Allele_Foe in range(3):
                if foetus[Alleles].allele[Allele_Foe] in mere[Alleles].allele:
                    if foetus[Alleles].allele[Allele_Foe] != 0.0:
                        concordance = concordance + 1
                        log = log + "Concordance pour marqueur " + str(foetus[Alleles].marqueur) + " OK..................\n"
                        break
                    else:
                        liste_non_concordant.append(foetus[Alleles].marqueur)
                        log = log + "Concordance pour marqueur " + foetus[Alleles].marqueur + " PAS OK..............\n"
                        break
        log = log + "Vérification concordance des ADns terminée..................................\n"
        return concordance, log, liste_non_concordant


def traitement_donnees(mere,foetus,echantillon,log):
    #Entree : la liste qui contient toutes les lignes de la mère, la liste qui contient toutes les lignes du foetus
    #Chaine de traitement des informations permettant de mettre en place une conclusion.
    concordance, log, liste_non_concordant = verif_concordance(mere,foetus,log)
    if concordance != 16:
        log = log + "Concordance des ADNs PAS OK....................\n"
        log = log + "Erreur dans l'échantillon...................\n"
        log = log + "Revérifier s'il vous plaît.............\n"
        for marqueurs in range(len(liste_non_concordant)):
            concl = "Pas de concordance pour " + str(liste_non_concordant[marqueurs]) + "\n"
        concl = concl + "Echantillon non concordant\n"
        return concl,log
    else:
        log = log + "Vérification si foetus à deux allèles pour marqueur AMEL..............\n"
        if foetus[0].allele[1] == 0.0:
            log = log + "Foetus n'a qu'un seul allèle pour marqueur AMEL, sexe féminin..........\n"
            foetus[0].sexe = "F"
        else:
            log = log + "Foetus a deux allèles pour marqueur AMEL, sexe masculin..........\n"
        log = log + "Traitement des 15 autres marqueurs..............................\n"
        for nbre_lignes in range(1,len(mere)):
            log = log + "Traitement du marqueur " + str(foetus[nbre_lignes].marqueur) + ".........."
            pic = foetus[nbre_lignes].foetus_pics()
            log = log + "Calcul du nombre d'allèles pour le foetus......................\n"
            log = log + "Nombre d'allèles pour le foetus : " + str(pic) + ".........\n"
            log = log + "Vérification de l'homozygotie de la mère......................\n"
            mere[nbre_lignes].homozygotie()
            log = log + "Mère homozygote : " + str(mere[nbre_lignes].homozygote) + "...............\n"
            log = log + "Vérification mère et foetus mêmes allèles......................\n"
            foetus[nbre_lignes].allele_semblable(mere[nbre_lignes])
            log = log + "Code de retour vérification allèles semblables: " + str(foetus[nbre_lignes].informatif) + "...............\n"
            log = log + "Initialisation du taux de contamination pour calcul à venir...............\n"
            foetus[nbre_lignes].taux = 0.0
            log = log + "Taux initialisé.................................\n"
            log = log + "Si code informatif de retour allèles semblables différent de 2, vérification écho.............\n"
            log = log + "Si écho, affection code informatif 3...............\n"
            if foetus[nbre_lignes].informatif != 2:
                log = log + "Vérification si écho......................\n"
                mere[nbre_lignes].echo(foetus[nbre_lignes])
                log = log + "Code retour vérification écho : " + str(foetus[nbre_lignes].informatif) + "...............\n"
            log = log + "Début chaîne de traitement...........................\n"
            if pic == 3:
                log = log + "Trois allèles détectés......................\n"
                foetus[nbre_lignes].contamination_heterozygote(mere[nbre_lignes])
                log = log + "Marqueur informatif, affectation du code contamination 1..............\n"
                foetus[nbre_lignes].informatif = 1
                log = log + "Calcul taux de contamination du marqueur..........\n"
                foetus[nbre_lignes].contamination = 2
                log = log + "Calcul terminé....................\n"
            elif mere[nbre_lignes].homozygote:
                log = log + "Mère homozygote.......................\n"
                log = log + "Marqueur non informatif, affectation du code informatif 0............\n"
                foetus[nbre_lignes].informatif = 0
            elif pic == 2:
                log = log + "Deux allèles détectés..............\n"
                if foetus[nbre_lignes].informatif == 2:
                    log = log + "Si mêmes allèles, vérification homozygote contaminé...............\n"
                    foetus[nbre_lignes].verif_homozygote_contamine(echantillon)
                    if foetus[nbre_lignes].contamination == 1:
                        log = log + "Homozygote contaminé identifié.....................\n"
                        log = log + "Calcul du taux de contamination....................\n"
                        foetus[nbre_lignes].homozygote_contamine(echantillon)
                        log = log + "Calcul du taux de contamination effectué...........\n"
                else:
                    if foetus[nbre_lignes].informatif != 3:
                        log = log + "Code calcul écho différent de 3..................\n"
                        log = log + "Marqueur informatif, affectation du code informatif 1.............\n"
                        foetus[nbre_lignes].informatif = 1
                        log = log + "Marqueur non contaminé, affectation du code contamination 0................\n"
                        foetus[nbre_lignes].contamination = 0
            else:
                log = log + "Un seul allèle détecté............\n"
                if foetus[nbre_lignes].informatif != 3:
                    log = log + "Code informatif différent de 3...........\n"
                    log = log + "Marqueur informatif, affectation du code informatif 1.............\n"
                    foetus[nbre_lignes].informatif = 1
                    log = log + "Marqueur non contaminé, affectation du code contamination 0................\n"
                    foetus[nbre_lignes].contamination = 0
            log = log + "\n\n"
            log = log + "Traitement nouveau marqueur\n\n"
    log = log + "Calcul échantillon contaminé ou non......"
    log = log + "Marqueur contaminé si >" + str(echantillon.seuil_taux_conta) + ".......\n"
    log = log + "Echantillon contaminé si plus de " + str(echantillon.seuil_nbre_marqueurs) + "marqueurs contaminés...\n"
    echantillon.conclusion_echantillon(foetus)
    log = log + "Calcul échantillon terminé.....\n"
    log = log + "Fin de traitement...........\n"
    concl = resultat(concordance,foetus,echantillon)
    return concl,log
        

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
    M, F, P, Echantillon_F, log = lecture_fichier("2018-03-27 foetus 90-10_PP16.txt")
    concl,log = traitement_donnees(M,F,Echantillon_F,log)
    print(concl)
