# coding: utf-8

# version application 1.0


import Traitement2
import pdf_feuille_resultat

import os
import sys
import kivy
import logging
import copy

from datetime import datetime
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import *
from kivy.uix.button import Button
from kivy.factory import Factory
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import ListProperty, NumericProperty
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.animation import Animation
from kivy.graphics.instructions import CanvasBase
from kivy.graphics import *
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.utils import platform

kivy.require('1.10.1')
Window.clearcolor = (0.949, 0.945, 0.945, 1)
Window.size = (850, 650)
Window.minimum_width = 800
Window.minimum_height = (Window.minimum_width)/1.44



heure = datetime.now()
heure_vrai = heure.strftime("%d-%m-%Y_%Hh_%Mm")
logging.basicConfig(filename='log_' + heure_vrai + '.txt', filemode='w', format='%(name)s - %(levelname)s: %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ScreenManagement(ScreenManager):
    pass


class EcranPremier(Screen):
    def show_load(self, nom_utilisateur):
        try:
            self.manager.get_screen('ecran_principale').ids.ecranMethod.show_load()
            self.manager.get_screen('ecran_principale').ids.ecranMethod.InfoParametre["nom_utilisateur"] = str(
                nom_utilisateur)
        except Exception as e:
            logger.error("Chargement écran échoué", exc_info=True)
            return

        logger.info("Changment d'écran réussi")


class EcranFct(Screen):
    pass


class TableOnglets(TabbedPanel):
    # override tab switching method to animate on tab switch
    def switch_to(self, header):
        anim = Animation(opacity=0, d=.24, t='in_out_quad')

        def start_anim(_anim, child, in_complete, *lt):
            _anim.start(child)

        def _on_complete(*lt):
            if header.content:
                header.content.opacity = 0
                anim = Animation(opacity=1, d=.20, t='in_out_quad')
                start_anim(anim, header.content, True)
            super(TableOnglets, self).switch_to(header)

        anim.bind(on_complete=_on_complete)
        if self.current_tab.content:
            start_anim(anim, self.current_tab.content, False)
        else:
            _on_complete()


class CloseableHeader(TabbedPanelHeader):
    panel = ObjectProperty(None)
    text1 = ObjectProperty(None)
    supr_onglets = ObjectProperty(None)


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    retour = ObjectProperty(None)
    ecran = ObjectProperty(None)
    path = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(LoadDialog, self).__init__(**kwargs)
        self.ids.drives_list.adapter.bind(on_selection_change=self.drive_selection_changed)

    def get_win_drives(self):
        if platform == 'win':
            import win32api

            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]

            return drives
        else:
            return []

    def drive_selection_changed(self, *args):
        selected_item = args[0].selection[0].text
        self.ids.file_chooser.path = selected_item


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    nom_pdf = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)
    path = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SaveDialog, self).__init__(**kwargs)
        self.ids.drives_list.adapter.bind(on_selection_change=self.drive_selection_changed)

    def get_win_drives(self):
        if platform == 'win':
            import win32api

            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]

            return drives
        else:
            return []

    def drive_selection_changed(self, *args):
        selected_item = args[0].selection[0].text
        self.ids.file_chooser.path = selected_item


class ParametreDialog(FloatLayout):
    save_parametres = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)
    hauteur = ObjectProperty(None)
    nb = ObjectProperty(None)
    emetteur = ObjectProperty(None)
    entite = ObjectProperty(None)
    reinit_para = ObjectProperty(None)


class InfosConclusion(BoxLayout):
    TLigneInfo1 = ObjectProperty(None)
    TLigneInfo2 = ObjectProperty(None)
    TLigneInfo3 = ObjectProperty(None)


class ConcordanceEtSexe(BoxLayout):
    info_sexe = ObjectProperty(None)
    conco_M = ObjectProperty(None)
    conco_P = ObjectProperty(None)
    colorconcoM = ListProperty((256, 256, 256, 1))
    colorconcoP = ListProperty((256, 256, 256, 1))


