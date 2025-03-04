# -*- coding: utf-8 -*-
from Traitement3 import*

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4,landscape
from reportlab.platypus import Image, Table, TableStyle, Paragraph
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet

'''Lecture dataframe'''
   
def get_date(det_dataframe):
    date=det_dataframe['1'][3]
    return date

def get_concordance(dataframe,presence_pere):
    Concordance_mf="OUI"
    Concordance_pf="OUI"
    for name in dataframe:
        if name == 'Concordance Mere/Foetus':
            Concordance_mf="NON"
        if name == 'Concordance Pere/Foetus':
            Concordance_pf="NON"
    if presence_pere == "ABS":
        Concordance_pf = "ABS"
    return Concordance_mf, Concordance_pf
    
def get_info(det_dataframe):
    nb_info_Nconta = det_dataframe['1'][0]
    nb_info_Conta = det_dataframe['1'][1]
    moy_conta = det_dataframe['1'][2]
    return nb_info_Nconta,nb_info_Conta,moy_conta

def get_contamination(choix_utilisateur, nom_utilisateur):
    if choix_utilisateur==0:
        Contamination="L'échantillon n'est pas contaminé (conclusion automatique)"
    elif choix_utilisateur==1:
        Contamination="L'échantillon est contaminé (conclusion automatique)"
    elif choix_utilisateur==2:
        Contamination="L'échantillon n'est pas contaminé (conclusion modifiée manuellement par "+nom_utilisateur+")"
    elif choix_utilisateur==3:
        Contamination="L'échantillon est contaminé (conclusion modifiée manuellement par "+nom_utilisateur+")"
    else:
        Contamination="Indéterminée"
    return Contamination

def def_variable(nom_projet,nom_fichier_mere,nom_fichier_foetus,nom_fichier_pere,Sexe,dataframe,det_dataframe,choix_utilisateur, nom_utilisateur, presence_pere):
    nom=nom_projet
    nb_mere=nom_fichier_mere
    nb_foetus=nom_fichier_foetus
    nb_pere=nom_fichier_pere
    date=get_date(det_dataframe)
    Sexe=Sexe
    nb_info_Nconta,nb_info_Conta,moy_conta=get_info(det_dataframe)
    Concordance_mf, Concordance_pf=get_concordance(dataframe,presence_pere)
    Decision_contamination=get_contamination(choix_utilisateur, nom_utilisateur)
    return nom,nb_mere,nb_foetus,nb_pere,date,Sexe,Concordance_mf, Concordance_pf,Decision_contamination,nb_info_Nconta,nb_info_Conta,moy_conta

'''Création feuille  pdf'''


def init_pdf(path,filename):

    canv = Canvas(os.path.join(path, filename+".pdf"), pagesize=landscape(A4))
    
    return canv


'''Mise en page'''

def colonne_marqueur(mot):
    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    return Paragraph("<para align=center spaceb=3><font size=12><b>"+mot+"</b></font></para>",style)

def colonne(mot):
    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    return Paragraph("<para align=center spaceb=3><font size=12><font color=white><b>"+mot+"</b></font></font></para>",style)

def diagnos(mot):
    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    if mot=="Contaminé" or mot=="NON" :
        return Paragraph("<para align=center spaceb=3><font size=12><font color=red>"+mot+"</font></font></para>",style)
    if mot=="Non contaminé" or mot=="OUI":
        return Paragraph("<para align=center spaceb=3><font size=12><font color=green>"+mot+"</font></font></para>",style)
    if mot[0:4]=="Taux":
        mot=mot[20:]
        return Paragraph("<para align=center spaceb=3><font size=12><font color=red>"+mot+"</font></font></para>",style)
    else:
        return Paragraph("<para align=center spaceb=3><font size=12>"+mot+"</font></para>",style)

def posinega(mot):
    if mot=="OUI" or mot[0:33] == "L'échantillon n'est pas contaminé":
        return "<font color=green>"+mot+"</font>"
    if mot != "ABS" and mot != "Indéterminée":
        return "<font color=red>"+mot+"</font>"
    return mot

'''Création des flowables et définition du style graphique sauf pour tableau central'''

