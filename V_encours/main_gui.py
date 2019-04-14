#coding: utf-8

#version application 0.2
import kivy

import Traitement2
import pdf_feuille_resultat

from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.lang  import Builder

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
from kivy.graphics.instructions import CanvasBase
from kivy.graphics import *



import pandas as pd
import os

import sys


kivy.require('1.10.1')
Window.clearcolor = (0.949, 0.945, 0.945, 1)
Window.size = (1000,800)


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class ParametreDialog(FloatLayout):
    save_parametres=ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)
    hauteur= ObjectProperty(None)
    nb= ObjectProperty(None)
    conta= ObjectProperty(None)

class TableOnglets(TabbedPanel):
    pass


class EcranPremier(Screen):
    def show_load(self):

        self.manager.get_screen('ecran_principale').ids.ecranMethod.show_load()



class EcranFct(Screen):
    pass
class InfosConclusion(BoxLayout):
    TLigneInfo1= ObjectProperty(None)
    TLigneInfo2= ObjectProperty(None)
    TLigneInfo3= ObjectProperty(None)
    pass
   
    
class LigneTableau(BoxLayout):
    t_col1 = ObjectProperty(None)
    t_col2 = ObjectProperty(None)
    t_col3 = ObjectProperty(None)
    color_mode=ObjectProperty(None)
    color_text=ListProperty((256, 256, 256, 1))
   
    pass
class ResAnalyse(BoxLayout):
    titre =ObjectProperty(None)
    NvGroupe = ObjectProperty(None)
    show_save=ObjectProperty(None)
    
    

    def remplissage(self,tableau_df,conclusion,contamination):
        print(tableau_df)
        print(conclusion)
        entete=LigneTableau(t_col1="Marqueur",t_col2="Conclusion",t_col3="Détails",color_mode=(75/255, 127/255, 209/255,1),color_text=(0.949, 0.945, 0.945, 1))
        if(contamination==1):
            self.ids.TButtonContamine.state='down'
        else:
            self.ids.TButtonNonContamine.state='down'
        self.ids.le_tableau.add_widget(entete)
        parti_conclu=InfosConclusion(TLigneInfo1="Marqueurs informatifs non contaminés: "+str(conclusion["1"][0]),TLigneInfo2="Marqueurs informatifs contaminés: "+str(conclusion["1"][1]),TLigneInfo3="Moyenne du pourcentage de contamination: "+str(conclusion["1"][2]))
        self.ids.ensemble_info.add_widget(parti_conclu)
        
        
        for i in range(len(tableau_df.index)):
            if (i%2 == 0):

                ligne=LigneTableau(t_col1=tableau_df["Marqueur"][i], t_col2=tableau_df["Conclusion"][i],t_col3=tableau_df["Détails M/F"][i],color_mode=(0.949, 0.945, 0.945, 0.2))

                self.ids.le_tableau.add_widget(ligne)
            else:
                ligne=LigneTableau(t_col1=tableau_df["Marqueur"][i], t_col2=tableau_df["Conclusion"][i],t_col3=tableau_df["Détails M/F"][i],color_mode=(49/255, 140/255, 231/255,0.2))

                self.ids.le_tableau.add_widget(ligne)
    
    
   
    def dismiss_popup(self):
        self._popup.dismiss()


class EcranFctMethod(GridLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    hauteur=1/3
    conta=0.05
    nb=2
    InfoParametre={}
    
    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        contenu=LoadDialog(load=self.load,cancel=self.dismiss_popup)
        self._popup = Popup(title='Ouvrir un fichier', content=contenu,  size_hint=(0.9, 0.9))
        self._popup.open()

        
    def load(self, path, filename):
        #TODO faire afficahege tableau différents selon concordance, utilisé get_concordance_mere_foetus et pareil pour pere

        #traitement du fichier
        M, F, P, Echantillon_F, log = Traitement2.lecture_fichier(os.path.join(path, filename[0]))
        resultats, conclusion, log = Echantillon_F.analyse_donnees(M, F,P, log)

        #récupération et attribution de données
        self.InfoParametre["Sexe"]=Echantillon_F.get_sexe()
        self.InfoParametre["df_conclusion"]=resultats
        self.InfoParametre["df_detail"]=conclusion
        self.InfoParametre["code_conclu"]=Echantillon_F.get_conclusion()
        self.titre = "Echantillon: " + Echantillon_F.get_name()

        print(os.path.join(path, filename[0]))
        
       
        Echantillon_F.set_seuil_hauteur(self.hauteur)
        Echantillon_F.set_seuil_taux_conta(self.conta)
        Echantillon_F.set_seuil_nbre_marqueurs(self.nb)

        
        nv_onglets = TabbedPanelHeader(text=self.titre,background_color=(75*3/255, 127*3/255, 209*3/255,1))
        contenu_res = ResAnalyse(
            titre=self.titre + "\n" + "\n", 
            NvGroupe=len(self.ids.les_onglets.tab_list),
            show_save=self.show_save)
        contenu_res.remplissage(self.InfoParametre["df_conclusion"], self.InfoParametre["df_detail"],Echantillon_F.get_conclusion())
        nv_onglets.content = contenu_res
        
        
        self.ids.les_onglets.add_widget(nv_onglets)
        self.ids.les_onglets.switch_to(nv_onglets, do_scroll=True)
        self.dismiss_popup()

    
    def show_save(self):
        
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Sauvegarder un  fichier", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path, filename):
        
        pdf_feuille_resultat.creation_PDF(os.path.join(path, filename),"TODO","TODO","TODO","TODO",self.InfoParametre["Sexe"],self.InfoParametre["df_conclusion"],self.InfoParametre["df_detail"],self.InfoParametre["code_conclu"])#nom_projet, nom_fichier_mere, nom_fichier_foetus, nom_fichier_pere, Sexe, dataframe, det_dataframe, choix_utilisateur
        self.dismiss_popup()
        

    

    def ouverture_parametres(self):
        content = ParametreDialog( hauteur=str(self.hauteur),nb=str(self.nb),conta=str(self.conta),save_parametres=self.save_parametres,cancel=self.dismiss_popup)
        self._popup = Popup(title="Modifier des parametres", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
    


    def save_parametres(self,p1,p2,p3):
        self.nb= float(p1)
        self.conta = float(p2)
        self.hauteur = float(eval(p3))
        
        self.dismiss_popup()

    def quitter(self):
       sys.exit(0)


class ScreenManagement(ScreenManager):
    pass       


class MyApp(App):
    
    title = 'DPN 3000'

    def build(self):
        self.icon = 'logo.png'
    
Factory.register('ResAnalyse', cls=ResAnalyse)
Factory.register('EcranPremier', cls=EcranPremier)    
Factory.register('EcranFct', cls=EcranFct)
Factory.register('EcranFctMethod', cls=EcranFctMethod)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)
Factory.register('ParametreDialog', cls=ParametreDialog)
Factory.register('LigneTableau', cls=LigneTableau)
Factory.register('InfosConclusion', cls=InfosConclusion)
if __name__ == '__main__':


    app= MyApp()
    app.run()
