# -*- coding: utf-8 -*-
from Traitement3 import *

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Image, Table, TableStyle, Paragraph
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet

'''Lecture dataframe'''


def get_date(det_dataframe):
    date = det_dataframe['1'][3]
    return date


def get_concordance(dataframe):
    Concordance_mf = "OUI"
    Concordance_pf = "OUI"
    for name in dataframe:
        if name == 'Concordance Mere/Foetus':
            Concordance_mf = "NON"
        if name == 'Concordance Pere/Foetus':
            Concordance_pf = "NON"
    return Concordance_mf, Concordance_pf


def get_info(det_dataframe):
    nb_info_Nconta = det_dataframe['1'][0]
    nb_info_Conta = det_dataframe['1'][1]
    moy_conta = det_dataframe['1'][2]
    return nb_info_Nconta, nb_info_Conta, moy_conta


def get_contamination(choix_utilisateur):
    if choix_utilisateur == 0:
        Contamination = "L'échantillon n'est pas contaminé (conclusion automatique)"
    elif choix_utilisateur == 1:
        Contamination = "L'échantillon est contaminé (conclusion automatique)"
    elif choix_utilisateur == 2:
        Contamination = "L'échantillon n'est pas contaminé (conclusion modifié manuellement)"
    elif choix_utilisateur == 1:
        Contamination = "L'échantillon est contaminé (conclusion modifié manuellement)"
    else:
        Contamination = "Indéterminée"
    return Contamination


def def_variable(nom_projet, nom_fichier_mere, nom_fichier_foetus, nom_fichier_pere, Sexe, dataframe, det_dataframe,
                 choix_utilisateur):
    nom = nom_projet
    nb_mere = nom_fichier_mere
    nb_foetus = nom_fichier_foetus
    nb_pere = nom_fichier_pere
    date = get_date(det_dataframe)
    Sexe = Sexe
    nb_info_Nconta, nb_info_Conta, moy_conta = get_info(det_dataframe)
    Concordance_mf, Concordance_pf = get_concordance(dataframe)
    Contamination = get_contamination(choix_utilisateur)  # conta de l'échantillon global
    return nom, nb_mere, nb_foetus, nb_pere, date, Sexe, Concordance_mf, Concordance_pf, Contamination, nb_info_Nconta, nb_info_Conta, moy_conta


'''Intialisation contenu du pdf'''


def init_pdf(Concordance_mf, Concordance_pf, Contamination, path, nb_info_Nconta, nb_info_Conta, moy_conta):
    styles = getSampleStyleSheet()
    style = styles["BodyText"]

    canv = Canvas(path + "Résultat.pdf", pagesize=landscape(A4))

    # images à intégrer dans le HEADER
    #CHU = Image('image.D7ADZZ.png')
    #CHU.drawHeight = 1.25 * cm * CHU.drawHeight / CHU.drawWidth
    #CHU.drawWidth = 1.25 * cm

    #LOGO = Image('logo.png')
    #LOGO.drawHeight = 1.25 * cm * LOGO.drawHeight / LOGO.drawWidth
    #LOGO.drawWidth = 1.25 * cm

    C = Paragraph("<font size=12><b><u>Conclusion</u></b></font>", style)
    Conclusion = Paragraph(
        "<font size=12><b><br/>Concordance mère/foetus: </b>" + Concordance_mf + "<b><br/>Concordance père/foetus: </b>" + Concordance_pf + "<br/><b>Nombre de marqueurs informatifs non contaminées : </b>" + str(
            nb_info_Nconta) + "  <br/> <b>Nombre de marqueurs informatifs contaminés : </b>" + str(
            nb_info_Conta) + "<br/><b>Moyenne du pourcentage de contamination : </b>" + str(
            moy_conta) + "<br/><br/><b>Contamination : " + Contamination + "</b></font>", style)
    return C, Conclusion, canv


'''Création table'''