def creat_struct_pdf(Concordance_mf, Concordance_pf,Entite_d_Application,Emetteur,version):
    '''input:
    Concordance_mf (string) : consistency between the DNA of the mother and the foetus
    Concordance_pf (string) : consistency between the DNA of the father and the foetus
        function:
    Create the formatted table for the header of the chu from their logo, Entite_d_Application, Emetteur and the version of the app. 
    Create the formatted table for the title with th logo of the app
    Create a matrix with a line for each marker, and the appropriate column dependending of the consistency of the DNA between the foetus and the mother, the father.
        output:
    CHU_HEADER (reportlab.platypus.tables.Table) : table containing the header of the CHU
    HEADER (reportlab.platypus.tables.Table) : table containing the logo of the app and title
    data (matrix) : empty table containing a line for each marker and information 
        about contamination or consistency depending on Concordanc_mf and Concordance_pf
    '''

    styles = getSampleStyleSheet()
    style = styles["Normal"]


    CHU = Image(os.path.join('logo_chu.png'))
    CHU.drawHeight = 3.18*cm*CHU.drawHeight / CHU.drawWidth
    CHU.drawWidth = 3.25*cm

    LOGO = Image(os.path.join('logo.png'))
    LOGO.drawHeight = 1.25*cm*LOGO.drawHeight / LOGO.drawWidth
    LOGO.drawWidth = 1.25*cm

    
    entite = Paragraph("<font size=12><b>Entité d'application :</b> "+Entite_d_Application+"</font>",style)
    emetteur = Paragraph("<font size=12><b>Emetteur  :</b>"+Emetteur+" </font>",style)
    no_version = Paragraph("<font size=12><b>"+version+"</b></font>",style)
    doc = Paragraph("<para align=center spaceb=3><font size=12>DOCUMENT D’ENREGISTREMENT</font></para>",style)
    page = Paragraph("<font size=12>Page : 1/1</font>",style)
    chu_titre = Paragraph("<para align=center spaceb=3><b><font size=16><font color=white>Feuille de résultats Recherche de contamination maternelle Kit PowerPlex 16 ® </font></font></b></para>",styles["Title"])

    chu_tab = [[CHU,[entite,emetteur],"","","","","","","","","","",no_version],
               ["",doc,"","","","","","","","","","",page],
               [chu_titre,"","","","","","","","","","","",""]]
    CHU_HEADER = Table(chu_tab)
    CHU_HEADER.setStyle(TableStyle([("BOX", (0, 0), (-1,-1), 1, colors.black),
                                    ('SPAN',(1,0),(11,0)),
                                    ('SPAN',(1,1),(11,1)),
                                    ('SPAN',(1,2),(11,2)),
                                    ('SPAN',(0,2),(12,2)),
                                    ('SPAN',(0,0),(0,1)),
                                    ('BACKGROUND',(0,2),(12,2),colors.lightgrey),
                                    ('LINEABOVE',(0,2),(12,2),1.5,colors.white),
                                    ('VALIGN',(0,0),(3,2),'MIDDLE'),
                                    ('ALIGN',(0,0),(3,2),'CENTER'),
                                    ('ALIGN',(0,2),(2,2),'CENTER'),
                                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))
    
    P0=Paragraph("<para align=center spaceb=3><b><font size=14><font color=darkblue> Étude de la contamination materno-foetale et de la bonne identité des ADN lors de la réalisation d’un diagnostic prénatal à l’aide du kit PowerPlex ® 16 System </font></font></b></para>", style)
    Titre = [[LOGO,P0,"","","","","","","","","",""]]
    
    HEADER = Table(Titre)
    HEADER.setStyle(TableStyle([("BOX", (0, 0), (-1,0), 0.25, colors.HexColor(0x003d99)),
                                ('SPAN',(1,0),(11,0)),
                                ('VALIGN',(1,0),(1,0),'MIDDLE'),
                                ('ALIGN',(0,0),(1,0),'CENTER'),
                                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor(0x003d99))]))



    if Concordance_mf=="OUI": 
        if Concordance_pf=="OUI" or Concordance_pf=="ABS" :
            data = [ [colonne("Marqueurs"),colonne("Contamination materno-fœtale"),"","",""],
                     ["",colonne("Informativités"),colonne("Résultats"),colonne("Pourcentages de contamination"),colonne("Détails")],
                     [colonne_marqueur("CSF1PO"),"","","",""],
                     [colonne_marqueur("D13S317"),"","","",""],
                     [colonne_marqueur("D16S539"),"","","",""],
                     [colonne_marqueur("D18S51"),"","","",""],
                     [colonne_marqueur("D21S11"),"","","",""],
                     [colonne_marqueur("D3S1358"),"","","",""],
                     [colonne_marqueur("D5S818"),"","","",""],
                     [colonne_marqueur("D7S820"),"","","",""],
                     [colonne_marqueur("D8S1179"),"","","",""],
                     [colonne_marqueur("FGA"),"","","",""],
                     [colonne_marqueur("Penta D"),"","","",""],
                     [colonne_marqueur("Penta E"),"","","",""],
                     [colonne_marqueur("THO1"),"","","",""],
                     [colonne_marqueur("TPOX"),"","","",""],
                     [colonne_marqueur("vWA"),"","","",""]]
        else:
            data = [ [colonne("Marqueurs"),colonne("Contamination materno-fœtale"),"","","",colonne("Concordances des ADN paternelles et fœtals"),"",""],
                     ["",colonne("Informativités"),colonne("Résultats"),colonne("Contamination"),colonne("Détails M/F"),colonne("Concordances Père/Fœtus"),colonne("Détails allèles père"),colonne("Détails allèles fœtus")],
                     [colonne_marqueur("CSF1PO"),"","","","","","",""],
                     [colonne_marqueur("D13S317"),"","","","","","",""],
                     [colonne_marqueur("D16S539"),"","","","","","",""],
                     [colonne_marqueur("D18S51"),"","","","","","",""],
                     [colonne_marqueur("D21S11"),"","","","","","",""],
                     [colonne_marqueur("D3S1358"),"","","","","","",""],
                     [colonne_marqueur("D5S818"),"","","","","","",""],
                     [colonne_marqueur("D7S820"),"","","","","","",""],
                     [colonne_marqueur("D8S1179"),"","","","","","",""],
                     [colonne_marqueur("FGA"),"","","","","","",""],
                     [colonne_marqueur("Penta D"),"","","","","","",""],
                     [colonne_marqueur("Penta E"),"","","","","","",""],
                     [colonne_marqueur("THO1"),"","","","","","",""],
                     [colonne_marqueur("TPOX"),"","","","","","",""],
                     [colonne_marqueur("vWA"),"","","","","","",""]]
        
    else: 
        if Concordance_pf=="OUI" or Concordance_pf=="ABS" :
           data = [ [colonne("Marqueurs"),colonne("Concordances des \nADN maternelles et fœtal"),colonne("Détails allèle mère"),colonne("Détails allèle fœtus")],
                     [colonne_marqueur("CSF1PO"),"","",""],
                     [colonne_marqueur("D13S317"),"","",""],
                     [colonne_marqueur("D16S539"),"","",""],
                     [colonne_marqueur("D18S51"),"","",""],
                     [colonne_marqueur("D21S11"),"","",""],
                     [colonne_marqueur("D3S1358"),"","",""],
                     [colonne_marqueur("D5S818"),"","",""],
                     [colonne_marqueur("D7S820"),"","",""],
                     [colonne_marqueur("D8S1179"),"","",""],
                     [colonne_marqueur("FGA"),"","",""],
                     [colonne_marqueur("Penta D"),"","",""],
                     [colonne_marqueur("Penta E"),"","",""],
                     [colonne_marqueur("THO1"),"","",""],
                     [colonne_marqueur("TPOX"),"","",""],
                     [colonne_marqueur("vWA"),"","",""]]
        else:
             data = [ [colonne("Marqueurs"),colonne("Concordances des\n ADN maternelles et fœtals"),colonne("Détails allèles mère"),colonne("Détails allèles fœtus"),colonne("Concordances des \nADN paternelles et fœtals"),colonne("Détails allèles père"),colonne("Détails allèles fœtus")],
                     [colonne_marqueur("CSF1PO"),"","","","","",""],
                     [colonne_marqueur("D13S317"),"","","","","",""],
                     [colonne_marqueur("D16S539"),"","","","","",""],
                     [colonne_marqueur("D18S51"),"","","","","",""],
                     [colonne_marqueur("D21S11"),"","","","","",""],
                     [colonne_marqueur("D3S1358"),"","","","","",""],
                     [colonne_marqueur("D5S818"),"","","","","",""],
                     [colonne_marqueur("D7S820"),"","","","","",""],
                     [colonne_marqueur("D8S1179"),"","","","","",""],
                     [colonne_marqueur("FGA"),"","","","","",""],
                     [colonne_marqueur("Penta D"),"","","","","",""],
                     [colonne_marqueur("Penta E"),"","","","","",""],
                     [colonne_marqueur("THO1"),"","","","","",""],
                     [colonne_marqueur("TPOX"),"","","","","",""],
                     [colonne_marqueur("vWA"),"","","","","",""]]
             
             
    return CHU_HEADER,HEADER,data