class LigneTableau(BoxLayout):
    t_col1 = ObjectProperty(None)
    t_col2 = ObjectProperty(None)
    t_col3 = ObjectProperty(None)
    color_mode = ObjectProperty(None)
    color_text = ListProperty((256, 256, 256, 1))
    color_text2 = ListProperty((256, 256, 256, 1))
    large = ObjectProperty(None)


class ResAnalyse(BoxLayout):
    titre = ObjectProperty(None)
    NvGroupe = ObjectProperty(None)
    show_save = ObjectProperty(None)
    colorconcoM = (256, 256, 256, 1)
    colorconcoP = (256, 256, 256, 1)
    SaveLog = ObjectProperty(None)
    down_button = ObjectProperty(None)
    InfoParametre = {}
    filename = ""
    path = ""

    def attribut(self, InfoParametre):
        self.InfoParametre = copy.copy(InfoParametre)

    def remplissage(self, contamination, Echantillon_F):
        tableau_df = self.InfoParametre["df_conclusion"]
        conclusion = self.InfoParametre["df_detail"]
        try:
            if (Echantillon_F.get_concordance_mere_foet() == 'NON'):
                self.colorconcoM = colortext = (241 / 256, 31 / 256, 82 / 256, 1)
            if (Echantillon_F.get_concordance_pere_foet() == 'NON'):
                self.colorconcoP = colortext = (241 / 256, 31 / 256, 82 / 256, 1)
            BoxConcordance = ConcordanceEtSexe(info_sexe="Sexe foetus : " + Echantillon_F.get_sexe(),
                                               conco_M=Echantillon_F.get_concordance_mere_foet(),
                                               conco_P=Echantillon_F.get_concordance_pere_foet(),
                                               colorconcoM=self.colorconcoM,
                                               colorconcoP=self.colorconcoP)
            self.ids.TitreEtConco.add_widget(BoxConcordance)

            if (Echantillon_F.get_concordance_mere_foet() == "OUI"):
                entete = LigneTableau(t_col1="Marqueurs",
                                      t_col2="Conclusions",
                                      t_col3="Détails",
                                      color_mode=(75 / 255, 127 / 255, 209 / 255, 1),
                                      color_text=(0.949, 0.945, 0.945, 1),
                                      color_text2=(0.949, 0.945, 0.945, 1))
                if (contamination == 1):
                    self.ids.TButtonContamine.state = 'down'

                else:
                    self.ids.TButtonNonContamine.state = 'down'
                self.ids.le_tableau.add_widget(entete)

                parti_conclu = InfosConclusion(
                    TLigneInfo1="Nombre de marqueurs informatifs non contaminés: " + str(conclusion["1"][0]),
                    TLigneInfo2="Nombre de marqueurs informatifs contaminés: " + str(conclusion["1"][1]),
                    TLigneInfo3="Moyenne du pourcentage de contamination: " + str(conclusion["1"][2])
                    )
                self.ids.ensemble_info.add_widget(parti_conclu)

                for i in range(len(tableau_df.index)):
                    colortext = (256, 256, 256, 1)
                    colmode = (49 / 255, 140 / 255, 231 / 255, 0.2)
                    if (tableau_df["Conclusion"][i] == 'Non contaminé'):
                        colortext = (23 / 256, 116 / 256, 10 / 256, 1)
                    if (tableau_df["Conclusion"][i] == 'Contaminé'):
                        colortext = (241 / 256, 31 / 256, 82 / 256, 1)
                    if (i % 2 == 0):
                        colmode = (0.949, 0.945, 0.945, 0.2)
                    ligne = LigneTableau(t_col1=tableau_df["Marqueur"][i],
                                         t_col2=tableau_df["Conclusion"][i],
                                         t_col3=tableau_df["Détails M/F"][i],
                                         color_mode=colmode,
                                         color_text2=colortext)
                    self.ids.le_tableau.add_widget(ligne)
            else:
                if (
                        Echantillon_F.get_concordance_pere_foet() == "OUI" or Echantillon_F.get_concordance_pere_foet() == "ABS"):
                    entete = LigneTableau(t_col1="Marqueurs",
                                          t_col2="Concordance Mere/Foetus",
                                          t_col3="Détails",
                                          color_mode=(75 / 255, 127 / 255, 209 / 255, 1),
                                          color_text=(0.949, 0.945, 0.945, 1),
                                          color_text2=(0.949, 0.945, 0.945, 1)
                                          )
                    self.ids.le_tableau.add_widget(entete)

                    parti_conclu = InfosConclusion(TLigneInfo1="Non calculé",
                                                   TLigneInfo2="Non calculé",
                                                   TLigneInfo3="Non calculé")
                    self.ids.ensemble_info.add_widget(parti_conclu)
                    self.ids.togglebutonEtLabel.clear_widgets()
                    new_label = Label(text="Analyse non-réalisée", color=(241 / 256, 31 / 256, 82 / 256, 1),
                                      font_size=30)
                    self.ids.togglebutonEtLabel.add_widget(new_label)
                    self.ids.labelPrelev.font_size = 30
                    self.ids.labelPrelev.color = (241 / 256, 31 / 256, 82 / 256, 1)

                    for i in range(len(tableau_df.index)):
                        colortext = (256, 256, 256, 1)
                        colmode = (49 / 255, 140 / 255, 231 / 255, 0.2)
                        if (tableau_df["Concordance Mere/Foetus"][i] == 'NON'):
                            colortext = (241 / 256, 31 / 256, 82 / 256, 1)
                        if (i % 2 == 0):
                            colmode = (0.949, 0.945, 0.945, 0.2)
                        ligne = LigneTableau(t_col1=tableau_df["Marqueur"][i],
                                             t_col2=tableau_df["Concordance Mere/Foetus"][i],
                                             t_col3=tableau_df["Détails M/F"][i],
                                             color_mode=colmode,
                                             color_text2=colortext)
                        self.ids.le_tableau.add_widget(ligne)


                else:
                    entete = LigneTableau(t_col1="Marqueurs",
                                          t_col2="Concordance Mere/Foetus",
                                          t_col3="Détails M/F", color_mode=(75 / 255, 127 / 255, 209 / 255, 1),
                                          color_text=(0.949, 0.945, 0.945, 1),
                                          color_text2=(0.949, 0.945, 0.945, 1),
                                          large=0.20)

                    col4 = Label(text="Concordance Pere/Foetus", color=(0.949, 0.945, 0.945, 1))
                    col5 = Label(text="Détails P/F", color=(0.949, 0.945, 0.945, 1))
                    entete.add_widget(col4)
                    entete.add_widget(col5)
                    self.ids.le_tableau.add_widget(entete)

                    parti_conclu = InfosConclusion(TLigneInfo1="Non calculé",
                                                   TLigneInfo2="Non calculé",
                                                   TLigneInfo3="Non calculé")
                    self.ids.ensemble_info.add_widget(parti_conclu)
                    self.ids.togglebutonEtLabel.clear_widgets()
                    new_label = Label(text="Analyse non-réalisée", color=(241 / 256, 31 / 256, 82 / 256, 1),
                                      font_size=30)
                    self.ids.togglebutonEtLabel.add_widget(new_label)
                    self.ids.labelPrelev.font_size = 30
                    self.ids.labelPrelev.color = (241 / 256, 31 / 256, 82 / 256, 1)

                    for i in range(len(tableau_df.index)):
                        if (tableau_df["Concordance Mere/Foetus"][i] == 'NON'):
                            for i in range(len(tableau_df.index)):
                                colortext = (256, 256, 256, 1)
                                colmode = (49 / 255, 140 / 255, 231 / 255, 0.2)
                                if (tableau_df["Concordance Mere/Foetus"][i] == 'NON'):
                                    colortext = (241 / 256, 31 / 256, 82 / 256, 1)
                                if (i % 2 == 0):
                                    colmode = (0.949, 0.945, 0.945, 0.2)
                                ligne = LigneTableau(t_col1=tableau_df["Marqueur"][i],
                                                     t_col2=tableau_df["Concordance Mere/Foetus"][i],
                                                     t_col3=tableau_df["Détails M/F"][i],
                                                     color_mode=colmode,
                                                     color_text2=colortext)
                                col4 = Label(text=tableau_df["Concordance Pere/Foetus"][i], color=(256, 256, 256, 1))
                                col5 = Label(text=tableau_df["Détails P/F"][i], color=(256, 256, 256, 1), font_size=12)
                                ligne.add_widget(col4)
                                ligne.add_widget(col5)

                                self.ids.le_tableau.add_widget(ligne)


        except Exception as e:
            logger.error("Remplissage de la page échouée", exc_info=True)
        logger.info("Remplissage de la page réussi")

    def CouleurBouton(self, id):

        if (id == 0):
            self.ids.TButtonNonContamine.background_color = (75 / 255, 127 / 255, 209 / 255, 1)
            self.ids.TButtonNonContamine.color = [0.949, 0.945, 0.945, 1]
            self.ids.TButtonContamine.background_color = (220 / 255, 220 / 255, 220 / 255, 1)
            self.ids.TButtonContamine.color = [130 / 256, 130 / 256, 130 / 256, 1]
        else:
            self.ids.TButtonContamine.background_color = (75 / 255, 127 / 255, 209 / 255, 1)
            self.ids.TButtonContamine.color = [0.949, 0.945, 0.945, 1]
            self.ids.TButtonNonContamine.background_color = (220 / 255, 220 / 255, 220 / 255, 1)
            self.ids.TButtonNonContamine.color = [130 / 256, 130 / 256, 130 / 256, 1]