def creat_struct_pdf(Sexe, nb_mere, nb_foetus, nb_pere, date, nom, Concordance_mf, Concordance_pf, Contamination,
                     choix_utilisateur):  # selon concord et si oui petit détail pr manuel ou auto

    styles = getSampleStyleSheet()
    style = styles["BodyText"]

    # Titre = [[CHU,header,"",LOGO]]
    Titre = [[Paragraph(
        "<b><font size=14.5> Etude de la contamination materno-foetale et de la bonne identité des ADN lors de la réalisation d’un diagnostic prénatal à l’aide du kit PowerPlex ® 16 System </font></b>",
        style)]]
    HEADER = Table(Titre)
    HEADER.setStyle(TableStyle([("BOX", (0, 0), (0, 0), 0.25, colors.black),
                                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))

    entete = [[Paragraph("<font size=12>Sexe du foetus : " + Sexe + "</font>", style), "", ""],
              [Paragraph("<font size=12>N°du fœtus : " + nb_foetus + "</font>", style),
               Paragraph("<font size=12>N°/Nom de la mère : " + nb_mere + "</font>", style),
               Paragraph("<font size=12>N°/Nom du père : " + nb_pere + "</font>", style)],
              [Paragraph("<font size=12>Date du run : " + date + "</font>", style),
               Paragraph("<font size=12>Nom du projet : " + nom + "</font>", style), ""]]
    t_entete = Table(entete)

    if Concordance_mf == "OUI":
        if Concordance_pf == "OUI":
            data = [["Marqueurs", "Contamination materno-fœtale", "", "", ""],
                    ["", "Informativités", "Résultats", "Pourcentages de contamination", "Détails"],
                    ["CSF1PO", "", "", "", ""],
                    ["D13S317", "", "", "", ""],
                    ["D16S539", "", "", "", ""],
                    ["D18S51", "", "", "", ""],
                    ["D21S11", "", "", "", ""],
                    ["D3S1358", "", "", "", ""],
                    ["D5S818", "", "", "", ""],
                    ["D7S820", "", "", "", ""],
                    ["D8S1179", "", "", "", ""],
                    ["FGA", "", "", "", ""],
                    ["Penta D", "", "", "", ""],
                    ["Penta E", "", "", "", ""],
                    ["THO1", "", "", "", ""],
                    ["TPOX", "", "", "", ""],
                    ["vWA", "", "", "", ""]]
        else:
            data = [
                ["Marqueurs", "Contamination materno-fœtale", "", "", "", "Concordances des ADN paternelles et fœtals",
                 "", ""],
                ["", "Informativités", "Résultats", "Pourcentages de contamination", "Détails M/F",
                 "Concordances Père/Fœtus", "Détails allèles père", "Détails allèles fœtus"],
                ["CSF1PO", "", "", "", "", "", "", ""],
                ["D13S317", "", "", "", "", "", "", ""],
                ["D16S539", "", "", "", "", "", "", ""],
                ["D18S51", "", "", "", "", "", "", ""],
                ["D21S11", "", "", "", "", "", "", ""],
                ["D3S1358", "", "", "", "", "", "", ""],
                ["D5S818", "", "", "", "", "", "", ""],
                ["D7S820", "", "", "", "", "", "", ""],
                ["D8S1179", "", "", "", "", "", "", ""],
                ["FGA", "", "", "", "", "", "", ""],
                ["Penta D", "", "", "", "", "", "", ""],
                ["Penta E", "", "", "", "", "", "", ""],
                ["THO1", "", "", "", "", "", "", ""],
                ["TPOX", "", "", "", "", "", "", ""],
                ["vWA", "", "", "", "", "", "", ""]]

    else:
        if Concordance_pf == "OUI":
            data = [["Marqueurs", "Concordances des \nADN maternelles et fœtal", "Détails allèle mère",
                     "Détails allèle fœtus"],
                    ["CSF1PO", "", "", ""],
                    ["D13S317", "", "", ""],
                    ["D16S539", "", "", ""],
                    ["D18S51", "", "", ""],
                    ["D21S11", "", "", ""],
                    ["D3S1358", "", "", ""],
                    ["D5S818", "", "", ""],
                    ["D7S820", "", "", ""],
                    ["D8S1179", "", "", ""],
                    ["FGA", "", "", ""],
                    ["Penta D", "", "", ""],
                    ["Penta E", "", "", ""],
                    ["THO1", "", "", ""],
                    ["TPOX", "", "", ""],
                    ["vWA", "", "", ""]]
        else:
            data = [["Marqueurs", "Concordances des\n ADN maternelles et fœtals", "Détails allèles mère",
                     "Détails allèles fœtus", "Concordances des \nADN paternelles et fœtals", "Détails allèles père",
                     "Détails allèles fœtus"],
                    ["CSF1PO", "", "", "", "", "", ""],
                    ["D13S317", "", "", "", "", "", ""],
                    ["D16S539", "", "", "", "", "", ""],
                    ["D18S51", "", "", "", "", "", ""],
                    ["D21S11", "", "", "", "", "", ""],
                    ["D3S1358", "", "", "", "", "", ""],
                    ["D5S818", "", "", "", "", "", ""],
                    ["D7S820", "", "", "", "", "", ""],
                    ["D8S1179", "", "", "", "", "", ""],
                    ["FGA", "", "", "", "", "", ""],
                    ["Penta D", "", "", "", "", "", ""],
                    ["Penta E", "", "", "", "", "", ""],
                    ["THO1", "", "", "", "", "", ""],
                    ["TPOX", "", "", "", "", "", ""],
                    ["vWA", "", "", "", "", "", ""]]

    return HEADER, t_entete, data


'''Remplissage avec Analyse(Part2)'''


def profil_allelique(string):
    alleles_f = ""
    alleles_p = ""
    nb_allele = 0
    for i in range(len(string)):
        if string[i] == "[":
            nb_allele = nb_allele + 1
            j = i
            while string[j + 1] != "]":
                j = j + 1
                if nb_allele <= 1:
                    alleles_p = alleles_p + string[j]
                else:
                    alleles_f = alleles_f + string[j]
    return alleles_p, alleles_f


def resultats(data, dataframe, Concordance_mf, Concordance_pf):
    if Concordance_mf == "OUI":
        if Concordance_pf == "OUI" or Concordance_pf == "ABS":
            for marqueurs in range(2, len(data)):
                if dataframe["Conclusion"][marqueurs - 2] == "Non informatif":
                    data[marqueurs][1] = dataframe["Conclusion"][marqueurs - 2]
                    data[marqueurs][2] = " / "
                    data[marqueurs][3] = " / "
                else:
                    data[marqueurs][1] = "OK"
                    data[marqueurs][2] = dataframe["Conclusion"][marqueurs - 2]
                    data[marqueurs][3] = " / "
                if dataframe["Détails M/F"][marqueurs - 2] != "Echo" and dataframe["Détails M/F"][
                    marqueurs - 2] != "Allèles semblables" and dataframe["Détails M/F"][
                    marqueurs - 2] != "Mère homozygote":
                    data[marqueurs][3] = dataframe["Détails M/F"][marqueurs - 2]
                    data[marqueurs][4] = " / "
                else:
                    data[marqueurs][3] = " / "
                    data[marqueurs][4] = dataframe["Détails M/F"][marqueurs - 2]
                if data[marqueurs][3] == "":
                    data[marqueurs][3] = " / "
        else:
            for marqueurs in range(2, len(data)):
                if dataframe["Conclusion"][marqueurs - 2] == "Non informatif":
                    data[marqueurs][1] = dataframe["Conclusion"][marqueurs - 2]
                    data[marqueurs][2] = " / "
                    data[marqueurs][3] = " / "
                else:
                    data[marqueurs][1] = "OK"
                    data[marqueurs][2] = dataframe["Conclusion"][marqueurs - 2]
                    data[marqueurs][3] = " / "
                if dataframe["Détails M/F"][marqueurs - 2] != "Echo" and dataframe["Détails M/F"][
                    marqueurs - 2] != "Allèles semblables" and dataframe["Détails M/F"][
                    marqueurs - 2] != "Mère homozygote":
                    data[marqueurs][3] = dataframe["Détails M/F"][marqueurs - 2]
                    data[marqueurs][4] = " / "
                else:
                    data[marqueurs][3] = " / "
                    data[marqueurs][4] = dataframe["Détails M/F"][marqueurs - 2]
                if data[marqueurs][3] == "":
                    data[marqueurs][3] = " / "

                data[marqueurs][5] = dataframe["Concordance Pere/Foetus"][marqueurs - 2]
                if dataframe["Concordance Pere/Foetus"][marqueurs - 2] == "NON":
                    data[marqueurs][6], data[marqueurs][7] = profil_allelique(dataframe["Détails P/F"][marqueurs - 2])
                else:
                    data[marqueurs][6], data[marqueurs][7] = " / ", " / "
    else:
        if Concordance_pf == "OUI" or Concordance_pf == "ABS":
            for marqueurs in range(1, len(data)):
                data[marqueurs][1] = dataframe["Concordance Mere/Foetus"][marqueurs - 1]
                if dataframe["Concordance Mere/Foetus"][marqueurs - 1] == "NON":
                    data[marqueurs][2], data[marqueurs][3] = profil_allelique(dataframe["Détails M/F"][marqueurs - 1])
                else:
                    data[marqueurs][2], data[marqueurs][3] = " / ", " / "
        else:
            for marqueurs in range(1, len(data)):
                data[marqueurs][1] = dataframe["Concordance Mere/Foetus"][marqueurs - 1]
                if dataframe["Concordance Mere/Foetus"][marqueurs - 1] == "NON":
                    data[marqueurs][2], data[marqueurs][3] = profil_allelique(dataframe["Détails M/F"][marqueurs - 1])
                else:
                    data[marqueurs][2], data[marqueurs][3] = " / ", " / "

                data[marqueurs][4] = dataframe["Concordance Pere/Foetus"][marqueurs - 1]
                if dataframe["Concordance Pere/Foetus"][marqueurs - 1] == "NON":
                    data[marqueurs][5], data[marqueurs][6] = profil_allelique(dataframe["Détails P/F"][marqueurs - 1])
                else:
                    data[marqueurs][5], data[marqueurs][6] = " / ", " / "


'''Définition tableau dans le pdf'''


def style_result(data, Concordance_mf, Concordance_pf):
    t = Table(data)
    if Concordance_mf == "OUI":
        alternance = range(2, len(data))
        if Concordance_pf == "OUI" or Concordance_pf == "ABS":
            t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                                   ('SPAN', (1, 0), (4, 0)),
                                   ('SPAN', (0, 0), (0, 1)),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('VALIGN', (0, 1), (4, 1), 'MIDDLE'),
                                   ('VALIGN', (0, 0), (0, 1), 'MIDDLE'),
                                   ('VALIGN', (1, 0), (1, 1), 'MIDDLE'),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))
        else:
            t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                                   ('SPAN', (1, 0), (4, 0)),
                                   ('SPAN', (0, 0), (0, 1)),
                                   ('SPAN', (5, 0), (7, 0)),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('VALIGN', (0, 1), (4, 1), 'MIDDLE'),
                                   ('VALIGN', (0, 0), (0, 1), 'MIDDLE'),
                                   ('VALIGN', (1, 0), (1, 1), 'MIDDLE'),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))
    else:
        alternance = range(1, len(data))
        if Concordance_pf == "OUI" or Concordance_pf == "ABS":
            t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))
        else:
            t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))

    for ligne in alternance:
        if ligne % 2 == 0:
            bg_color = colors.white
        else:
            bg_color = colors.lightgrey
        t.setStyle(TableStyle([('BACKGROUND', (0, ligne), (-1, ligne), bg_color)]))
    return t


