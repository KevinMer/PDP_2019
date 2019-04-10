import pandas as pd
import numpy as np
import logging
from datetime import datetime
from time import strftime
import re

    #heure = datetime.now()
    #heure_vrai = heure.strftime("%d-%m-%Y %H:%M")
    #logging.basicConfig(filename='app.log', filemode='w',format='%(levelname)s:%(message)s', level=logging.DEBUG)
    #logging.info("################Mirna Marie-Joseph, Théo Gauvrit, Kévin Merchadou################\n################DPN3000 1.0################\n################"f'{heure_vrai}################')
    #logging.warning('Lancement analyse')



class Echantillon:
    """ Parameters used to analyze one fetal sample

    Attributes:
        date : date sample 
        liste_lignes (list) : extracted from txt file, lines corresponding to fetus
        sexe (str) : fetus sex
        concordance (str) : DNAs match between mother and fetus
        seuil_nbre_marqueurs (int) : marker number which have to be contaminated to declare sample as contaminated
        seuil_taux_conta (int) : one marker is contaminated if his contamination percentage is higher than the value
        seuil_hauteur (int) : spike height to check
        conclusion (int) : contaminated sample (1) or not (0)
    """

    def __init__(self,date,name,liste_lignes,sexe=None,concordance_mere_foet=None, concordance_pere_foet=None,seuil_nbre_marqueurs = 2,seuil_taux_conta = 0.05,seuil_hauteur = 1/3,conclusion = None):
        """ The constructor for Echantillon class

        Parameters:
            date : date sample
            liste_lignes (list) : extracted from txt file, lines corresponding to fetus
            sexe (str) : fetus sex
            concordance (str) : DNAs match between mother and fetus
            seuil_nbre_marqueurs (int) : marker number which have to be contaminated to declare sample as contaminated
            seuil_taux_conta (int) : one marker is contaminated if his contamination percentage is higher than the value
            seuil_hauteur (int) : spike height to check
            conclusion (int) : contaminated sample (1) or not (0)

        """
        self.date = date
        self.name = name
        self.liste_lignes = liste_lignes
        self.seuil_nbre_marqueurs = seuil_nbre_marqueurs
        self.seuil_taux_conta = seuil_taux_conta
        self.conclusion = conclusion
        self.seuil_hauteur = seuil_hauteur
        self.sexe = sexe
        self.concordance_mere_foet = concordance_mere_foet
        self.concordance_pere_foet = concordance_pere_foet

    def get_date(self):
        return self.date

    def gate_name(self):
        return self.name

    def get_seuil_nbre_marqueurs(self):
        """ Return seuil_nbre_marqueurs
        """
        return self.seuil_nbre_marqueurs

    def get_seuil_taux_conta(self):
        """ Return seuil_taux_con
        """
        return self.seuil_taux_conta

    def get_seuil_hauteur(self):
        """ Return seuil_hauteur
        """
        return self.seuil_hauteur

    def get_conclusion(self):
        """ Return conclusion
        """
        return self.conclusion

    def get_sexe(self):
        """ Return sex
        """
        return self.sexe
    
    def get_concordance_mere_foet(self):
        """ Return concordance
        """
        return self.concordance_mere_foet

    def get_concordance_pere_foet(self):
        """ Return concordance
        """
        return self.concordance_pere_foet

    def set_seuil_nbre_marqueurs(self,nb):
        """ Set seuil_nbre_marqueurs
        """
        self.seuil_nbre_marqueurs = nb

    def set_seuil_taux_conta(self,taux):
        """ Set seuil_taux_conta
        """
        self.seuil_taux_conta = taux

    def set_seuil_hauteur(self,hauteur):
        """ Set seuil_hauteur
        """
        self.seuil_hauteur = hauteur
    
    def set_sexe(self,sexe):
        """ Set sex 
        """
        self.sexe = sexe
    
    def set_concordance_mere_foet(self,concordance_mere_foet):
        """ Set concordance 
        """
        self.concordance_mere_foet = concordance_mere_foet

    def set_concordance_pere_foet(self,concordance_pere_foet):
        """ Set concordance 
        """
        self.concordance_pere_foet = concordance_pere_foet

    def set_conclusion(self,conclusion):
        """ Set conclusion
        """
        self.conclusion = conclusion

    def analyse_donnees(self,mere, foetus, pere, log):
        """ Analyze data
            For one couple lignes mother/fetus, informative character and conclusion is set
        
            Parameters :
                mere (list) : lines extracted from txt file corresponding to mother
                foetus (list) : lines extracted from txt file corresponding to fetus 
                
            Return two dataframes :
                - first one containing information about Name, Conclusion and Details for each marker
                - second one containing global information about sample (Number of informative markers, contaminated markers and free contaminated markers )

            """
        concordance_mf = 0
        concordance_pf = None
        if len(pere) != 0:
            concordance_pf = 0
            log = log + "Père détecté.................................\n"
            log = log + "\n\nVérification concordance des ADNs entre père et foetus..............................\n"
            for Alleles in range(len(foetus)):
                for Allele_Foe in range(3):
                    if foetus[Alleles].allele[Allele_Foe] in pere[Alleles].allele:
                        if foetus[Alleles].allele[Allele_Foe] != 0.0:
                            pere[Alleles].concordance_pere_foetus = "OUI"
                            concordance_pf = concordance_pf + 1
                            log = log + "Concordance pour marqueur " + str(foetus[Alleles].marqueur) + " OK..................\n"
                            break
                        else:
                            pere[Alleles].concordance_pere_foetus = "NON"
                            log = log + "Concordance pour marqueur " + foetus[Alleles].marqueur + " PAS OK..............\n"
                            break
        log = log + "\n\nVérification concordance des ADNs entre mère et foetus..............................\n"
        for Alleles in range(len(foetus)):
            for Allele_Foe in range(3):
                if foetus[Alleles].allele[Allele_Foe] in mere[Alleles].allele:
                    if foetus[Alleles].allele[Allele_Foe] != 0.0:
                        foetus[Alleles].concordance_mere_foetus = "OUI"
                        concordance_mf = concordance_mf + 1
                        log = log + "Concordance pour marqueur " + str(foetus[Alleles].marqueur) + " OK..................\n"
                        break
                    else:
                        foetus[Alleles].concordance_mere_foetus = "NON"
                        log = log + "Concordance pour marqueur " + foetus[Alleles].marqueur + " PAS OK..............\n"
                        break
        log = log + "Vérification concordance des ADns terminée..................................\n\n\n"
        if concordance_mf != len(foetus):
            resultats, conclusion = self.resultat(concordance_mf, concordance_pf, foetus, mere, pere)
            log = log + "Concordance des ADNs PAS OK....................\n"
            log = log + "Erreur dans l'échantillon...................\n"
            log = log + "Revérifier s'il vous plaît.............\n"
            return resultats, conclusion, log
        else:
            log = log + "Traitement des 15 autres marqueurs..............................\n"
            for nbre_lignes in range(1,len(mere)):
                log = log + "Traitement du marqueur " + str(foetus[nbre_lignes].marqueur) + "..........\n"
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
                        foetus[nbre_lignes].verif_homozygote_contamine(self)
                        if foetus[nbre_lignes].contamination == 1:
                            log = log + "Homozygote contaminé identifié.....................\n"
                            log = log + "Calcul du taux de contamination....................\n"
                            foetus[nbre_lignes].homozygote_contamine(self)
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
            log = log + "Calcul échantillon contaminé ou non......\n"
            log = log + "Marqueur contaminé si >" + str(self.seuil_taux_conta) + ".......\n"
            log = log + "Echantillon contaminé si plus de " + str(self.seuil_nbre_marqueurs) + "marqueurs contaminés...\n"
            self.conclusion_echantillon(foetus)
            log = log + "Calcul échantillon terminé.....\n"
            log = log + "Fin de traitement...........\n"
            resultats, conclusion = self.resultat(concordance_mf, concordance_pf, foetus,mere, pere)
            return resultats, conclusion, log

    def resultat(self,concordance_mf, concordance_pf, liste_F, liste_M, liste_P):
        """ Set informative character and conclusion for each marker using code tables
                Code tables are :

                Informative code :
                    0 : Homozygous mother
                    1 : Informative marker
                    2 : Same alleles between mother and fetus
                    3 : Stutter

                Contamination code :
                    0 : No contamination
                    1 : Homozygous marker contaminated
                    2 : Heterozygous marker contaminated

                Samle conclusion code :
                    0 : not contaminated
                    1 : contaminated

            Parameters :
                - concordance (int) : DNAs matching markers between mother and fetus
                - list_F (list) : contains fetus lines from txt file

            Return two dataframes :
                - first one containing information about Name, Conclusion and Details for each marker
                - second one containing global information about sample (Number of informative markers, contaminated markers and free contaminated markers)

        """
        resultat = {"Marqueur":[],"Conclusion": [],"Concordance Mere/Foetus":[],"Détails M/F":[],"Concordance Pere/Foetus":[], "Détails P/F":[]}
        marqueurs_conta = 0
        marqueurs_non_conta = 0
        somme_conta = 0
        if liste_F[0].allele[1] == 0.0:
            self.set_sexe("F")
        else:
            self.set_sexe("M")
        if concordance_mf != 16 and concordance_pf != 16:
            self.set_concordance_mere_foet("NON")
            self.set_concordance_pere_foet("NON")
            del resultat["Conclusion"]
            for nbres in range(1,len(liste_F)):
                resultat["Marqueur"].append(str(liste_F[nbres].marqueur))
                resultat["Concordance Mere/Foetus"].append(liste_F[nbres].concordance_mere_foetus)
                resultat["Concordance Pere/Foetus"].append(liste_P[nbres].concordance_pere_foetus)
                if liste_F[nbres].concordance_mere_foetus == "NON" and liste_P[nbres].concordance_pere_foetus == "NON":
                    resultat["Détails M/F"].append("Allèles mère : " + str(liste_M[nbres].allele) + " Allèles foetus : " + str(liste_F[nbres].allele))
                    resultat["Détails P/F"].append("Allèles père : " + str(liste_P[nbres].allele) + " Allèles foetus : " + str(liste_F[nbres].allele))
                elif liste_F[nbres].concordance_mere_foetus == "NON":
                    resultat["Détails M/F"].append("Allèles mère : " + str(liste_M[nbres].allele) + " Allèles foetus : " + str(liste_F[nbres].allele))
                    resultat["Détails P/F"].append("")
                elif liste_P[nbres].concordance_pere_foetus == "NON":
                    resultat["Détails P/F"].append("Allèles père : " + str(liste_P[nbres].allele) + " Allèles foetus : " + str(liste_F[nbres].allele))
                    resultat["Détails M/F"].append("")
                else:
                    resultat["Détails M/F"].append("")
                    resultat["Détails P/F"].append("")
                conclusion = pd.DataFrame({"1": ["Non calculé", "Non calculé", "Non calculé", self.get_date()]},index = ["Nombre de marqueurs informatifs non contaminés","Nombre de marqueurs informatifs contaminés","Moyenne du pourcentage de contamination","Date"])
                resultats = pd.DataFrame(resultat, columns=["Marqueur", "Concordance Mere/Foetus","Détails M/F", "Concordance Pere/Foetus", "Détails P/F"])
            return resultats, conclusion
        elif concordance_mf != len(liste_F) and concordance_pf == len(liste_F):
            self.set_concordance_mere_foet("NON")
            self.set_concordance_pere_foet("OUI")
            del resultat["Conclusion"]
            del resultat["Concordance Pere/Foetus"]
            del resultat["Détails P/F"]
            for nbres in range(1,len(liste_F)):
                resultat["Marqueur"].append(str(liste_F[nbres].marqueur))
                resultat["Concordance Mere/Foetus"].append(liste_F[nbres].concordance_mere_foetus)
                if liste_F[nbres].concordance_mere_foetus == "NON":
                    resultat["Détails M/F"].append("Allèles mère : " + str(liste_M[nbres].allele) + " Allèles foetus : " + str(liste_F[nbres].allele))
                else:
                    resultat["Détails M/F"].append("")
                conclusion = pd.DataFrame({"1": ["Non calculé", "Non calculé", "Non calculé", self.get_date()]},index = ["Nombre de marqueurs informatifs non contaminés","Nombre de marqueurs informatifs contaminés","Moyenne du pourcentage de contamination","Date"])
                resultats = pd.DataFrame(resultat, columns=["Marqueur", "Concordance Mere/Foetus", "Détails M/F"])
            return resultats, conclusion
        elif concordance_mf == len(liste_F) and concordance_pf == len(liste_F) :
            self.set_concordance_mere_foet("OUI")
            self.set_concordance_pere_foet("OUI")
            del resultat["Concordance Mere/Foetus"]
            del resultat["Concordance Pere/Foetus"]
            del resultat["Détails P/F"]
            for nbres in range(1,len(liste_F)):
                resultat["Marqueur"].append(str(liste_F[nbres].marqueur))
                if liste_F[nbres].informatif == 0:
                    resultat["Conclusion"].append("Non informatif")
                    resultat["Détails M/F"].append("Mère homozygote")
                elif liste_F[nbres].informatif == 1:
                    if liste_F[nbres].contamination == 0:
                        marqueurs_non_conta+=1
                        resultat["Conclusion"].append("Non contaminé")
                        resultat["Détails M/F"].append("")   
                    elif liste_F[nbres].contamination == 1:
                        marqueurs_conta+=1
                        somme_conta = somme_conta + liste_F[nbres].taux
                        resultat["Conclusion"].append("Contaminé")
                        resultat["Détails M/F"].append("Taux contamination : " + str(liste_F[nbres].taux) + "%")
                    else:
                        marqueurs_conta+=1
                        somme_conta = somme_conta + liste_F[nbres].taux
                        resultat["Conclusion"].append("Contaminé")
                        resultat["Détails M/F"].append("Taux contamination : " + str(liste_F[nbres].taux) + "%")
                elif liste_F[nbres].informatif == 2:
                    resultat["Conclusion"].append("Non informatif")
                    resultat["Détails M/F"].append("Allèles semblables")
                else:
                    resultat["Conclusion"].append("Non informatif")
                    resultat["Détails M/F"].append("Echo")
            resultats = pd.DataFrame(resultat, columns=["Marqueur", "Conclusion", "Détails M/F"])
            try :
                moyenne_conta = somme_conta / marqueurs_conta
            except ZeroDivisionError:
                moyenne_conta = 0
            conclusion = pd.DataFrame({"1": [int(marqueurs_non_conta),int(marqueurs_conta),round(moyenne_conta,2),self.get_date()]},index = ["Nombre de marqueurs informatifs non contaminés","Nombre de marqueurs informatifs contaminés","Moyenne du pourcentage de contamination","Date"])
            return resultats,conclusion
        elif concordance_mf == len(liste_F) and concordance_pf != len(liste_F):
            self.set_concordance_mere_foet("OUI")
            self.set_concordance_pere_foet("NON")
            del resultat["Concordance Mere/Foetus"]
            for nbres in range(1,len(liste_F)):
                resultat["Concordance Pere/Foetus"].append(liste_P[nbres].concordance_pere_foetus)
                if liste_P[nbres].concordance_pere_foetus == "NON":
                    resultat["Détails P/F"].append("Allèles père : " + str(liste_P[nbres].allele) + " Allèles foetus : " + str(liste_F[nbres].allele))
                else:
                    resultat["Détails P/F"].append("")
            for nbres in range(1,len(liste_F)):
                resultat["Marqueur"].append(str(liste_F[nbres].marqueur))
                if liste_F[nbres].informatif == 0:
                    resultat["Conclusion"].append("Non informatif")
                    resultat["Détails M/F"].append("Mère homozygote")
                elif liste_F[nbres].informatif == 1:
                    if liste_F[nbres].contamination == 0:
                        marqueurs_non_conta+=1
                        resultat["Conclusion"].append("Non contaminé")
                        resultat["Détails M/F"].append("")   
                    elif liste_F[nbres].contamination == 1:
                        marqueurs_conta+=1
                        somme_conta = somme_conta + liste_F[nbres].taux
                        resultat["Conclusion"].append("Contaminé")
                        resultat["Détails M/F"].append("Taux contamination : " + str(liste_F[nbres].taux) + "%")
                    else:
                        marqueurs_conta+=1
                        somme_conta = somme_conta + liste_F[nbres].taux
                        resultat["Conclusion"].append("Contaminé")
                        resultat["Détails M/F"].append("Taux contamination : " + str(liste_F[nbres].taux) + "%")
                elif liste_F[nbres].informatif == 2:
                    resultat["Conclusion"].append("Non informatif")
                    resultat["Détails M/F"].append("Allèles semblables")
                else:
                    resultat["Conclusion"].append("Non informatif")
                    resultat["Détails M/F"].append("Echo")
            resultats = pd.DataFrame(resultat, columns=["Marqueur", "Conclusion", "Détails M/F", "Concordance Pere/Foetus", "Détails P/F"])
            try :
                moyenne_conta = somme_conta / marqueurs_conta
            except ZeroDivisionError:
                moyenne_conta = 0
            conclusion = pd.DataFrame({"1": [int(marqueurs_non_conta),int(marqueurs_conta),round(moyenne_conta,2),self.get_date()]},index = ["Nombre de marqueurs informatifs non contaminés","Nombre de marqueurs informatifs contaminés","Moyenne du pourcentage de contamination","Date"])
            return resultats,conclusion
        else:
            print("Erreur")


    def conclusion_echantillon(self,liste_foetus):
        """ This concludes about sample contamination or not.

            Compare number of contaminated markers (more or equal to 5 %) to seuil_taux_conta.
            If the number is higher than seuil_taux_conta -> sample is contaminated
            Else -> sample is not contaminated

            Parameters :
                liste_foetus (list) : contains fetus lines from txt file
        """
        compteur = 0
        for lignes in range(1,len(liste_foetus)):
            if liste_foetus[lignes].contamination != 0 and liste_foetus[lignes].taux > self.seuil_taux_conta:
                compteur = compteur + 1
        if compteur > self.seuil_nbre_marqueurs:
            self.conclusion = 1
        else:
            self.conclusion = 0

