import re


Marqueur = []
#Mere = {"":{"Allele_m":{"1":None,"2":None,"3":None},"Hauteur_m":{"1":None,"2":None,"3":None}}}
Foetus = {"":{"Allele_f":{"1":None,"2":None,"3":None},"Hauteur_f":{"1":None,"2":None,"3":None}}}

entree = open("pp16-dmpk-crampe-050219_PP16.txt","r")

####Récuperer valeurs
#Avec père de 3 en 3. Sans de 2 en 2
fichier = entree.readlines()
Allele_m = {"1":None,"2":None,"3":None}
Allele_f = {"1":None,"2":None,"3":None}
Hauteur_m = {"1":None,"2":None,"3":None}
Hauteur_f = {"1":None,"2":None,"3":None}
Mere = {"Sample_file":None,"Sample_name":None}
Foetus = {"Sample_file":None,"Sample_name":None}
for l in range(1,len(fichier),2):
    lignes = fichier[l]
    infos = ("").join(lignes)
    valeurs = infos.split("\t")
    Mere["Sample_file"] = valeurs[0]
    Mere["Sample_name"] = valeurs[1]
    Mere[valeurs[2]] = {"Allele_m":Allele_m,"Hauteur_m":Hauteur_m}
    Mere[valeurs[2]]["Allele_m"]["1"] = valeurs[3]
    Mere[valeurs[2]]["Allele_m"]["2"] = valeurs[4]
    Mere[valeurs[2]]["Allele_m"]["3"] = valeurs[5]
    Mere[valeurs[2]]["Hauteur_m"]["1"] = valeurs[6]
    Mere[valeurs[2]]["Hauteur_m"]["2"] = valeurs[7]
    Mere[valeurs[2]]["Hauteur_m"]["3"] = valeurs[8]
    for l in range(2,len(fichier),2):
        Foetus["Sample_file"] = valeurs[0]
        Foetus["Sample_name"] = valeurs[1]
        Foetus[valeurs[2]] = {"Allele_f":Allele_f,"Hauteur_f":Hauteur_f}
        Foetus[valeurs[2]]["Allele_f"]["1"] = valeurs[3]
        Foetus[valeurs[2]]["Allele_f"]["2"] = valeurs[4]
        Foetus[valeurs[2]]["Allele_f"]["3"] = valeurs[5]
        Foetus[valeurs[2]]["Hauteur_f"]["1"] = valeurs[6]
        Foetus[valeurs[2]]["Hauteur_f"]["2"] = valeurs[7]
        Foetus[valeurs[2]]["Hauteur_f"]["3"] = valeurs[8]

