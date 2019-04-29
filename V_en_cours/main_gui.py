#coding: utf-8

#version application 1.0


import Traitement2
import pdf_feuille_resultat
import pandas as pd
import os
import sys
import kivy

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
from kivy.animation import Animation
from kivy.graphics.instructions import CanvasBase
from kivy.graphics import *
from kivy.uix.behaviors import ToggleButtonBehavior


kivy.require('1.10.1')
Window.clearcolor = (0.949, 0.945, 0.945, 1)
Window.size = (850,650)
Window.minimum_width= 800
Window.minimum_height=550
class ScreenManagement(ScreenManager):
    pass 

class EcranPremier(Screen):
    def show_load(self,nom_utilisateur):

        self.manager.get_screen('ecran_principale').ids.ecranMethod.show_load()
        self.manager.get_screen('ecran_principale').ids.ecranMethod.InfoParametre["nom_utilisateur"]=str(nom_utilisateur)

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
    panel=ObjectProperty(None)
    text1=ObjectProperty(None)
    SuprOnglet=ObjectProperty(None)

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    Retourner=ObjectProperty(None)
    ecran=ObjectProperty(None)
class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    nom_pdf=ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)
    path=ObjectProperty("./")

class ParametreDialog(FloatLayout):
    save_parametres=ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)
    hauteur= ObjectProperty(None)
    nb= ObjectProperty(None)
    conta= ObjectProperty(None)
    emetteur=ObjectProperty(None)
    entite=ObjectProperty(None)
    reinit_para=ObjectProperty(None)



class InfosConclusion(BoxLayout):
    TLigneInfo1= ObjectProperty(None)
    TLigneInfo2= ObjectProperty(None)
    TLigneInfo3= ObjectProperty(None)


class ConcordanceEtSexe(BoxLayout):
    info_sexe= ObjectProperty(None)
    conco_M= ObjectProperty(None)
    conco_P= ObjectProperty(None)
    colorconcoM= ListProperty((256, 256, 256, 1))
    colorconcoP= ListProperty((256, 256, 256, 1))
    

class LigneTableau(BoxLayout):
    t_col1 = ObjectProperty(None)
    t_col2 = ObjectProperty(None)
    t_col3 = ObjectProperty(None)
    color_mode=ObjectProperty(None)
    color_text=ListProperty((256, 256, 256, 1))
    color_text2=ListProperty((256, 256, 256, 1))
    large=ObjectProperty(None)