'''Affichage des allèles lors d'absencde de concordance'''

def profil_allelique(string):
    '''input:
    string : contains the allelic profile of the parent and the foetus
       function : seperate into two variable the alleles of each individual
       output:
    alleles_p (string) : alleles of the parent
    alleles_f (string) : alleles of the foetus
    '''
    alleles_f=""
    alleles_p=""
    nb_allele=0
    for i in range(len(string)):
        if string[i]=="[":
            nb_allele=nb_allele+1
            j=i
            while string[j+1]!="]":
                j=j+1
                if nb_allele<=1:
                    alleles_p=alleles_p+string[j]
                else:
                    alleles_f=alleles_f+string[j]
    return alleles_p,alleles_f
  
'''Remplissage du tableau principal avec Analyse'''
    
def resultats(data,dataframe,Concordance_mf, Concordance_pf):
    '''input:
    data (matrix) : matrix created in the function create_struct_pdf
    dataframe (dataframe) : contains the conlusion for each markers
    Concordance_mf (string) : consistency between the DNA of the mother and the foetus
    Concordance_pf (string) : consistency between the DNA of the father and the foetus
       function : 
    Fill the matrix with the information contained in the dataframe
       output : 
    None
    '''
    if Concordance_mf=="OUI":
        if Concordance_pf=="OUI" or Concordance_pf=="ABS":
            for marqueurs in range(2,len(data)):
                if dataframe["Conclusion"][marqueurs-2] == "Non informatif":
                     data[marqueurs][1] = dataframe["Conclusion"][marqueurs-2]
                     data[marqueurs][2] = " / "
                     data[marqueurs][3] = " / "
                else:
                     data[marqueurs][1] = "OK"
                     data[marqueurs][2] = diagnos(dataframe["Conclusion"][marqueurs-2])
                     data[marqueurs][3] = " / "
                if dataframe["Détails M/F"][marqueurs-2]!="Echo" and dataframe["Détails M/F"][marqueurs-2]!="Allèles semblables" and dataframe["Détails M/F"][marqueurs-2]!="Mère homozygote":
                    data[marqueurs][3] = diagnos(dataframe["Détails M/F"][marqueurs-2])
                    data[marqueurs][4] = " / "
                else:
                    data[marqueurs][3] = " / "
                    data[marqueurs][4] = diagnos(dataframe["Détails M/F"][marqueurs-2])
                if data[marqueurs][3] == "":
                    data[marqueurs][3] =" / "
        else:
            for marqueurs in range(2,len(data)):
                if dataframe["Conclusion"][marqueurs-2] == "Non informatif":
                     data[marqueurs][1] = dataframe["Conclusion"][marqueurs-2]
                     data[marqueurs][2] = " / "
                     data[marqueurs][3] = " / "
                else:
                     data[marqueurs][1] = "OK"
                     data[marqueurs][2] = diagnos(dataframe["Conclusion"][marqueurs-2])
                     data[marqueurs][3] = " / "
                if dataframe["Détails M/F"][marqueurs-2]!="Echo" and dataframe["Détails M/F"][marqueurs-2]!="Allèles semblables" and dataframe["Détails M/F"][marqueurs-2]!="Mère homozygote":
                     data[marqueurs][3] = diagnos(dataframe["Détails M/F"][marqueurs-2])
                     data[marqueurs][4] = " / "
                else:
                     data[marqueurs][3] = " / "
                     data[marqueurs][4] = dataframe["Détails M/F"][marqueurs-2]
                if data[marqueurs][3] == "":
                     data[marqueurs][3] =" / "
                     
                data[marqueurs][5] = diagnos(dataframe["Concordance Pere/Foetus"][marqueurs-2])
                if dataframe["Concordance Pere/Foetus"][marqueurs-2]=="NON":
                    data[marqueurs][6], data[marqueurs][7] = profil_allelique(dataframe["Détails P/F"][marqueurs-2])
                else:
                    data[marqueurs][6], data[marqueurs][7] = " / "," / "
    else:
        if Concordance_pf=="OUI" or Concordance_pf=="ABS":
            for marqueurs in range(1,len(data)):
                data[marqueurs][1] = diagnos(dataframe["Concordance Mere/Foetus"][marqueurs-1])
                if dataframe["Concordance Mere/Foetus"][marqueurs-1]=="NON":
                    data[marqueurs][2], data[marqueurs][3] = profil_allelique(dataframe["Détails M/F"][marqueurs-1])
                else:
                    data[marqueurs][2], data[marqueurs][3] = " / ", " / "
        else:
            for marqueurs in range(1,len(data)):
                data[marqueurs][1] = diagnos(dataframe["Concordance Mere/Foetus"][marqueurs-1])
                if dataframe["Concordance Mere/Foetus"][marqueurs-1]=="NON":
                    data[marqueurs][2], data[marqueurs][3] = profil_allelique(dataframe["Détails M/F"][marqueurs-1])
                else:
                    data[marqueurs][2], data[marqueurs][3] = " / "," / "
                    
                data[marqueurs][4] = diagnos(dataframe["Concordance Pere/Foetus"][marqueurs-1])
                if dataframe["Concordance Pere/Foetus"][marqueurs-1]=="NON":
                    data[marqueurs][5], data[marqueurs][6] = profil_allelique(dataframe["Détails P/F"][marqueurs-1])
                else:
                    data[marqueurs][5], data[marqueurs][6] = " / "," / "
                