class Patient:

    """ Common informations between mother and fetus

        Attributes :
            marqueur (list) : markers list
            allele (list) : alleles list
            hauteur (list) : alleles height list
            informatif (int) : informatif character of marker
    """

    def __init__(self, marqueur, allele, hauteur, informatif):
        """ The constructor for Patient class

            Parameters :
            marqueur (list) : markers list
            allele (list) : alleles list
            hauteur (list) : alleles height list
            informatif (int) : informatif character of marker
        """

        self.marqueur = marqueur
        self.allele = allele
        self.hauteur = hauteur
        self.informatif = informatif

    def allele_semblable(self, mere): 
        """ Check for each marker if fetus and mother have the same alleles list.
            Because homozygous marker from mother is always non-informative character, we only check similarity for heterozygous marker.

            Parameters :
                - mere (list) : mere class object

            If Similarite is equal to two, informative code is set to 2.
        """
        Similarite = 0
        for Allele in range(3):
            if self.allele[Allele] in mere.allele and self.allele[Allele] != 0.0:
                Similarite = Similarite + 1
        if Similarite == 2:
            self.informatif = 2

    def echo(self, foetus):
        """ Allow to detect stutter.
            Stutter : Fetus alleles are 12 and 8, Mother alleles are 11 and 10. 11 is a stutter because is n-1 (12-1) from fetus alleles

            Parameters :
                - foetus (list) : list of fetus object corresponding to each line of the fetus extracted from the txt file

            If a stutter is detected, fetus informative code is set to 3.

        """
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

    """ Exclusive informations about the mother. Mere class inherits from Patient.

        Attributes :
            homozygote (boolean) : set to True if the mother is homozygous for the marker studied
    """

    def __init__(self, marqueur, allele, hauteur, informatif, homozygote):
        """ The constructor for Mere class

            Parameters :
                - homozygote (boolean) : set to True if the mother is homozygous for the marker studied
        """

        super().__init__(marqueur, allele, hauteur, informatif)
        self.homozygote = homozygote

    def homozygotie(self):
        """ Detect if the mother is homozygous for the marker stutied.
            If it's true, homozygote is set to True
        """
        if self.allele[1] == 0.0:
            self.homozygote = True


