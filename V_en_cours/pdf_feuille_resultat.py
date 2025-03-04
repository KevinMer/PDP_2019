# -*- coding: utf-8 -*-

import os
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


def get_concordance(dataframe, presence_pere):
    Concordance_mf = "OUI"
    Concordance_pf = "OUI"
    for name in dataframe:
        if name == 'Concordance Mere/Foetus':
            Concordance_mf = "NON"
        if name == 'Concordance Pere/Foetus':
            Concordance_pf = "NON"
    if presence_pere == "ABS":
        Concordance_pf = "ABS"
    return Concordance_mf, Concordance_pf


def get_info(det_dataframe):
    nb_info_Nconta = det_dataframe['1'][0]
    nb_info_Conta = det_dataframe['1'][1]
    moy_conta = det_dataframe['1'][2]
    return nb_info_Nconta, nb_info_Conta, moy_conta


def get_contamination(choix_utilisateur, nom_utilisateur):
    if choix_utilisateur == 0:
        Contamination = "L'échantillon n'est pas contaminé (conclusion automatique)"
    elif choix_utilisateur == 1:
        Contamination = "L'échantillon est contaminé (conclusion automatique)"
    elif choix_utilisateur == 2:
        Contamination = "L'échantillon n'est pas contaminé (conclusion modifiée manuellement par " + nom_utilisateur + ")"
    elif choix_utilisateur == 3:
        Contamination = "L'échantillon est contaminé (conclusion modifiée manuellement par " + nom_utilisateur + ")"
    else:
        Contamination = "Analyse non réalisée"
    return Contamination


def def_variable(nom_projet, nom_fichier_mere, nom_fichier_foetus, nom_fichier_pere, Sexe, dataframe, det_dataframe,
                 choix_utilisateur, nom_utilisateur, presence_pere):
    nom = nom_projet
    nb_mere = nom_fichier_mere
    nb_foetus = nom_fichier_foetus
    nb_pere = nom_fichier_pere
    date = get_date(det_dataframe)
    Sexe = Sexe
    nb_info_Nconta, nb_info_Conta, moy_conta = get_info(det_dataframe)
    Concordance_mf, Concordance_pf = get_concordance(dataframe, presence_pere)
    Decision_contamination = get_contamination(choix_utilisateur, nom_utilisateur)
    return nom, nb_mere, nb_foetus, nb_pere, date, Sexe, Concordance_mf, Concordance_pf, Decision_contamination, nb_info_Nconta, nb_info_Conta, moy_conta


'''Création feuille pdf'''


def init_pdf(path, filename, Concordance_mf, Concordance_pf):
    if Concordance_mf == "NON" or Concordance_pf == "NON":
        canv = Canvas(os.path.join(path, filename + ".pdf"), pagesize=A4)
    else:
        canv = Canvas(os.path.join(path, filename + ".pdf"), pagesize=landscape(A4))
    return canv


'''Mise en page'''


def colonne_marqueur(mot):
    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    return Paragraph("<para align=center spaceb=15> <font size=9><b>" + mot + "</b></font></para>", style)


def colonne(mot):
    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    return Paragraph(
        "<para align=center spaceb=3><font size=12><font color=white><b>" + mot + "</b></font></font></para>", style)


def style_resultat_tableau(mot):
    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    if mot == None:
        return
    else:
        if mot == "Contaminé" or mot == "NON":
            return Paragraph(
                "<para align=center spaceb=3><font size=11><font color=red>" + mot + "</font></font></para>", style)
        if mot == "Non contaminé" or mot == "OUI":
            return Paragraph(
                "<para align=center spaceb=3><font size=11><font color=green>" + mot + "</font></font></para>", style)
        if mot[0:4] == "Taux":
            mot = mot[20:]
            return Paragraph(
                "<para align=center spaceb=3><font size=11><font color=red>" + mot + "</font></font></para>", style)
        if mot == "Informatif":
            return Paragraph("<para align=center spaceb=3><font size=10><b>" + mot + "</b></font></para>", style)
        else:
            return Paragraph(
                "<para align=center spaceb=3><font size=11><font color=black>" + mot + "</font></font></para>", style)


def style_resultat_conclusion(mot):
    if mot == "OUI" or mot[0:33] == "L'échantillon n'est pas contaminé":
        return "<font color=green><font size=13>" + mot + "</font></font>"
    if mot != "ABS":
        return "<font color=red><font size=13>" + mot + "</font></font>"
    return mot