'''Définition du style graphique du tableau principal'''

def style_result(data,Concordance_mf, Concordance_pf):
    '''input:
    data (matrix) : contain the conclusion for each marker
    Concordance_mf (string) : consistency between the DNA of the mother and the foetus
    Concordance_pf (string) : consistency between the DNA of the father and the foetus
       function: 
    Transform the matrix into a table useable for reportlab and adjust the apparence of the table
       output:
    t (reportlab.platypus.tables.Table) : formatted table containing the conclusion for each marker
    '''
    t = Table(data)
    if Concordance_mf=="OUI":
        alternance=range(2,len(data))
        if Concordance_pf=="OUI" or  Concordance_pf=="ABS":
            t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.HexColor(0x003d99)),
                                   ('SPAN',(1,0),(4,0)),
                                   ('SPAN',(0,0),(0,1)),
                                   ('ALIGN',(0,0),(-1,-1),'CENTER'),
                                   ('VALIGN',(0,1),(4,1),'MIDDLE'),
                                   ('VALIGN',(0,0),(0,1),'MIDDLE'),
                                   ('VALIGN',(1,0),(1,1),'MIDDLE'),
                                   ('BACKGROUND',(0,0),(5,2),colors.HexColor(0x4b7fd1)),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor(0x003d99))]))
        else:
            t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.HexColor(0x003d99)),
                                   ('SPAN',(1,0),(4,0)),
                                   ('SPAN',(0,0),(0,1)),
                                   ('SPAN',(5,0),(7,0)),
                                   ('ALIGN',(0,0),(-1,-1),'CENTER'),
                                   ('VALIGN',(0,1),(4,1),'MIDDLE'),
                                   ('VALIGN',(0,0),(0,1),'MIDDLE'),
                                   ('VALIGN',(1,0),(1,1),'MIDDLE'),
                                   ('BACKGROUND',(0,0),(7,2),colors.HexColor(0x4b7fd1)),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor(0x003380))]))
    else:
        alternance=range(1,len(data))
        if Concordance_pf=="OUI" or  Concordance_pf=="ABS":
            t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.HexColor(0x003d99)),
                                   ('ALIGN',(0,0),(-1,-1),'CENTER'),
                                   ('VALIGN',(0,0),(-1,0),'MIDDLE'),
                                   ('BACKGROUND',(0,0),(3,0),colors.HexColor(0x4b7fd1)),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor(0x003d99))]))
        else:
            t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.HexColor(0x003d99)),
                                   ('ALIGN',(0,0),(-1,-1),'CENTER'),
                                   ('VALIGN',(0,0),(-1,0),'MIDDLE'),
                                   ('BACKGROUND',(0,0),(6,0),colors.HexColor(0x4b7fd1)),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor(0x003d99))]))

    for ligne in alternance:
        if ligne % 2 == 0:
            bg_color = colors.white
        else:
            bg_color = colors.HexColor(0xd1e6fa)
        t.setStyle(TableStyle([('BACKGROUND', (0, ligne), (-1, ligne), bg_color)]))
    return t