class Foetus(Patient):

    """ Exclusive informations about the fetus. Mere class inherits from Patient.

        Attributes :
            - contamination (int) : 0 if the marker is not contaminated. 1 if it is.
            - taux (int) : value corresponding to the contamination
    """

    def __init__(self, marqueur, allele, hauteur, concordance_mere_foetus, informatif, num_foetus,contamination,taux):
        """ The constructor for Mere class

            Parameters :
                - contamination (int) : 0 if the marker is not contaminated. 1 if it is.
                - taux (int) : value corresponding to the contamination
        """

        super().__init__(marqueur, allele, hauteur, informatif)
        self.num_foetus = num_foetus
        self.contamination = contamination
        self.taux = taux
        self.concordance_mere_foetus = concordance_mere_foetus

    def get_num_foetus(self):
        return self.num_foetus

    def foetus_pics(self):
        """ Count spikes number (alleles number)

            Return :
                Spikes number
        """
        pic = 0
        if 0.0 not in self.allele:
            self.contamination = 2
            pic = 3
        elif 0.0 == self.allele[1]:
            pic = 1
        else:
            pic = 2
        return pic

    def contamination_heterozygote(self,mere):
        """ Compute contamination value for heterozygous contamination.

            Parameters :
                - mere (list) : list of Mere object corresponding to each line of the mother extracted from the txt file

            Set taux attribute to value computed.
        """
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
        """ Check if the marker is homozygous contaminated

            Parameters :
            - echantillon : Echantillon object

            If the marker is contaminated, contamination code is set to 1 and informative code is set to 1 too.
            Set taux attribute to value computed.
        """
        seuil = echantillon.get_seuil_hauteur()
        if self.hauteur[0] < self.hauteur[1] * seuil or self.hauteur[1] < self.hauteur[0] * seuil:
            self.contamination = 1
            self.informatif = 1
        else:
            self.taux = 0.0

    def homozygote_contamine(self,echantillon):
        """ Compute contamination value for homozygous contamination.

            Parameters :
                - echantillon : Echantillon object

            Set taux attribute to value computed.
        """
        seuil = echantillon.get_seuil_hauteur()
        if self.hauteur[1] < self.hauteur[0] * seuil:
            allele_contaminant = 1
            taux = ((2 * self.hauteur[allele_contaminant]) / (self.hauteur[allele_contaminant] + self.hauteur[0])) * 100
        else:
            allele_contaminant = 0
            taux = ((2 * self.hauteur[allele_contaminant]) / (self.hauteur[allele_contaminant] + self.hauteur[1])) * 100
        self.taux = round(taux,2)
    