'''Création des flowables et définition du style graphique sauf pour tableau central'''


def creat_struct_pdf(Concordance_mf, Concordance_pf, Entite_d_Application, Emetteur, version):
    '''input:
    Concordance_mf (string) : consistency between the DNA of the mother and the foetus
    Concordance_pf (string) : consistency between the DNA of the father and the foetus
        function:
    Create the formatted table for the header of the chu from their logo, Entite_d_Application, Emetteur and the version of the app.
    Create the formatted table for the title with the logo of the app
    Create a matrix with a line for each marker, and the appropriate column dependending of the consistency of the DNA between the foetus and the mother/the father.
        output:
    CHU_HEADER (reportlab.platypus.tables.Table) : table containing the header of the CHU
    HEADER (reportlab.platypus.tables.Table) : table containing the logo of the app and title
    data (matrix) : empty table containing a line for each marker and a column for the information about contaminations or consistency depending on Concordance_mf and Concordance_pf
    '''

    styles = getSampleStyleSheet()
    style = styles["Normal"]

    CHU = Image(os.path.join('logo_chu.png'))
    CHU.drawHeight = 3.18 * cm * CHU.drawHeight / CHU.drawWidth
    CHU.drawWidth = 3.25 * cm

    LOGO = Image(os.path.join('logo.png'))
    LOGO.drawHeight = 1.25 * cm * LOGO.drawHeight / LOGO.drawWidth
    LOGO.drawWidth = 1.25 * cm

    entite = Paragraph("<font size=12><b>Entité d'application :</b> " + Entite_d_Application + "</font>", style)
    emetteur = Paragraph("<font size=12><b>Emetteur  :</b>" + Emetteur + " </font>", style)
    no_version = Paragraph("<font size=12><b>" + version + "</b></font>", style)
    doc = Paragraph("<para align=center spaceb=3><font size=12>DOCUMENT D’ENREGISTREMENT</font></para>", style)
    page = Paragraph("<font size=12>Page : 1/1</font>", style)
    chu_titre = Paragraph(
        "<para align=center spaceb=3><b><font size=15><font color=white>Feuille de résultats Recherche de contamination maternelle Kit PowerPlex 16 ® </font></font></b></para>",
        styles["Title"])

    chu_tab = [[CHU, [entite, emetteur], "", "", "", no_version],
               ["", doc, "", "", "", page],
               [chu_titre, "", "", "", "", ""]]
    if Concordance_pf == "NON" or Concordance_mf == "NON":
        CHU_HEADER = Table(chu_tab, colWidths=3.4 * cm, rowHeights=1 * cm)
    else:
        CHU_HEADER = Table(chu_tab, colWidths=4.65 * cm, rowHeights=1 * cm)
    CHU_HEADER.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1, colors.black),
                                    ('SPAN', (1, 0), (4, 0)),
                                    ('SPAN', (1, 1), (4, 1)),
                                    ('SPAN', (0, 2), (5, 2)),
                                    ('SPAN', (0, 0), (0, 1)),
                                    ('BACKGROUND', (0, 2), (5, 2), colors.lightgrey),
                                    ('LINEABOVE', (0, 2), (4, 2), 1.5, colors.white),
                                    ('VALIGN', (1, 0), (3, 2), 'MIDDLE'),
                                    ('VALIGN', (4, 0), (5, 1), 'MIDDLE'),
                                    ('ALIGN', (0, 0), (3, 2), 'CENTER'),
                                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))

    P0 = Paragraph(
        "<para align=center spaceb=3><b><font size=13><font color=darkblue> Étude de la contamination materno-foetale et de la bonne identité des ADN lors de la réalisation d’un diagnostic prénatal à l’aide du kit PowerPlex ® 16 System </font></font></b></para>",
        style)
    Titre = [[LOGO, P0, "", "", "", "", "", "", "", "", ""]]

    if Concordance_pf == "NON" or Concordance_mf == "NON":
        HEADER = Table(Titre, colWidths=1.85 * cm)
    else:
        HEADER = Table(Titre, colWidths=2.53 * cm)
    HEADER.setStyle(TableStyle([("BOX", (0, 0), (-1, 0), 0.25, colors.HexColor(0x003d99)),
                                ('SPAN', (1, 0), (10, 0)),
                                ('VALIGN', (1, 0), (1, 0), 'MIDDLE'),
                                ('ALIGN', (0, 0), (1, 0), 'CENTER'),
                                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor(0x003d99))]))

    if Concordance_mf == "OUI":
        if Concordance_pf == "OUI" or Concordance_pf == "ABS":
            data = [[colonne("Marqueurs"), colonne("Contamination materno-fœtale"), "", "", ""],
                    ["", colonne("Informativité"), colonne("Résultat"), colonne("Pourcentage de contamination"),
                     colonne("Détails")],
                    [colonne_marqueur("CSF1PO"), "", "", "", ""],
                    [colonne_marqueur("D13S317"), "", "", "", ""],
                    [colonne_marqueur("D16S539"), "", "", "", ""],
                    [colonne_marqueur("D18S51"), "", "", "", ""],
                    [colonne_marqueur("D21S11"), "", "", "", ""],
                    [colonne_marqueur("D3S1358"), "", "", "", ""],
                    [colonne_marqueur("D5S818"), "", "", "", ""],
                    [colonne_marqueur("D7S820"), "", "", "", ""],
                    [colonne_marqueur("D8S1179"), "", "", "", ""],
                    [colonne_marqueur("FGA"), "", "", "", ""],
                    [colonne_marqueur("Penta D"), "", "", "", ""],
                    [colonne_marqueur("Penta E"), "", "", "", ""],
                    [colonne_marqueur("THO1"), "", "", "", ""],
                    [colonne_marqueur("TPOX"), "", "", "", ""],
                    [colonne_marqueur("vWA"), "", "", "", ""]]
        else:
            data = [[colonne("Marqueurs"), colonne("Contamination materno-fœtale"), "", "", "",
                     colonne("Concordance des ADN"), ""],
                    ["", colonne("Informativité"), colonne("Résultat"), colonne("Contamination"),
                     colonne("Détails Mère/Fœtus"), colonne("Père/Fœtus"), colonne("Détails allèles père et fœtus")],
                    [colonne_marqueur("CSF1PO"), "", "", "", "", "", ""],
                    [colonne_marqueur("D13S317"), "", "", "", "", "", ""],
                    [colonne_marqueur("D16S539"), "", "", "", "", "", ""],
                    [colonne_marqueur("D18S51"), "", "", "", "", "", ""],
                    [colonne_marqueur("D21S11"), "", "", "", "", "", ""],
                    [colonne_marqueur("D3S1358"), "", "", "", "", "", ""],
                    [colonne_marqueur("D5S818"), "", "", "", "", "", ""],
                    [colonne_marqueur("D7S820"), "", "", "", "", "", ""],
                    [colonne_marqueur("D8S1179"), "", "", "", "", "", ""],
                    [colonne_marqueur("FGA"), "", "", "", "", "", ""],
                    [colonne_marqueur("Penta D"), "", "", "", "", "", ""],
                    [colonne_marqueur("Penta E"), "", "", "", "", "", ""],
                    [colonne_marqueur("THO1"), "", "", "", "", "", ""],
                    [colonne_marqueur("TPOX"), "", "", "", "", "", ""],
                    [colonne_marqueur("vWA"), "", "", "", "", "", ""]]

    else:
        if Concordance_pf == "OUI" or Concordance_pf == "ABS":
            data = [[colonne("Marqueurs"), colonne("Concordances des ADN maternelles et fœtal"),
                     colonne("Détails allèles mère et fœtus")],
                    [colonne_marqueur("CSF1PO"), "", ""],
                    [colonne_marqueur("D13S317"), "", ""],
                    [colonne_marqueur("D16S539"), "", ""],
                    [colonne_marqueur("D18S51"), "", ""],
                    [colonne_marqueur("D21S11"), "", ""],
                    [colonne_marqueur("D3S1358"), "", ""],
                    [colonne_marqueur("D5S818"), "", ""],
                    [colonne_marqueur("D7S820"), "", ""],
                    [colonne_marqueur("D8S1179"), "", ""],
                    [colonne_marqueur("FGA"), "", ""],
                    [colonne_marqueur("Penta D"), "", ""],
                    [colonne_marqueur("Penta E"), "", ""],
                    [colonne_marqueur("THO1"), "", ""],
                    [colonne_marqueur("TPOX"), "", ""],
                    [colonne_marqueur("vWA"), "", ""]]
        else:
            data = [[colonne("Marqueurs"), colonne("Concordance des ADN maternelles et fœtals"),
                     colonne("Détails allèles mère et fœtus"), colonne("Concordance des ADN paternelles et fœtals"),
                     colonne("Détails allèles père et fœtus")],
                    [colonne_marqueur("CSF1PO"), "", "", "", ""],
                    [colonne_marqueur("D13S317"), "", "", "", ""],
                    [colonne_marqueur("D16S539"), "", "", "", ""],
                    [colonne_marqueur("D18S51"), "", "", "", ""],
                    [colonne_marqueur("D21S11"), "", "", "", ""],
                    [colonne_marqueur("D3S1358"), "", "", "", ""],
                    [colonne_marqueur("D5S818"), "", "", "", ""],
                    [colonne_marqueur("D7S820"), "", "", "", ""],
                    [colonne_marqueur("D8S1179"), "", "", "", ""],
                    [colonne_marqueur("FGA"), "", "", "", ""],
                    [colonne_marqueur("Penta D"), "", "", "", ""],
                    [colonne_marqueur("Penta E"), "", "", "", ""],
                    [colonne_marqueur("THO1"), "", "", "", ""],
                    [colonne_marqueur("TPOX"), "", "", "", ""],
                    [colonne_marqueur("vWA"), "", "", "", ""]]

    return CHU_HEADER, HEADER, data