'''Placement table et paragraphes dans PDF'''


def disposition_pdf(CHU_HEADER,HEADER,t,canv,Concordance_mf, Concordance_pf,Contamination,nb_info_Nconta,nb_info_Conta,moy_conta,nom,nb_mere,nb_foetus,nb_pere,date,Sexe, seuil_pic, seuil_marqueur,seuil_pourcentage):

    aW = 780
    aH = 503
    
    w, h = CHU_HEADER.wrap(aW, aH)
    CHU_HEADER.drawOn(canv, 30, aH)
    
    aW = 780
    aH = 455
    
    w, h = HEADER.wrap(aW, aH)


    HEADER.drawOn(canv, 30, aH)
    
    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    
    P_sexe = Paragraph("<font size=12><font color=darkblue>Sexe du foetus : </font>"+Sexe+"</font>",style)
    P_no_foetus = Paragraph("<font size=12><font color=darkblue>N° du fœtus : </font>"+nb_foetus+"</font>",style)
    P_no_mere = Paragraph("<font size=12><font color=darkblue>N° de la mère : </font>"+nb_mere+"</font>",style)
    P_no_pere = Paragraph("<font size=12><font color=darkblue>N° du père : </font>"+nb_pere+"</font>",style)
    P_date = Paragraph("<font size=12><font color=darkblue>Date du run : </font>"+date+"</font>",style)
    P_nom = Paragraph("<font size=12><font color=darkblue>Nom du projet : </font>"+nom+"</font>",style)

    aH = aH - 5
    w, h = P_sexe.wrap(aW,aH)
    P_sexe.drawOn(canv, 90,aH-h)
    
    w, h = P_nom.wrap(aW,aH)
    P_nom.drawOn(canv, 300,aH-h)
    
    aH = aH - h
    w, h = P_no_mere.wrap(aW,aH)
    P_no_mere.drawOn(canv, 90,aH-h)
    
    w, h = P_no_foetus.wrap(aW,aH)
    P_no_foetus.drawOn(canv, 300,aH-h)
    
    w, h = P_no_pere.wrap(aW,aH)
    P_no_pere.drawOn(canv, 490,aH-h)
    
    aH = aH - h
    w, h = P_date.wrap(aW,aH)
    P_date.drawOn(canv, 90,aH-h)
    
    
    if Concordance_mf=="OUI":#tableau principal
        if Concordance_pf=="OUI" or Concordance_pf=="ABS":
            aH = aH - (h+10)
            w, h = t.wrap(aW, aH)
            t.drawOn(canv, 30, aH-h)
        else:
            aH = aH - (h+10)
            w, h = t.wrap(aW, aH)
            t.drawOn(canv, 25, aH-h)
    else:
        if Concordance_pf=="OUI" or Concordance_pf=="ABS":
            aH = aH - (h+10)
            w, h = t.wrap(aW, aH)
            t.drawOn(canv, 30, aH-h)
        else:
            aH = aH - (h+10)
            w, h = t.wrap(aW, aH)
            t.drawOn(canv, 30, aH-h)


    
    C = Paragraph("<font size=12><font color=darkblue><b><u>Conclusion</u></b></font></font>",style)
    Par = Paragraph("<font size=12><font color=darkblue><u>Paramètres</u></font></font>",style)
    alignement_col_gauche = 20
    alignement_col_centre = 220
    alignement_col_droite = 605
    
    aH = aH - h
    w, h = C.wrap(aW, aH)
    C.drawOn(canv,alignement_col_gauche, aH-h)
    
    w, h = Par.wrap(aW, aH)
    Par.drawOn(canv,alignement_col_droite, aH-h)
    

    P_concordance_p = Paragraph("<font size=12><font color=darkblue><b>Concordance père/foetus: </b></font>"+posinega(Concordance_pf)+"</font>",style)
    P_concordance_m = Paragraph("<font size=12><font color=darkblue><b>Concordance mère/foetus: </b></font>"+posinega(Concordance_mf)+"</font>",style)
    if Concordance_mf != "NON":
        P_nb_Nconta = Paragraph("<b><font size=12><font color=darkblue>Nombre de marqueurs informatifs non contaminés : </font><font color=green>"+str(nb_info_Nconta)+"</font></font></b>",style)
        P_nb_conta = Paragraph("<b><font size=12><font color=darkblue>Nombre de marqueurs informatifs contaminés : </font><font color=red>"+str(nb_info_Conta)+"</font></font></b>",style)
    else:
        P_nb_Nconta = Paragraph("<b><font size=12><font color=darkblue>Nombre de marqueurs informatifs non contaminés : </font>"+str(nb_info_Nconta)+"</font></b>",style)
        P_nb_conta = Paragraph("<b><font size=12><font color=darkblue>Nombre de marqueurs informatifs contaminés : </font>"+str(nb_info_Conta)+"</font></b>",style)
        
    P_moy = Paragraph("<font size=12><b><font color=darkblue>Moyenne du pourcentage de contamination : </font>"+str(moy_conta)+"</b></font>",style)
    P_conta_echantillon = Paragraph("<font size=12><b><font color=darkblue>Contamination : </font>"+posinega(Contamination)+"</b></font>",style)
    P_seuil_m = Paragraph("<font size=12><font color=darkblue>Seuil minimum de marqueur : </font>"+str(seuil_marqueur)+"</font>",style)
    P_seuil_h = Paragraph("<font size=12><font color=darkblue>Seuil de hauteur d'un pic: </font>"+str(seuil_pic)+"</font>",style)
    P_seuil_p = Paragraph("<font size=12><font color=darkblue>Seuil pourcentage de contamination: </font>"+str(seuil_pourcentage)+"</font>",style)
    

    aH = aH - (h+5)
    w, h = P_concordance_m.wrap(aW,aH)
    P_concordance_m.drawOn(canv, alignement_col_gauche,aH-h)
    
    w, h = P_nb_Nconta.wrap(aW,aH)
    P_nb_Nconta.drawOn(canv, alignement_col_centre,aH-h)

    w, h = P_seuil_m.wrap(aW,aH)
    P_seuil_m.drawOn(canv, alignement_col_droite,aH-h)
    
    aH = aH - (h+10)
    if Concordance_pf != "ABS":
        w, h = P_concordance_p.wrap(aW,aH)
        P_concordance_p.drawOn(canv, alignement_col_gauche,aH-h)

    w, h = P_nb_conta.wrap(aW,aH)
    P_nb_conta.drawOn(canv, alignement_col_centre,aH-(h-10))

    w, h =P_seuil_h.wrap(aW,aH)
    P_seuil_h.drawOn(canv, alignement_col_droite,aH-(h-10))

    aH = aH - h
    w, h = P_moy.wrap(aW,aH)
    P_moy.drawOn(canv, alignement_col_centre,aH-(h-10))

    w, h =P_seuil_p.wrap(aW,aH)
    P_seuil_p.drawOn(canv, alignement_col_droite,aH-(h-10))
    
    aH = aH - h
    w, h = P_conta_echantillon.wrap(aW,aH)
    P_conta_echantillon.drawOn(canv, alignement_col_gauche,aH-h)
    
    canv.save()