class Pere(Patient):
    """ Exclusive informations about the father. Pere class inherits from Patient.

        Do not implemented because mother and fetus are enough to conclude.
    """

    def __init__(self, marqueur, allele, hauteur, informatif,num_pere,concordance_pere_foetus):
        super().__init__(marqueur, allele, hauteur,informatif)
        self.num_pere = num_pere
        self.concordance_pere_foetus = concordance_pere_foetus

    def get_num_pere(self):
        return self.num_pere

def lecture_fichier(path_data_frame):
    """ Read file corresponding to path_data_frame.
        For each line, Mere, Foetus or Pere object are created.
        At the end, one Echantillon object is created.

        Parameters :
        - path_data_frame (file)

        Return :
        Donnees_Mere (list) : list of Mere object corresponding to each line of the mother extracted from the txt file
        Donnees_Foetus (list) : list of Foetus object corresponding to each line of the fetus extracted from the txt file
        Donnees_Pere (list) : list of Pere object corresponding to each line of the father extracted from the txt file
        Echantillon_F : Echantillon object to summerize the file
    """
    logger = logging.getLogger('Lecture du fichier')
    log = "#### DPNMaker 1.0..............\n### Mirna Marie-Joseph, Théo Gauvrit, Kévin Merchadou\n#### Date : 1 avril 2019\n\n"
    log = log + "Ouverture du fichier.......................................\n"
    log = log + "Chargement des données.......................................\n"
    Iterateur = 2
    Donnees_Mere = []
    Donnees_Foetus = []
    Donnees_Pere = []
    Donnees_na = pd.read_csv(path_data_frame, sep='\t', header=0)
    Donnees = Donnees_na.replace(np.nan, 0.0, regex=True)
    if (Donnees.shape[0] > 32):
        Iterateur = 3
        num_pere = Donnees["Sample Name"].values[2]
    Allele_na = Donnees[["Allele 1", "Allele 2", "Allele 3"]].values
    Hauteur_na = Donnees[["Height 1", "Height 2", "Height 3"]].values
    Date_echantillon = re.search("(\d{4}-\d{2}-\d{2})",Donnees["Sample File"].values[0]).group()
    Nom_echantillon = Donnees["Sample Name"].values[0]
    num_foetus = Donnees["Sample Name"].values[1]
    Allele, Hauteur, log = homogeneite_type(Allele_na, Hauteur_na,log)
    for ligne in range(0, Donnees.shape[0] - 1, Iterateur):
        M = Mere(Donnees["Marker"][ligne], Allele[ligne],
                Hauteur[ligne], None, None)
        F = Foetus(Donnees["Marker"][ligne], Allele[ligne + 1],
                Hauteur[ligne + 1], None, None,num_foetus, None, None)
        if (Iterateur == 3):
            P = Pere(Donnees["Marker"][ligne],
                        Allele[ligne + 2], Hauteur[ligne + 2], None,num_pere,None)
            Donnees_Pere.append(P)
        Donnees_Mere.append(M)
        Donnees_Foetus.append(F)
    Echantillon_F = Echantillon(Date_echantillon,Nom_echantillon,F)
    log = log + "Donnees chargees.......................................\n"
    return Donnees_Mere, Donnees_Foetus, Donnees_Pere,Echantillon_F, log


def homogeneite_type(list_allele, list_hauteur, log):
    """ Allow to convert string into float for Alleles and Height values in order to compute contamination.

        Parameters :
            - list_allele (list) : alleles list
            - list_height (list) : height list

        Return :
            - Allele (list) : converted values
            - Hauteur (list) : converted values
    """
    log = log + "Normalisation des données..........................\n"
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
        
if __name__ == "__main__":
    M, F, P, Echantillon_F, log = lecture_fichier("pp16-dmpk-crampe-050219_PP16.txt")
    resultats, conclusion, log = Echantillon_F.analyse_donnees(M,F,P,log)