class ResAnalyse(BoxLayout):
    titre =ObjectProperty(None)
    NvGroupe = ObjectProperty(None)
    show_save=ObjectProperty(None)
    colorconcoM=(256, 256, 256, 1)
    colorconcoP=(256, 256, 256, 1)
    SaveLog=ObjectProperty(None)
    down_button=ObjectProperty(None)
    
    def remplissage(self,tableau_df,conclusion,contamination,Echantillon_F):
        
        if(Echantillon_F.get_concordance_mere_foet()=='NON'):
            self.colorconcoM=colortext=(241/256,31/256,82/256,1)
        if(Echantillon_F.get_concordance_pere_foet()=='NON'):
            self.colorconcoP=colortext=(241/256,31/256,82/256,1)
        BoxConcordance=ConcordanceEtSexe(info_sexe="Sexe foetus : "+Echantillon_F.get_sexe(),
                                        conco_M=Echantillon_F.get_concordance_mere_foet(),
                                        conco_P=Echantillon_F.get_concordance_pere_foet(),
                                        colorconcoM=self.colorconcoM,
                                        colorconcoP=self.colorconcoP)
        self.ids.TitreEtConco.add_widget(BoxConcordance)

        if(Echantillon_F.get_concordance_mere_foet()=="OUI"):
            entete=LigneTableau(t_col1="Marqueurs",
                                t_col2="Conclusion",
                                t_col3="Détails",
                                color_mode=(75/255, 127/255, 209/255,1),
                                color_text=(0.949, 0.945, 0.945, 1),
                                color_text2=(0.949, 0.945, 0.945, 1))
            if(contamination==1):
                self.ids.TButtonContamine.state='down'
                
            else:
                self.ids.TButtonNonContamine.state='down'
            self.ids.le_tableau.add_widget(entete)
            parti_conclu=InfosConclusion(TLigneInfo1="Marqueurs informatifs non contaminés: "+str(conclusion["1"][0]),
                                        TLigneInfo2="Marqueurs informatifs contaminés: "+str(conclusion["1"][1]),
                                        TLigneInfo3="Moyenne du pourcentage de contamination: "+str(conclusion["1"][2])
                                        )
            self.ids.ensemble_info.add_widget(parti_conclu)
            
            
            for i in range(len(tableau_df.index)):
                colortext=(256,256,256,1)
                if(tableau_df["Conclusion"][i]=='Non contaminé'):
                    colortext=(23/256,116/256,10/256,1)
                if(tableau_df["Conclusion"][i]=='Contaminé'):
                    colortext=(241/256,31/256,82/256,1)
                if (i%2 == 0):

                    ligne=LigneTableau(t_col1=tableau_df["Marqueur"][i], 
                                        t_col2=tableau_df["Conclusion"][i],
                                        t_col3=tableau_df["Détails M/F"][i],
                                        color_mode=(0.949, 0.945, 0.945, 0.2), 
                                        color_text2=colortext
                                       )

                    self.ids.le_tableau.add_widget(ligne)
                else:
                    ligne=LigneTableau(t_col1=tableau_df["Marqueur"][i], 
                                        t_col2=tableau_df["Conclusion"][i],
                                        t_col3=tableau_df["Détails M/F"][i],
                                        color_mode=(49/255, 140/255, 231/255,0.2), 
                                        color_text2=colortext
                                        )

                    self.ids.le_tableau.add_widget(ligne)
        else:
            if(Echantillon_F.get_concordance_pere_foet()=="OUI" or Echantillon_F.get_concordance_pere_foet()=="ABS" ):
                entete=LigneTableau(t_col1="Marqueurs",
                                    t_col2="Concordance Mere/Foetus",
                                    t_col3="Détails",
                                    color_mode=(75/255, 127/255, 209/255,1),
                                    color_text=(0.949, 0.945, 0.945, 1),
                                    color_text2=(0.949, 0.945, 0.945, 1)
                                    )
                self.ids.le_tableau.add_widget(entete)
                
                parti_conclu=InfosConclusion(TLigneInfo1="Marqueurs informatifs non contaminés: "+str(conclusion["1"][0]),
                                            TLigneInfo2="Marqueurs informatifs contaminés: "+str(conclusion["1"][1]),
                                            TLigneInfo3="Moyenne du pourcentage de contamination: "+str(conclusion["1"][2]))
                self.ids.ensemble_info.add_widget(parti_conclu)
                
                
                for i in range(len(tableau_df.index)):
                    colortext=(256,256,256,1)
                    if(tableau_df["Concordance Mere/Foetus"][i]=='NON'):
                        colortext=(241/256,31/256,82/256,1)
                    if (i%2 == 0):

                        ligne=LigneTableau(t_col1=tableau_df["Marqueur"][i], 
                                            t_col2=tableau_df["Concordance Mere/Foetus"][i],
                                            t_col3=tableau_df["Détails M/F"][i],
                                            color_mode=(0.949, 0.945, 0.945, 0.2), 
                                            color_text2=colortext)

                        self.ids.le_tableau.add_widget(ligne)
                    else:
                        ligne=LigneTableau(t_col1=tableau_df["Marqueur"][i], 
                                            t_col2=tableau_df["Concordance Mere/Foetus"][i],
                                            t_col3=tableau_df["Détails M/F"][i],
                                            color_mode=(49/255, 140/255, 231/255,0.2), 
                                            color_text2=colortext)

                        self.ids.le_tableau.add_widget(ligne)

            else:
                entete=LigneTableau(t_col1="Marqueurs",
                                    t_col2="Concordance Mere/Foetus",
                                    t_col3="Détails M/F",color_mode=(75/255, 127/255, 209/255,1),
                                    color_text=(0.949, 0.945, 0.945, 1),
                                    color_text2=(0.949, 0.945, 0.945, 1),
                                    large=0.20)
                
                col4=Label(text="Concordance Pere/Foetus",color=(0.949, 0.945, 0.945, 1))
                col5=Label(text="Détails P/F",color=(0.949, 0.945, 0.945, 1))
                entete.add_widget(col4)
                entete.add_widget(col5)
                self.ids.le_tableau.add_widget(entete)
                
                parti_conclu=InfosConclusion(TLigneInfo1="Marqueurs informatifs non contaminés: "+str(conclusion["1"][0]),
                                            TLigneInfo2="Marqueurs informatifs contaminés: "+str(conclusion["1"][1]),
                                            TLigneInfo3="Moyenne du pourcentage de contamination: "+str(conclusion["1"][2]))
                self.ids.ensemble_info.add_widget(parti_conclu)
                
                
                for i in range(len(tableau_df.index)):
                    colortext=(256,256,256,1)
                    if(tableau_df["Concordance Mere/Foetus"][i]=='NON'):
                        colortext=(241/256,31/256,82/256,1)
                    if (i%2 == 0):

                        ligne=LigneTableau(t_col1=tableau_df["Marqueur"][i], 
                                            t_col2=tableau_df["Concordance Mere/Foetus"][i],
                                            t_col3=tableau_df["Détails M/F"][i],
                                            color_mode=(0.949, 0.945, 0.945, 0.2), 
                                            color_text2=colortext,large=0.20)
                        col4=Label(text=tableau_df["Concordance Pere/Foetus"][i],color=(256,256,256,1))
                        col5=Label(text=tableau_df["Détails P/F"][i],color=(256,256,256,1))
                        ligne.add_widget(col4)
                        ligne.add_widget(col5)

                        
                        self.ids.le_tableau.add_widget(ligne)
                    else:
                        ligne=LigneTableau(t_col1=tableau_df["Marqueur"][i], 
                                            t_col2=tableau_df["Concordance Mere/Foetus"][i],
                                            t_col3=tableau_df["Détails M/F"][i],
                                            color_mode=(49/255, 140/255, 231/255,0.2), 
                                            color_text2=colortext,large=0.20)
                        col4=Label(text=tableau_df["Concordance Pere/Foetus"][i],color=(256,256,256,1))
                        col5=Label(text=tableau_df["Détails P/F"][i],color=(256,256,256,1))
                        ligne.add_widget(col4)
                        ligne.add_widget(col5)
                        
                        self.ids.le_tableau.add_widget(ligne)
    
                pass
            
    def CouleurBouton(self,id):
        
        if(id==0):
            self.ids.TButtonNonContamine.background_color=(75/255, 127/255, 209/255,1)
            self.ids.TButtonNonContamine.color=[0.949, 0.945, 0.945, 1]
            self.ids.TButtonContamine.background_color=(220/255, 220/255, 220/255,1)
            self.ids.TButtonContamine.color= [130/256, 130/256, 130/256, 1]
        else:
            self.ids.TButtonContamine.background_color=(75/255, 127/255, 209/255,1)
            self.ids.TButtonContamine.color=[0.949, 0.945, 0.945, 1]
            self.ids.TButtonNonContamine.background_color=(220/255, 220/255, 220/255,1)
            self.ids.TButtonNonContamine.color= [130/256, 130/256, 130/256, 1]



    def dismiss_popup(self):
        self._popup.dismiss()