'''Affichage des allèles lors d'absencde de concordance'''


def profil_allelique(string):
    '''input:
    string : contains the allelic profile of the parent and the foetus
       function : seperate into two variable the alleles of each individual
       output:
    alleles_p (string) : alleles of the parent
    alleles_f (string) : alleles of the foetus
    '''
    styles = getSampleStyleSheet()
    style = styles["BodyText"]
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
    profil_all_p = Paragraph(
        "<para align=center spaceb=3><font size=10><font color=grey>" + alleles_p + "</font></font></para>", style)
    profil_all_f = Paragraph("<para align=center spaceb=3><font size=10>" + alleles_f + "</font></para>", style)
    return [profil_all_p, profil_all_f]


'''Remplissage du tableau principal avec Analyse'''


def resultats(data, dataframe, Concordance_mf, Concordance_pf):
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
    ligne_informative = []
    if Concordance_mf == "OUI":
        if Concordance_pf == "OUI" or Concordance_pf == "ABS":
            for marqueurs in range(2, len(data)):
                if dataframe["Conclusion"][marqueurs - 2] == "Non informatif":
                    data[marqueurs][1] = style_resultat_tableau(dataframe["Conclusion"][marqueurs - 2])
                    data[marqueurs][2] = " / "
                    data[marqueurs][3] = " / "
                else:
                    data[marqueurs][1] = style_resultat_tableau("Informatif")
                    data[marqueurs][2] = style_resultat_tableau(dataframe["Conclusion"][marqueurs - 2])
                    data[marqueurs][3] = " / "
                    ligne_informative.append(marqueurs)
                if dataframe["Détails M/F"][marqueurs - 2] != "Echo" and dataframe["Détails M/F"][
                    marqueurs - 2] != "Mêmes allèles que la mère" and dataframe["Détails M/F"][
                    marqueurs - 2] != "Mère homozygote":
                    data[marqueurs][3] = style_resultat_tableau(dataframe["Détails M/F"][marqueurs - 2])
                    data[marqueurs][4] = " / "
                else:
                    data[marqueurs][3] = " / "
                    data[marqueurs][4] = style_resultat_tableau(dataframe["Détails M/F"][marqueurs - 2])
                if data[marqueurs][3] == "":
                    data[marqueurs][3] = " / "
        else:
            for marqueurs in range(2, len(data)):
                if dataframe["Conclusion"][marqueurs - 2] == "Non informatif":
                    data[marqueurs][1] = style_resultat_tableau(dataframe["Conclusion"][marqueurs - 2])
                    data[marqueurs][2] = " / "
                    data[marqueurs][3] = " / "
                else:
                    ligne_informative.append(marqueurs)
                    data[marqueurs][1] = style_resultat_tableau("Informatif")
                    data[marqueurs][2] = style_resultat_tableau(dataframe["Conclusion"][marqueurs - 2])
                    data[marqueurs][3] = " / "
                if dataframe["Détails M/F"][marqueurs - 2] != "Echo" and dataframe["Détails M/F"][
                    marqueurs - 2] != "Mêmes allèles que la mère" and dataframe["Détails M/F"][
                    marqueurs - 2] != "Mère homozygote":
                    data[marqueurs][3] = style_resultat_tableau(dataframe["Détails M/F"][marqueurs - 2])
                    data[marqueurs][4] = " / "
                else:
                    data[marqueurs][3] = " / "
                    data[marqueurs][4] = style_resultat_tableau(dataframe["Détails M/F"][marqueurs - 2])
                if data[marqueurs][3] == "":
                    data[marqueurs][3] = " / "

                data[marqueurs][5] = style_resultat_tableau(dataframe["Concordance Pere/Foetus"][marqueurs - 2])
                if dataframe["Concordance Pere/Foetus"][marqueurs - 2] == "NON":
                    data[marqueurs][6] = profil_allelique(dataframe["Détails P/F"][marqueurs - 2])
                else:
                    data[marqueurs][6] = " / "
    else:
        ligne_informative = range(2, len(data), 2)
        if Concordance_pf == "OUI" or Concordance_pf == "ABS":
            for marqueurs in range(1, len(data)):
                data[marqueurs][1] = style_resultat_tableau(dataframe["Concordance Mere/Foetus"][marqueurs - 1])
                if dataframe["Concordance Mere/Foetus"][marqueurs - 1] == "NON":
                    data[marqueurs][2] = profil_allelique(dataframe["Détails M/F"][marqueurs - 1])
                else:
                    data[marqueurs][2] = " / "
        else:
            for marqueurs in range(1, len(data)):
                data[marqueurs][1] = style_resultat_tableau(dataframe["Concordance Mere/Foetus"][marqueurs - 1])
                if dataframe["Concordance Mere/Foetus"][marqueurs - 1] == "NON":
                    data[marqueurs][2] = profil_allelique(dataframe["Détails M/F"][marqueurs - 1])
                else:
                    data[marqueurs][2] = " / "

                data[marqueurs][3] = style_resultat_tableau(dataframe["Concordance Pere/Foetus"][marqueurs - 1])
                if dataframe["Concordance Pere/Foetus"][marqueurs - 1] == "NON":
                    data[marqueurs][4] = profil_allelique(dataframe["Détails P/F"][marqueurs - 1])
                else:
                    data[marqueurs][4] = " / "
    return ligne_informative


