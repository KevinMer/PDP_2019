# -*- coding: utf-8 -*-
from Traitement2 import*

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4,landscape
from reportlab.platypus import Image, Table, TableStyle, Paragraph
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet

'''Lecture dataframe'''
   
def get_date(det_dataframe):
    date=det_dataframe['1'][4]
    return date

def get_concordance(dataframe):
    for name in dataframe:
        if name == 'Concordance':
            Concordance=dataframe["Concordance"]
            break
        else:
            Concordance="OK"
    return Concordance
    
def get_info(det_dataframe):
    nb_info_Nconta = det_dataframe['1'][0]
    nb_info_Conta = det_dataframe['1'][1]
    moy_conta = det_dataframe['1'][2]
    return nb_info_Nconta,nb_info_Conta,moy_conta

def get_contamination(choix_utilisateur):
    if choix_utilisateur==0:
        Contamination="L'échantillon n'est pas contaminé"
    else:
        Contamination="L'échantillon est contaminé"
    return Contamination

def def_variable(nom_projet,nom_fichier_mere,nom_fichier_foetus,nom_fichier_pere,Sexe,dataframe,det_dataframe,choix_utilisateur):
    nom=nom_projet
    nb_mere=nom_fichier_mere
    nb_foetus=nom_fichier_foetus
    nb_pere=nom_fichier_pere
    date=get_date(det_dataframe)
    Sexe=Sexe
    nb_info_Nconta,nb_info_Conta,moy_conta=get_info(det_dataframe)
    Concordance=get_concordance(dataframe)
    Contamination=get_contamination(choix_utilisateur)#conta de l'échantillon global
    return nom,nb_mere,nb_foetus,nb_pere,date,Sexe,Concordance,Contamination,nb_info_Nconta,nb_info_Conta,moy_conta

'''Intialisation contenu du pdf'''
def init_pdf(Concordance,Contamination,path,nb_info_Nconta,nb_info_Conta,moy_conta):
    styles = getSampleStyleSheet()
    style = styles["BodyText"]

    canv = Canvas(path+"Résultat.pdf", pagesize=landscape(A4))

    #images à intégrer dans le HEADER
    CHU = Image('image.D7ADZZ.png')
    CHU.drawHeight = 1.25*cm*CHU.drawHeight / CHU.drawWidth
    CHU.drawWidth = 1.25*cm

    LOGO = Image('logo.png')
    LOGO.drawHeight = 1.25*cm*LOGO.drawHeight / LOGO.drawWidth
    LOGO.drawWidth = 1.25*cm



    C = Paragraph("<font size=12><b><u>Conclusion</u></b></font>",style)
    Conclusion = Paragraph("<font size=12><b><br/>Concordance : </b>"+Concordance+"<br/><b>Nombre de marqueurs informatifs non contaminées : </b>"+str(nb_info_Nconta)+"  <br/> <b>Nombre de marqueurs informatifs contaminés : </b>"+str(nb_info_Conta)+"<br/><b>Moyenne du pourcentage de contamination : </b>"+str(moy_conta)+"<br/><br/><b>Contamination : "+Contamination+"</b></font>",style)
    return C,Conclusion,CHU,LOGO,canv