'''Placement table et paragraphes dans PDF'''


def disposition_pdf(HEADER, t_entete, t, C, Conclusion, canv, Concordance_mf, Concordance_pf):
    aW = 650
    aH = 560

    w, h = HEADER.wrap(aW, aH)
    HEADER.drawOn(canv, 85, aH)  # titre

    aH = aH - 5
    w, h = t_entete.wrap(aW, aH)
    t_entete.drawOn(canv, 100, aH - h)  # info

    if Concordance_mf == "OUI":  # tableau principal
        if Concordance_pf == "OUI" or Concordance_pf == "ABS":
            aH = aH - (h + 30)
            w, h = t.wrap(aW, aH)
            t.drawOn(canv, 180, aH - h)
        else:
            aH = aH - (h + 30)
            w, h = t.wrap(aW, aH)
            t.drawOn(canv, 25, aH - h)
    else:
        if Concordance_pf == "OUI" or Concordance_pf == "ABS":
            aH = aH - (h + 30)
            w, h = t.wrap(aW, aH)
            t.drawOn(canv, 220, aH - h)
        else:
            aH = aH - (h + 30)
            w, h = t.wrap(aW, aH)
            t.drawOn(canv, 60, aH - h)

    aH = aH - 25
    w, f = C.wrap(aW, aH)
    C.drawOn(canv, 100, aH - h)  # le mot conclusion soulignés

    aH = aH - 95
    w, f = Conclusion.wrap(aW, aH)
    Conclusion.drawOn(canv, 90, aH - h)  # les conclusions

    canv.save()