'''Définition du style graphique du tableau principal'''


def style_result(data, Concordance_mf, Concordance_pf, l_info):
    '''input:
    data (matrix) : contain the conclusion for each marker
    Concordance_mf (string) : consistency between the DNA of the mother and the foetus
    Concordance_pf (string) : consistency between the DNA of the father and the foetus
       function:
    Transform the matrix into a table useable for reportlab and adjust the apparence of the table
       output:
    t (reportlab.platypus.tables.Table) : formatted table containing the conclusion for each marker
    '''
    if Concordance_mf == "OUI":
        if Concordance_pf == "OUI" or Concordance_pf == "ABS":
            t = Table(data)
            t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.HexColor(0x003d99)),
                                   ('SPAN', (1, 0), (4, 0)),
                                   ('SPAN', (0, 0), (0, 1)),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('VALIGN', (0, 1), (4, 1), 'MIDDLE'),
                                   ('VALIGN', (0, 0), (0, 1), 'MIDDLE'),
                                   ('VALIGN', (1, 0), (1, 1), 'MIDDLE'),
                                   ('BACKGROUND', (0, 0), (5, 1), colors.HexColor(0x4b7fd1)),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor(0x003d99))]))
        else:
            t = Table(data, colWidths=[2.59 * cm, 3 * cm, 2.4 * cm, 3.4 * cm, 3.5 * cm, 2.76 * cm, 2.95 * cm],
                      rowHeights=[1 * cm] + [1.4 * cm] + [1.2 * cm] * 15)
            t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.HexColor(0x003d99)),
                                   ('SPAN', (1, 0), (4, 0)),
                                   ('SPAN', (0, 0), (0, 1)),
                                   ('SPAN', (5, 0), (6, 0)),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                   ('BACKGROUND', (0, 0), (6, 1), colors.HexColor(0x4b7fd1)),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor(0x003380))]))
    else:
        if Concordance_pf == "OUI" or Concordance_pf == "ABS":
            t = Table(data, colWidths=6.3 * cm)
            t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.HexColor(0x003d99)),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                   ('BACKGROUND', (0, 0), (3, 0), colors.HexColor(0x4b7fd1)),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor(0x003d99))]))
        else:

            t = Table(data, colWidths=4.05 * cm)
            t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.HexColor(0x003d99)),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                   ('BACKGROUND', (0, 0), (6, 0), colors.HexColor(0x4b7fd1)),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor(0x003d99))]))

    for ligne in l_info:
        t.setStyle(TableStyle([('BACKGROUND', (0, ligne), (-1, ligne), colors.HexColor(0xd1e6fa))]))
    return t