def creation_PDF(path,nom_projet, nom_fichier_mere, nom_fichier_foetus, nom_fichier_pere, nom_pdf, Sexe, dataframe, det_dataframe, choix_utilisateur, nom_utilisateur, seuil_pic, seuil_marqueur,seuil_pourcentage,presence_pere,Entite_d_Application, Emetteur, version):
    '''
    Input: 
      path : path to the directory to create the pdf
      nom_projet (string) : Name of the project
      nom_fichier_mere (string) : ID number of the mother
      nom_fichier_foetus (string) : ID number of the foetus
      nom_fichier_pere (string) : ID number of the father or None if he is absent
      nom_pdf (string) : name of the pdf
      Sexe (string) : Sexe of the foetus
      dataframe (dataframe) : Results for each marker
      det_dataframe (dataframe) : Global conclusion fo the sample and date of the run
      choix_utilisateur (int) : Code that give the global conclusion with or without the input of the user
      nom_utilisateur (string) : Name of the user
      seuil_pic (int) : Threshold used to decide if a signal should be considered as a contamination
      seuil_marqueur (int) : Threshold used to decide the minimal number of contaminated marker needed to conclude on a contamination 
      seuil_pourcentage (float) : Threshold for the minimal percentage to decide if a sample is contaminated as a whole
      presence_pere (string) : give the presence or absence of the father in the file
      Entite_d_Application (string) : 
      Emetteur (string) : 
      version (string) : version of the software
    Function: Creates a PDF according to the parameters given, in the directory gave by path
    Output: None
    '''


    
    nom,nb_mere,nb_foetus,nb_pere,date,Sexe,Concordance_mf, Concordance_pf,Contamination,nb_info_Nconta,nb_info_Conta,moy_conta = def_variable(nom_projet,nom_fichier_mere,nom_fichier_foetus,nom_fichier_pere,Sexe,dataframe,det_dataframe,choix_utilisateur, nom_utilisateur,presence_pere)
    
    canv = init_pdf(path,nom_pdf)
    
    CHU_HEADER,HEADER,data = creat_struct_pdf(Concordance_mf, Concordance_pf, Entite_d_Application,Emetteur,version)

    resultats(data,dataframe,Concordance_mf, Concordance_pf)

    t=style_result(data,Concordance_mf, Concordance_pf)

    disposition_pdf(CHU_HEADER,HEADER,t,canv,Concordance_mf, Concordance_pf,Contamination,nb_info_Nconta,nb_info_Conta,moy_conta,nom,nb_mere,nb_foetus,nb_pere,date,Sexe, seuil_pic, seuil_marqueur,seuil_pourcentage)


if __name__ == "__main__":
    M, F, P, Echantillon_F, log = lecture_fichier("PP16_XFra_FAURE_290119_PP16.txt")
    path = ""
    dataframe, det_dataframe, log = Echantillon_F.analyse_donnees(M,F,P,log)
    nom_projet="projet"
    nom_fichier_mere="mere"
    nom_fichier_foetus="foetus"
    nom_fichier_pere="pere"
    nom_fichier="fichier"
    date="01/01/1999"
    Sexe="I"
    path=""
    nom_utilisateur = "nom_prenom"
    choix_utilisateur=0
    nom_pdf= nom_projet+"_"+nom_utilisateur
    seuil_pic = 42
    seuil_marqueur = 4
    seuil_pourcentage = 0.42
    presence_pere = "CACA"
    Entite_d_Application=  "-  - SEQUENCEUR"
    Emetteur = "  PTBM -  -"
    version = "V.1"
    creation_PDF(path,nom_projet, nom_fichier_mere, nom_fichier_foetus, nom_fichier_pere, nom_pdf, Sexe, dataframe, det_dataframe, choix_utilisateur, nom_utilisateur, seuil_pic, seuil_marqueur,seuil_pourcentage, presence_pere,Entite_d_Application, Emetteur, version)