'''Création table'''
def creat_struct_pdf(Sexe,nb_mere,nb_foetus,nb_pere,date,nom,Concordance,Contamination,choix_utilisateur):#selon concord et si oui petit détail pr manuel ou auto

    styles = getSampleStyleSheet()
    style = styles["BodyText"]

    #Titre = [[CHU,header,LOGO]]
    Titre = [[Paragraph("<b><font size=14.5> Etude de la contamination materno-foetale et de la bonne identité des ADN lors de la réalisation d’un diagnostic prénatal à l’aide du kit PowerPlex ® 16 System </font></b>", style)]]
    HEADER = Table(Titre)
    HEADER.setStyle(TableStyle([("BOX", (0, 0), (0,0), 0.25, colors.black),
                                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))


    entete = [[Paragraph("<font size=12>Sexe du foetus : "+Sexe+"</font>",style),"",""],
            [Paragraph("<font size=12>N°du fœtus : "+nb_foetus+"</font>",style),Paragraph("<font size=12>N°/Nom de la mère : "+nb_mere+"</font>",style),Paragraph("<font size=12>N°/Nom du père : "+nb_pere+"</font>",style)],
            [Paragraph("<font size=12>Date du run : "+date+"</font>",style),Paragraph("<font size=12>Nom du projet : "+nom+"</font>",style),""]]
    t_entete = Table(entete)


    if Concordance=="OK":
        data = [ ["Marqueurs","Contamination materno-fœtale","","",""],
                ["","Informativité","Résultat","Pourcentage de contamination","Détails"],
            ["CSF1PO","","","",""],
            ["D13S317","","","",""],
            ["D16S539","","","",""],
            ["D18S51","","","",""],
            ["D21S11","","","",""],
            ["D3S1358","","","",""],
            ["D5S818","","","",""],
            ["D7S820","","","",""],
            ["D8S1179","","","",""],
            ["FGA","","","",""],
            ["Penta D","","","",""],
            ["Penta E","","","",""],
            ["THO1","","","",""],
            ["TPOX","","","",""],
            ["vWA","","","",""]]
    else: #a faire
        data = [ ["Marqueurs","Concordance des ADN","Contamination materno-fœtale","","",""],
                ["","","Informativité","Résultat","Pourcentage de contamination","Détails"],
            ["CSF1PO","","","","",""],
            ["D13S317","","","","",""],
            ["D16S539","","","","",""],
            ["D18S51","","","","",""],
            ["D21S11","","","","",""],
            ["D3S1358","","","","",""],
            ["D5S818","","","","",""],
            ["D7S820","","","","",""],
            ["D8S1179","","","","",""],
            ["FGA","","","","",""],
            ["Penta D","","","","",""],
            ["Penta E","","","","",""],
            ["THO1","","","","",""],
            ["TPOX","","","","",""],
            ["vWA","","","","",""]]
    return HEADER,t_entete,data
    
'''Remplissage avec Analyse(Part2)'''

def resultats(data,dataframe,Concordance):
    if Concordance=="OK":
        for marqueurs in range(2,len(data)):
            if dataframe["Conclusion"][marqueurs-2] == "Non informatif":
                data[marqueurs][1] = dataframe["Conclusion"][marqueurs-2]
                data[marqueurs][2] = " / "
                data[marqueurs][3] = " / "
            else:
                data[marqueurs][1] = "OK"
                data[marqueurs][2] = dataframe["Conclusion"][marqueurs-2]
                data[marqueurs][3] = " / "
            if dataframe["Détails"][marqueurs-2]!="Echo" and dataframe["Détails"][marqueurs-2]!="Allèles semblables" and dataframe["Détails"][marqueurs-2]!="Mère homozygote":
                data[marqueurs][3] = dataframe["Détails"][marqueurs-2]
                data[marqueurs][4] = " / "
            else:
                data[marqueurs][3] = " / "
                data[marqueurs][4] = dataframe["Détails"][marqueurs-2]
            if data[marqueurs][3] == "":
                data[marqueurs][3] =" / "

'''Définition tableau dans le pdf'''
def style_result(data):
    t = Table(data)
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                ('SPAN',(1,0),(4,0)),
                ('SPAN',(0,0),(0,1)),
                ('ALIGN',(0,0),(4,16),'CENTER'),
                ('VALIGN',(0,1),(4,1),'MIDDLE'),
                ('VALIGN',(0,0),(0,1),'MIDDLE'),
                ('VALIGN',(1,0),(1,1),'MIDDLE'),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))

    for ligne in range(2,len(data)):
        if ligne % 2 == 0:
            bg_color = colors.white
        else:
            bg_color = colors.lightgrey
        t.setStyle(TableStyle([('BACKGROUND', (0, ligne), (-1, ligne), bg_color)]))
    return t

'''Placement table et paragraphes dans PDF'''
def disposition_pdf(HEADER,t_entete,t,C,Conclusion,canv):

    aW = 650
    aH = 560

    w, h = HEADER.wrap(aW, aH)
    HEADER.drawOn(canv, 85, aH)#titre

    aH = aH - 5
    w, h = t_entete.wrap(aW,aH)
    t_entete.drawOn(canv, 100,aH-h)#info


    aH = aH - (h+30)
    w, h = t.wrap(aW, aH)
    t.drawOn(canv, 160, aH-h)#tableau principal

    aH = aH - 25
    w, f = C.wrap(aW, aH)
    C.drawOn(canv,100, aH-h)#le mot conclusion soulignés

    aH = aH - 75
    w, f = Conclusion.wrap(aW, aH)
    Conclusion.drawOn(canv,90, aH-h)#les conclusions

    canv.save()

'''
if __name__ == "__main__":
    M, F, P, Echantillon_F, log = lecture_fichier("181985_xfra_ja_200618_PP16.txt")
    dataframe, det_dataframe, log = Echantillon_F.analyse_donnees(M,F,log)
    nom_projet="projet"
    nom_fichier_mere="mere"
    nom_fichier_foetus="foetus"
    nom_fichier_pere="pere"
    nom_fichier="fichier"
    date="01/01/1999"
    Sexe="I"
    path=""
    choix_utilisateur=0'''

def creation_PDF(nom_projet, nom_fichier_mere, nom_fichier_foetus, nom_fichier_pere, Sexe, dataframe, det_dataframe, choix_utilisateur):
    
    nom,nb_mere,nb_foetus,nb_pere,date,Sexe,Concordance,Contamination,nb_info_Nconta,nb_info_Conta,moy_conta= def_variable(nom_projet,nom_fichier_mere,nom_fichier_foetus,nom_fichier_pere,date,Sexe,dataframe,det_dataframe,choix_utilisateur)
    
    C,Conclusion,CHU,LOGO,canv = init_pdf(Concordance,Contamination,path,nb_info_Nconta,nb_info_Conta,moy_conta)
    HEADER,t_entete,data = creat_struct_pdf(Sexe,nb_mere,nb_foetus,nb_pere,date,nom,Concordance,Contamination,choix_utilisateur)

    resultats(data,dataframe,Concordance)

    t=style_result(data)

    disposition_pdf(HEADER,t_entete,t,C,Conclusion,canv)