'''Placement table et paragraphes dans PDF'''


def disposition_pdf(CHU_HEADER, HEADER, nom_utilisateur, tableau_principal, canv, Concordance_mf, Concordance_pf,
                    Contamination, nb_info_Nconta, nb_info_Conta, moy_conta, nom, nb_mere, nb_foetus, nb_pere, date,
                    Sexe, seuil_pic, seuil_marqueur, seuil_pourcentage):
    aW = 780
    aH = 500
    if Concordance_mf == "NON" or Concordance_pf == "NON":
        aW = aW - 20
        aH = aH + 240

    w, h = CHU_HEADER.wrap(aW, aH)
    CHU_HEADER.drawOn(canv, aW - 750, aH)

    aH = aH - 50

    w, h = HEADER.wrap(aW, aH)

    HEADER.drawOn(canv, aW - 750, aH)

    styles = getSampleStyleSheet()
    style = styles["BodyText"]

    P_date = Paragraph("<font size=12><font color=darkblue>Date du run : </font>" + date + "</font>", style)
    P_nom = Paragraph("<font size=12><font color=darkblue>Nom du projet : </font>" + nom + "</font>", style)
    P_utilisateur = Paragraph("<font size=12><font color=darkblue>Utilisateur : </font>" + nom_utilisateur + "</font>",
                              style)
    P_sexe = Paragraph("<font size=12><font color=darkblue>Sexe du foetus : </font>" + Sexe + "</font>", style)
    P_no_foetus = Paragraph("<font size=12><font color=darkblue>N° du fœtus : </font>" + nb_foetus + "</font>", style)
    P_no_mere = Paragraph("<font size=12><font color=darkblue>N° de la mère : </font>" + nb_mere + "</font>", style)
    P_no_pere = Paragraph("<font size=12><font color=darkblue>N° du père : </font>" + nb_pere + "</font>", style)

    if Concordance_mf == "NON" or Concordance_pf == "NON":
        alignement_col_gauche = 10
        alignement_col_centre = 155
        alignement_col_droite = 380
        align_mere = 300
        align_pere = 460
    else:
        alignement_col_gauche = 60
        alignement_col_centre = 220
        alignement_col_droite = 490
        align_mere = 420
        align_pere = 640

    aH = aH - 10
    w, h = P_date.wrap(aW, aH)
    P_date.drawOn(canv, alignement_col_gauche, aH - h)

    w, h = P_nom.wrap(aW, aH)
    P_nom.drawOn(canv, alignement_col_centre, aH - h)

    w, h = P_utilisateur.wrap(aW, aH)
    P_utilisateur.drawOn(canv, alignement_col_droite, aH - h)

    aH = aH - h

    w, h = P_no_foetus.wrap(aW, aH)
    P_no_foetus.drawOn(canv, alignement_col_centre, aH - h)

    w, h = P_sexe.wrap(aW, aH)
    P_sexe.drawOn(canv, alignement_col_gauche, aH - h)

    w, h = P_no_mere.wrap(aW, aH)
    P_no_mere.drawOn(canv, align_mere, aH - h)

    w, h = P_no_pere.wrap(aW, aH)
    P_no_pere.drawOn(canv, align_pere, aH - h)

    if Concordance_mf == "OUI":  # tableau_principal
        if Concordance_pf == "OUI" or Concordance_pf == "ABS":
            aH = aH - (h + 10)
            w, h = tableau_principal.wrap(aW, aH)
            tableau_principal.drawOn(canv, 30, aH - h)
        else:
            aH = aH - (h + 10)
            w, h = tableau_principal.wrap(aW, aH)
            tableau_principal.drawOn(canv, 5, aH - h)
    else:
        if Concordance_pf == "OUI" or Concordance_pf == "ABS":
            aH = aH - (h + 10)
            w, h = tableau_principal.wrap(aW, aH)
            tableau_principal.drawOn(canv, 30, aH - h)
        else:
            aH = aH - (h + 10)
            w, h = tableau_principal.wrap(aW, aH)
            tableau_principal.drawOn(canv, 10, aH - h)

    Par = Paragraph("<font size=12><font color=darkblue><u>Paramètres</u></font></font>", style)
    alignement_col_gauche = 20
    alignement_col_centre = 220
    alignement_col_droite = 580

    aH = aH - h
    w, h = Par.wrap(aW, aH)
    if Concordance_mf == "OUI" and Concordance_pf == "NON":
        Par.drawOn(canv, 500, aH - h)
    elif Concordance_mf == "OUI":
        Par.drawOn(canv, alignement_col_droite, aH - h)

    P_concordance_p = Paragraph(
        "<font size=12><font color=darkblue><b>Concordance père/foetus: </b></font>" + style_resultat_conclusion(
            Concordance_pf) + "</font>", style)
    P_concordance_m = Paragraph(
        "<font size=12><font color=darkblue><b>Concordance mère/foetus: </b></font>" + style_resultat_conclusion(
            Concordance_mf) + "</font>", style)
    if Concordance_mf != "NON":
        P_nb_Nconta = Paragraph(
            "<b><font size=12><font color=darkblue>Marqueurs informatifs non contaminés : </font><font color=green>" + str(
                nb_info_Nconta) + "</font></font></b>", style)
        P_nb_conta = Paragraph(
            "<b><font size=12><font color=darkblue>Marqueurs informatifs contaminés : </font><font color=red>" + str(
                nb_info_Conta) + "</font></font></b>", style)
        P_moy = Paragraph(
            "<font size=12><b><font color=darkblue>Moyenne des pourcentages de contamination : </font>" + str(
                moy_conta) + "</b></font>", style)
    else:
        P_nb_Nconta = Paragraph(
            "<b><font size=12><font color=darkblue>Marqueurs informatifs non contaminés : </font><font color=red>" + str(
                nb_info_Nconta) + "</font></font></b>", style)
        P_nb_conta = Paragraph(
            "<b><font size=12><font color=darkblue>Marqueurs informatifs contaminés : </font><font color=red>" + str(
                nb_info_Conta) + "</font></font></b>", style)
        P_moy = Paragraph(
            "<font size=12><b><font color=darkblue>Moyenne des pourcentages de contamination : </font><font color=red>" + str(
                moy_conta) + "</font></b></font>", style)

    P_conta_echantillon = Paragraph("<font size=12><b>" + style_resultat_conclusion(Contamination) + "</b></font>",
                                    style)
    P_seuil_m = Paragraph("<font size=12><font color=darkblue>N : </font>" + str(seuil_marqueur) + "</font>", style)
    P_seuil_h = Paragraph("<font size=12><font color=darkblue>H : </font>" + str(seuil_pic) + "</font>", style)

    aH = aH - h
    w, h = P_concordance_m.wrap(aW, aH)
    P_concordance_m.drawOn(canv, alignement_col_gauche, aH - h)

    w, h = P_nb_Nconta.wrap(aW, aH)
    P_nb_Nconta.drawOn(canv, alignement_col_centre, aH - h)

    if Concordance_mf == "OUI" and Concordance_pf == "NON":
        w, h = P_seuil_m.wrap(aW, aH)
        P_seuil_m.drawOn(canv, 505, aH - h)
    elif Concordance_mf == "OUI":
        w, h = P_seuil_m.wrap(aW, aH)
        P_seuil_m.drawOn(canv, alignement_col_droite, aH - h)

    aH = aH - (h + 10)
    if Concordance_pf != "ABS":
        w, h = P_concordance_p.wrap(aW, aH)
        P_concordance_p.drawOn(canv, alignement_col_gauche, aH - h)

    w, h = P_nb_conta.wrap(aW, aH)
    P_nb_conta.drawOn(canv, alignement_col_centre, aH - (h - 10))

    if Concordance_mf == "OUI" and Concordance_pf == "NON":
        w, h = P_seuil_h.wrap(aW, aH)
        P_seuil_h.drawOn(canv, 505, aH - (h - 10))
    elif Concordance_mf == "OUI":
        w, h = P_seuil_h.wrap(aW, aH)
        P_seuil_h.drawOn(canv, alignement_col_droite, aH - (h - 10))

    aH = aH - h
    w, h = P_moy.wrap(aW, aH)
    P_moy.drawOn(canv, alignement_col_centre, aH - (h - 10))

    aH = aH - 5
    w, h = P_conta_echantillon.wrap(aW, aH)
    P_conta_echantillon.drawOn(canv, alignement_col_gauche, aH - h)

    if Concordance_mf == "NON":
        aH = aH - (h * 2 + 2)
        Par.drawOn(canv, alignement_col_gauche, aH)
        aH = aH - h
        w, h = P_seuil_m.wrap(aW, aH)
        P_seuil_m.drawOn(canv, alignement_col_gauche + 4, aH)

        aH = aH - h
        w, h = P_seuil_h.wrap(aW, aH)
        P_seuil_h.drawOn(canv, alignement_col_gauche + 4, aH)

    canv.save()