class EcranFctMethod(GridLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    hauteur = "1/3"
    conta = 5
    nb = 2
    InfoParametre = {}
    nb_header = 0
    choix = 0
    retour = False
    cpt = 0
    InfoParametre["choix"]=None
    emetteur = "PBP-P2A-GEN"
    entite = "PBP-PTBM"
    instance_path = os.path.join(os.environ["HOMEPATH"], "Desktop")

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        """  Display a pop up windows with the FileChooser for loading purpose
                        """

        self.hauteur = "1/3"
        self.nb = 2
        # ppath=os.path.join(os.environ["HOMEPATH"], "Desktop")
        ppath = self.instance_path
        contenu = LoadDialog(load=self.load, cancel=self.dismiss_popup, ecran=self, path=ppath)
        self._popup = Popup(title='Ouvrir un fichier', content=contenu, size_hint=(0.9, 0.9))
        self._popup.open()
        if (self.retour):
            return True

    def retour_conclusion(self, retour):
        self.retour = retour

    def load(self, path, filename):
        """ Call the functions and methods from Traitement2 with default parameters, path and filename
                chose by user. Gather result from them and put it in attributes of an instance of ResAnalyse
                """
        try:
            # lecture du fichier et traitement
            M, F, P, Echantillon_F = Traitement2.lecture_fichier(os.path.join(path, filename[0]))
            logger.info("fonction lecture fichier réussi")
            Echantillon_F.set_seuil_hauteur(eval(self.hauteur))
            Echantillon_F.set_seuil_nbre_marqueurs(float(self.nb))
            logger.info("Attribution des taux réussi")
            resultats, conclusion = Echantillon_F.analyse_donnees(M, F, P)
            logger.info("Fonction analyse_données réussi")
            # récupération et attribution de données
            self.titre = Echantillon_F.get_name()
            self.instance_path = path
            nv_onglets = CloseableHeader(text1=self.titre + "  ", panel=self.ids.les_onglets,
                                         supr_onglets=self.supr_onglets)
            contenu_res = ResAnalyse(
                titre=self.titre + "\n" + "\n",
                NvGroupe=len(self.ids.les_onglets.tab_list),
                show_save=self.show_save,
                down_button=self.down_button)
            self.InfoParametre["Sexe"] = Echantillon_F.get_sexe()
            self.InfoParametre["df_conclusion"] = resultats
            self.InfoParametre["df_detail"] = conclusion
            self.InfoParametre["code_conclu"] = Echantillon_F.get_conclusion()
            print(Echantillon_F.get_conclusion())
            self.InfoParametre["nom_projet"] = Echantillon_F.get_name()
            self.InfoParametre["Emetteur"] = self.emetteur
            self.InfoParametre["Entite_appli"] = self.entite
            self.InfoParametre["nom_pdf"] = Echantillon_F.get_name() + "_" + self.InfoParametre["nom_utilisateur"]
            self.InfoParametre["Version"] = str(version)
            logger.info("Récupération des données réussi")
            if (Echantillon_F.get_concordance_pere_foet() == "ABS"):
                self.InfoParametre["num_pere"] = "ABS"
                self.InfoParametre["pres_pere"] = "ABS"
            else:
                self.InfoParametre["num_pere"] = P[0].get_num_pere()
                self.InfoParametre["pres_pere"] = "OUI"
            self.InfoParametre["num_foetus"] = F[0].get_num_foetus()
            self.InfoParametre["filename"] = filename
            self.InfoParametre["path"] = path
            self.InfoParametre["nb"] = self.nb
            self.InfoParametre["hauteur"] = self.hauteur
            contenu_res.attribut(self.InfoParametre)
            contenu_res.remplissage(Echantillon_F.get_conclusion(),
                                    Echantillon_F)
            self.content = contenu_res
            nv_onglets.content = self.content

            self.ids.les_onglets.add_widget(nv_onglets)
            self.ids.les_onglets.switch_to(nv_onglets)
            self.dismiss_popup()
            self.cpt = self.cpt + 1

        except Exception as e:

            logger.error("Chargement données/Traitement impossible", exc_info=True)

            return False
        logger.info("Chargement et traitement des données réussi")

        return True

    def change_onglets(self):
        if (len(self.ids.les_onglets.get_tab_list()) != 0):
            self.ids.les_onglets.switch_to(self.ids.les_onglets.get_tab_list()[0])
        else:
            self.panel.manager.current = "EcranAccueil"
            self.retour = False

    def supr_onglets(self, id):

        self.ids.les_onglets.remove_widget(id)
        self.change_onglets()

    def show_save(self):
        """  Display a pop up windows with the FileChooser for saving purpose
                                """

        content = SaveDialog(save=self.save, cancel=self.dismiss_popup, path=self.instance_path,
                             nom_pdf=self.ids.les_onglets.current_tab.content.InfoParametre["nom_pdf"])

        self._popup = Popup(title="Sauvegarder un  fichier", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path, filename):
        """  Call function for creating pdf and test if the autmatic conclusion have been changed
                                     """
        conclu = 0
        self.instance_path = path
        try:
            if (self.ids.les_onglets.current_tab.content.InfoParametre["choix"] == 0 and self.ids.les_onglets.current_tab.content.InfoParametre["code_conclu"] == 0):
                conclu = 0
            elif (self.ids.les_onglets.current_tab.content.InfoParametre["choix"] == 1 and self.ids.les_onglets.current_tab.content.InfoParametre["code_conclu"] == 1):
                conclu = 1
            elif (self.ids.les_onglets.current_tab.content.InfoParametre["choix"]== 0 and self.ids.les_onglets.current_tab.content.InfoParametre["code_conclu"] == 1):
                conclu = 2
            elif (self.ids.les_onglets.current_tab.content.InfoParametre["choix"]== 1 and self.ids.les_onglets.current_tab.content.InfoParametre["code_conclu"] == 0):
                conclu = 3
            else:
                conclu=self.ids.les_onglets.current_tab.content.InfoParametre["code_conclu"]
        except Exception as e:
            logger.error("Echec atribution varaible conclu", exc_info=True)
            return


        try:
            pdf_feuille_resultat.creation_PDF(os.path.join(path),
                                              self.ids.les_onglets.current_tab.content.InfoParametre["nom_projet"],
                                              self.ids.les_onglets.current_tab.content.InfoParametre["nom_projet"],
                                              self.ids.les_onglets.current_tab.content.InfoParametre["num_foetus"],
                                              self.ids.les_onglets.current_tab.content.InfoParametre["num_pere"],
                                              filename,
                                              self.ids.les_onglets.current_tab.content.InfoParametre["Sexe"],
                                              self.ids.les_onglets.current_tab.content.InfoParametre["df_conclusion"],
                                              self.ids.les_onglets.current_tab.content.InfoParametre["df_detail"],
                                              conclu,
                                              self.InfoParametre["nom_utilisateur"],
                                              self.ids.les_onglets.current_tab.content.InfoParametre["hauteur"],
                                              self.ids.les_onglets.current_tab.content.InfoParametre["nb"],
                                              None,
                                              self.ids.les_onglets.current_tab.content.InfoParametre["pres_pere"],
                                              self.ids.les_onglets.current_tab.content.InfoParametre["Entite_appli"],
                                              self.ids.les_onglets.current_tab.content.InfoParametre["Emetteur"],
                                              self.ids.les_onglets.current_tab.content.InfoParametre["Version"])
            self.dismiss_popup()
        except Exception as e:
            logger.error("Echec lancement créaton pdf", exc_info=True)
            return
        logger.info("Création pdf réussi")
        if platform == 'linux':
            os.system("xdg-open " + os.path.join(path + filename) + ".pdf")
        else:
            os.system('start ' + path + "\\" + filename + ".pdf")

    def down_button(self, num):

        self.ids.les_onglets.current_tab.content.InfoParametre["choix"] = num

    def ouverture_parametres(self):
        """  Display a pop up windows with the parameters
                                        """
        try:
            content = ParametreDialog(hauteur=str(self.ids.les_onglets.current_tab.content.InfoParametre["hauteur"]),
                                      nb=str(self.ids.les_onglets.current_tab.content.InfoParametre["nb"]),
                                      save_parametres=self.save_parametres,
                                      emetteur=self.ids.les_onglets.current_tab.content.InfoParametre["Emetteur"],
                                      entite=self.ids.les_onglets.current_tab.content.InfoParametre["Entite_appli"],
                                      cancel=self.dismiss_popup)
            self._popup = Popup(title="Modifier des parametres",
                                content=content,
                                size_hint=(0.9, 0.9))
            self._popup.open()
        except Exception as e:
            logger.error("Ouverture paramétre impossible", exc_info=True)
            return
        logger.info("Ouverture paramètre réussi")

    def save_parametres(self, p1, p3, p4, p5):
        """  The new parameters of the analysis are put in temp attributes(EcranFctmethod's attributes)
                and a new analysis is started(load method)
                                        """
        try:
            self.nb = p1
            self.hauteur = p3
            self.emetteur = p4
            self.entite = p5
            self.load(self.ids.les_onglets.current_tab.content.InfoParametre["path"],
                      self.ids.les_onglets.current_tab.content.InfoParametre["filename"])
            self.dismiss_popup()
        except Exception as e:
            logger.error("Changement paramètres échoué nb(attendu)=entier,nb(indiqué)= " + str(
                p1) + ", hauteur(attendu)=entier ou fraction,hauteur(indiqué)=" + str(p3), exc_info=True)
            return
        logger.info("Changement paramètres réussi")

    def quitter(self):
        sys.exit(0)


class MyApp(App):
    """It's the main Class application, kivy detect kv file automatically with a name in lowercase
        which is before the word App in the name of this class
        , example: MyApp will detect a the kv file my.kv or TestApp
        will detect the kv file test.kv
                                """

    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    title = 'LACFoM'

    def build(self):
        self.icon = 'logo.png'


"""Factory register is for communicating name's Classes to the kv file
                                """

Factory.register('ResAnalyse', cls=ResAnalyse)
Factory.register('EcranPremier', cls=EcranPremier)
Factory.register('EcranFct', cls=EcranFct)
Factory.register('EcranFctMethod', cls=EcranFctMethod)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)
Factory.register('ParametreDialog', cls=ParametreDialog)
Factory.register('LigneTableau', cls=LigneTableau)
Factory.register('InfosConclusion', cls=InfosConclusion)
Factory.register('ConcordanceEtSexe', cls=ConcordanceEtSexe)
Factory.register('CloseableHeader', cls=CloseableHeader)
if __name__ == '__main__':
    version = 1.0
    app = MyApp()
    app.run()
