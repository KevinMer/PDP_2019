# -*- coding: utf-8 -*-
from Traitement_1 import*
import re
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4,landscape
from reportlab.platypus import Image, Table, TableStyle, Paragraph
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet

'''découpage de la conclusion d'un string à une liste de string'''

def list_info():
    #M, F, P = lecture_fichier("181985_xfra_ja_200618_PP16.txt")
    M, F, P, Echantillon_F,S_File_m, S_File_f, S_File_p = lecture_fichier("2018-03-27 foetus 90-10_PP16.txt")
    concl = traitement_donnees(M,F,Echantillon_F)
    conclu=[S_File_m,S_File_f,S_File_p]
    temp=""

    for lettre in range(len(concl)):
        if concl[lettre]!= "\n":
            temp=temp+concl[lettre]
        else:
            conclu.append(temp)
            temp=""

    return conclu,F,Echantillon_F


'''Remplissage avec Analyse(Part1)'''
def get_num(S_File):
    num=""
    if S_File!="":
        i=0
        while S_File[i]!="_":
            num=num+S_File[i]
            i=i+1
    return num

def get_date(S_File):
    nb_=0
    i=0
    date=""
    while nb_!=2:
        if S_File[i]=="_":
            nb_=nb_+1
        i=i+1
    for pos in range(i,i+10):
        date=date+S_File[pos]
    return date

def complt_num(conclusion):
    nb_mere=get_num(conclusion[0])
    nb_foetus=get_num(conclusion[1])
    nb_pere=get_num(conclusion[2])
    date=get_date(conclusion[0])
    return nb_mere,nb_foetus,nb_pere,date

def get_concordance(conclusion):
    if conclusion=="Concordance OK":
        return "OK"
    else:
        return "PAS OK"
    
conclusion,list_F,Echantillon_F=list_info()
Sexe=conclusion[4][22:len(conclusion[4])]
nb_mere,nb_foetus,nb_pere,date=complt_num(conclusion[0:3])
nom="............................."
Concordance=get_concordance(conclusion[3])
Contamination=conclusion[len(conclusion)-1]




'''Intialisation contenu du pdf'''

styles = getSampleStyleSheet()
style = styles["BodyText"]

canv = Canvas("Résultat.pdf", pagesize=landscape(A4))

#images à intégrer dans le header
CHU = Image('image.D7ADZZ.png')
CHU.drawHeight = 1.25*cm*CHU.drawHeight / CHU.drawWidth
CHU.drawWidth = 1.25*cm

LOGO = Image('logo.png')
LOGO.drawHeight = 1.25*cm*LOGO.drawHeight / LOGO.drawWidth
LOGO.drawWidth = 1.25*cm



header = Paragraph("<b><font size=14.5> Etude de la contamination materno-foetale et de la bonne identité des ADN lors de la réalisation d’un diagnostic prénatal à l’aide du kit PowerPlex ® 16 System </font></b>", style)

C = Paragraph("<font size=12><b><u>Conclusion</u></b></font>",style)

Conclusion = Paragraph("<font size=12><b>Concordance : "+Concordance+"<br/> <br/>Contamination : "+Contamination+"</b></font>",style)

'''Création table'''

#Titre = [[CHU,header,LOGO]]
Titre = [[header]]
HEADER = Table(Titre)
HEADER.setStyle(TableStyle([("BOX", (0, 0), (0,0), 0.25, colors.black),
                            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))


entete = [[Paragraph("<font size=12>Sexe du foetus : "+Sexe+"</font>",style),"",""],
          [Paragraph("<font size=12>N°du fœtus : "+nb_foetus+"</font>",style),Paragraph("<font size=12>N°/Nom de la mère : "+nb_mere+"</font>",style),Paragraph("<font size=12>N°/Nom du père : "+nb_pere+"</font>",style)],
          [Paragraph("<font size=12>Date du run : "+date+"</font>",style),Paragraph("<font size=12>Nom du projet : "+nom+"</font>",style),""]]
t_entete = Table(entete)



data = [ ["Marqueurs","Concordance des ADN","Contamination materno-fœtale","","",""],
         ["","","Informativité","Résultat","Pourcentage de contamination","Détails"],
         ["Amelogenin","","","","",""] ,
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
    
'''Remplissage avec Analyse(Part2)'''

def remplissage_data(conclusion):
    return 0

def resultats(liste_F,Echantillon_F):
    for nb in range(1,len(data)):
        data[nb][1] = Concordance
    for nbres in range(1,len(liste_F)):
        if liste_F[nbres].informatif == 0:
            data[nbres+2][2]="NON INFORMATIF"
            data[nbres+2][3]="/"
            data[nbres+2][4]="/"
            data[nbres+2][5]="mère homozygote"
            
        elif liste_F[nbres].informatif == 1:
            if liste_F[nbres].contamination == 0:
                data[nbres+2][2]="OK"
                data[nbres+2][3]="NON CONTAMINE"
            elif liste_F[nbres].contamination == 1:
                data[nbres+2][2]="OK"
                data[nbres+2][3]="CONTAMINE"
                data[nbres+2][4]=str(liste_F[nbres].taux)+"%"
                data[nbres+2][5]="foetus homozygte"
            else:
                data[nbres+2][2]="OK"
                data[nbres+2][3]="CONTAMINE"
                data[nbres+2][4]=str(liste_F[nbres].taux)+"%"
                data[nbres+2][5]="foetus hétérozygte"
        elif liste_F[nbres].informatif == 2:
            data[nbres+2][2]="NON INFORMATIF"
            data[nbres+2][3]="/"
            data[nbres+2][4]="/"
            data[nbres+2][5]="foetus et mère possèdent les mêmes allèles"
        else:
            data[nbres+2][2]="OK"
            data[nbres+2][3]="/"
            data[nbres+2][5]="Echo"


remplissage_data(conclusion[5:len(conclusion)])
resultats(list_F,Echantillon_F)

'''Définition tableau dans le pdf'''

t = Table(data)
t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
			('SPAN',(2,0),(5,0)),
			('SPAN',(0,0),(0,1)),
			('SPAN',(1,0),(1,1)),
			('ALIGN',(0,0),(5,17),'CENTER'),
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

'''Placement table et paragraphes dans PDF'''

aW = 640
aH = 560

w, h = HEADER.wrap(aW, aH)
HEADER.drawOn(canv, 85, aH)

aH = aH - h
w, h = t_entete.wrap(aW,aH)
t_entete.drawOn(canv, 100,aH-h)


aH = aH - (h+30)
w, h = t.wrap(aW, aH)
t.drawOn(canv, 70, aH-h)

aH = aH - 20
w, f = C.wrap(aW, aH)
C.drawOn(canv,100, aH-h)

aH = aH - 50
w, f = Conclusion.wrap(aW, aH)
Conclusion.drawOn(canv,120, aH-h)

canv.save()