def creation_PDF(path, nom_projet, nom_fichier_mere, nom_fichier_foetus, nom_fichier_pere, nom_pdf, Sexe, dataframe,
                 det_dataframe, choix_utilisateur, nom_utilisateur, seuil_pic, seuil_marqueur, seuil_pourcentage,
                 presence_pere, Entite_d_Application, Emetteur, version):
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

    nom, nb_mere, nb_foetus, nb_pere, date, Sexe, Concordance_mf, Concordance_pf, Contamination, nb_info_Nconta, nb_info_Conta, moy_conta = def_variable(
        nom_projet, nom_fichier_mere, nom_fichier_foetus, nom_fichier_pere, Sexe, dataframe, det_dataframe,
        choix_utilisateur, nom_utilisateur, presence_pere)

    canv = init_pdf(path, nom_pdf, Concordance_mf, Concordance_pf)

    CHU_HEADER, HEADER, data = creat_struct_pdf(Concordance_mf, Concordance_pf, Entite_d_Application, Emetteur, version)

    l_info = resultats(data, dataframe, Concordance_mf, Concordance_pf)

    t = style_result(data, Concordance_mf, Concordance_pf, l_info)

    disposition_pdf(CHU_HEADER, HEADER, nom_utilisateur, t, canv, Concordance_mf, Concordance_pf, Contamination,
                    nb_info_Nconta, nb_info_Conta, moy_conta, nom, nb_mere, nb_foetus, nb_pere, date, Sexe, seuil_pic,
                    seuil_marqueur, seuil_pourcentage)


