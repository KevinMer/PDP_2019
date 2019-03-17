import re


Marqueur = []
#Mere = {"":{"Allele_m":{"1":None,"2":None,"3":None},"Hauteur_m":{"1":None,"2":None,"3":None}}}
Foetus = {"":{"Allele_f":{"1":None,"2":None,"3":None},"Hauteur_f":{"1":None,"2":None,"3":None}}}

entree = open("181985_xfra_ja_200618_PP16.txt","r")

####Récuperer valeurs
fichier = entree.readlines()
Allele_m = {"1":None,"2":None,"3":None}
Allele_f = {"1":None,"2":None,"3":None}
Hauteur_m = {"1":None,"2":None,"3":None}
Hauteur_f = {"1":None,"2":None,"3":None}
Mere = {}
Foetus = {}
for l in range(1,len(fichier),2):
    lignes = fichier[l]
    infos = ("").join(lignes)
    valeurs = infos.split("\t")
    Mere[valeurs[2]] = {"Allele_m":Allele_m,"Hauteur_m":Hauteur_m}
    Mere[valeurs[2]]["Allele_m"]["1"] = valeurs[3]
    Mere[valeurs[2]]["Allele_m"]["2"] = valeurs[4]
    Mere[valeurs[2]]["Allele_m"]["3"] = valeurs[5]
    Mere[valeurs[2]]["Hauteur_m"]["1"] = valeurs[6]
    Mere[valeurs[2]]["Hauteur_m"]["2"] = valeurs[7]
    Mere[valeurs[2]]["Hauteur_m"]["3"] = valeurs[8]
    for l in range(2,len(fichier),2):
        Foetus[valeurs[2]] = {"Allele_f":Allele_f,"Hauteur_f":Hauteur_f}
        Foetus[valeurs[2]]["Allele_f"]["1"] = valeurs[3]
        Foetus[valeurs[2]]["Allele_f"]["2"] = valeurs[4]
        Foetus[valeurs[2]]["Allele_f"]["3"] = valeurs[5]
        Foetus[valeurs[2]]["Hauteur_f"]["1"] = valeurs[6]
        Foetus[valeurs[2]]["Hauteur_f"]["2"] = valeurs[7]
        Foetus[valeurs[2]]["Hauteur_f"]["3"] = valeurs[8]