def creation_PDF(path,nom_projet, nom_fichier_mere, nom_fichier_foetus, nom_fichier_pere, Sexe, dataframe, det_dataframe,
                 choix_utilisateur):
    nom, nb_mere, nb_foetus, nb_pere, date, Sexe, Concordance_mf, Concordance_pf, Contamination, nb_info_Nconta, nb_info_Conta, moy_conta = def_variable(
        nom_projet, nom_fichier_mere, nom_fichier_foetus, nom_fichier_pere, Sexe, dataframe, det_dataframe,
        choix_utilisateur)

    C, Conclusion, canv = init_pdf(Concordance_mf, Concordance_pf, Contamination, path, nb_info_Nconta,
                                              nb_info_Conta, moy_conta)
    HEADER, t_entete, data = creat_struct_pdf(Sexe, nb_mere, nb_foetus, nb_pere, date, nom, Concordance_mf,
                                              Concordance_pf, Contamination, choix_utilisateur)

    resultats(data, dataframe, Concordance_mf, Concordance_pf)

    t = style_result(data, Concordance_mf, Concordance_pf)

    disposition_pdf(HEADER, t_entete, t, C, Conclusion, canv, Concordance_mf, Concordance_pf)


if __name__ == "__main__":
    M, F, P, Echantillon_F, log = lecture_fichier("2018-03-27 foetus 90-10_PP16.txt")
    dataframe, det_dataframe, log = Echantillon_F.analyse_donnees(M, F, P, log)
    nom_projet = "projet"
    nom_fichier_mere = "mere"
    nom_fichier_foetus = "foetus"
    nom_fichier_pere = "pere"
    nom_fichier = "fichier"
    date = "01/01/1999"
    Sexe = "I"
    path = ""
    choix_utilisateur = 1
    creation_PDF(nom_projet, nom_fichier_mere, nom_fichier_foetus, nom_fichier_pere, Sexe, dataframe, det_dataframe,
                 choix_utilisateur)