if __name__ == "__main__":
    from Traitement2 import *

    n_conc = "exemple_absence_totale_concordance.txt"
    ex_non_conta = "PP16_XFra_FAURE_290119_PP16.txt"
    ex_conta = "2018-03-27 foetus 90-10_PP16.txt"
    ex = ""
    ex_n_conc_pere = "non_concordance_pere.txt"
    ex_n_conc_mere = "181985_xfra_ja_200618_PP16.txt"
    M, F, P, Echantillon_F = lecture_fichier(ex_n_conc_mere)

    path = ""
    dataframe, det_dataframe = Echantillon_F.analyse_donnees(M, F, P)
    nom_projet = "ex_abs_concord_mere_pere_abs"
    nom_fichier_mere = "mere"
    nom_fichier_foetus = "foetus"
    nom_fichier_pere = "pere"
    date = "01/01/1999"
    Sexe = "I"
    path = ""
    nom_utilisateur = "Nom prénom"
    choix_utilisateur = 0
    nom_pdf = nom_projet + "_" + nom_utilisateur
    seuil_pic = 42
    seuil_marqueur = 4
    seuil_pourcentage = 0.42
    presence_pere = "ABS"
    Entite_d_Application = "-  - SEQUENCEUR"
    Emetteur = "  PTBM -  -"
    version = "V.1"
    creation_PDF(path, nom_projet, nom_fichier_mere, nom_fichier_foetus, nom_fichier_pere, nom_pdf, Sexe, dataframe,
                 det_dataframe, choix_utilisateur, nom_utilisateur, seuil_pic, seuil_marqueur, seuil_pourcentage,
                 presence_pere, Entite_d_Application, Emetteur, version)