class EcranFctMethod(GridLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    hauteur="1/3"
    conta=5
    nb=2
    InfoParametre={}
    nb_header=0
    choix=0
    retour=False
    

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        
        contenu=LoadDialog(load=self.load,cancel=self.dismiss_popup,Retourner=self.Retourner,ecran=self)
        self._popup = Popup(title='Ouvrir un fichier', content=contenu,  size_hint=(0.9, 0.9))
        self._popup.open()
        if(self.retour):
            return True
        
    def Retourner(self,retour):
        self.retour=retour

        
    def load(self, path, filename):
        #traitement du fichier
        try:
            M, F, P, Echantillon_F, log = Traitement2.lecture_fichier(os.path.join(path, filename[0]))
            
        
            Echantillon_F.set_seuil_hauteur(eval(self.hauteur))
            Echantillon_F.set_seuil_taux_conta(float(self.conta))
            Echantillon_F.set_seuil_nbre_marqueurs(float(self.nb))
            resultats, conclusion, log = Echantillon_F.analyse_donnees(M, F,P, log)

            #récupération et attribution de données
            self.InfoParametre["Sexe"]=Echantillon_F.get_sexe()
            self.InfoParametre["df_conclusion"]=resultats
            self.InfoParametre["df_detail"]=conclusion
            self.InfoParametre["code_conclu"]=Echantillon_F.get_conclusion()
            self.InfoParametre["nom_projet"] = Echantillon_F.get_name()
            self.InfoParametre["Emetteur"]=""
            self.InfoParametre["Entite_appli"]=""
            self.InfoParametre["nom_pdf"]= self.InfoParametre["nom_projet"]+"_"+self.InfoParametre["nom_utilisateur"]
            self.InfoParametre["Version"]=str(version)

            if(Echantillon_F.get_concordance_pere_foet() == "ABS"):
                self.InfoParametre["num_pere"] = "ABS"
                self.InfoParametre["pres_pere"] = "ABS"
            else:
                self.InfoParametre["num_pere"] = P[0].get_num_pere()
                self.InfoParametre["pres_pere"] = "OUI"
            self.InfoParametre["num_foetus"] = F[0].get_num_foetus()
            self.titre =  Echantillon_F.get_name()
            self.log=log
            
            nv_onglets = CloseableHeader(text1=self.titre +"  ",panel=self.ids.les_onglets,SuprOnglet=self.SuprOnglet)
            contenu_res = ResAnalyse(
                titre=self.titre + "\n" + "\n", 
                NvGroupe=len(self.ids.les_onglets.tab_list),
                show_save=self.show_save,
                SaveLog=self.SaveLog,
                down_button=self.down_button)
            contenu_res.remplissage(self.InfoParametre["df_conclusion"],
                                    self.InfoParametre["df_detail"],
                                    Echantillon_F.get_conclusion(),
                                    Echantillon_F)
            nv_onglets.content = contenu_res
            
            
            self.ids.les_onglets.add_widget(nv_onglets)
            self.ids.les_onglets.switch_to(nv_onglets)
            self.dismiss_popup()
            
        except ( KeyError,UnicodeDecodeError):
            print("Erreur lecture fichier")
            return False
        return True

    def ChangeOnglet(self):
        if(len(self.ids.les_onglets.get_tab_list())!=0):
            self.ids.les_onglets.switch_to(self.ids.les_onglets.get_tab_list()[0])
        else:
            self.panel.manager.current = "EcranAccueil"
            self.retour=False


    def SuprOnglet(self,id):
        
        self.ids.les_onglets.remove_widget(id)
        self.ChangeOnglet()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup,path=os.getcwd(),nom_pdf=self.InfoParametre["nom_pdf"])
        self._popup = Popup(title="Sauvegarder un  fichier", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path, filename):
        if (self.choix == 0 and self.InfoParametre["code_conclu"]==0):
            self.InfoParametre["code_conclu"] = 0
        if(self.choix==1 and  self.InfoParametre["code_conclu"]==1 ):
            self.InfoParametre["code_conclu"] = 1
        if (self.choix == 0 and self.InfoParametre["code_conclu"]==1):
            self.InfoParametre["code_conclu"] = 2
        if (self.choix == 1 and self.InfoParametre["code_conclu"]==0):
            self.InfoParametre["code_conclu"] = 3
        pdf_feuille_resultat.creation_PDF(os.path.join(path),
                                        self.InfoParametre["nom_projet"],
                                        self.InfoParametre["nom_projet"],
                                        self.InfoParametre["num_foetus"],
                                        self.InfoParametre["num_pere"],
                                        filename,
                                        self.InfoParametre["Sexe"],
                                        self.InfoParametre["df_conclusion"],
                                        self.InfoParametre["df_detail"],
                                        self.InfoParametre["code_conclu"],
                                        self.InfoParametre["nom_utilisateur"],
                                        self.hauteur,
                                        self.nb,
                                        self.conta,
                                        self.InfoParametre["pres_pere"],
                                        self.InfoParametre["Entite_appli"],
                                        self.InfoParametre["Emetteur"],
                                        self.InfoParametre["Version"])
        self.dismiss_popup()
        os.system("xdg-open " + (self.InfoParametre["nom_projet"]+"_"+self.InfoParametre["nom_utilisateur"]+".pdf"))
    def down_button(self,num):
        
        self.choix=num
    
    def ouverture_parametres(self):
        content = ParametreDialog( hauteur=str(self.hauteur),
                                    nb=str(self.nb),
                                    conta=str(self.conta),
                                    save_parametres=self.save_parametres,
                                    emetteur=self.InfoParametre["Emetteur"],
                                    entite=self.InfoParametre["Entite_appli"],
                                    cancel=self.dismiss_popup)
        self._popup = Popup(title="Modifier des parametres", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
    

    def save_parametres(self,p1,p2,p3,p4,p5):
        self.nb= p1
        self.conta = p2
        self.hauteur = p3
        self.InfoParametre["Emetteur"]=p4
        self.InfoParametre["Entite_appli"] = p5
        self.dismiss_popup()
        
    def SaveLog(self):
        with open(os.path.join("log_"+self.titre), 'w') as stream:
            stream.write(self.log)

    def quitter(self):
       
       sys.exit(0)


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
Factory.register('ConcordanceEtSexe', cls=ConcordanceEtSexe)
Factory.register('CloseableHeader', cls=CloseableHeader)
if __name__ == '__main__':

    version=1.0
    app= MyApp()
    app.run()
