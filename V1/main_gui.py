#coding: utf-8

#version application 0.2
import kivy

import Traitement_1

from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.lang  import Builder

from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.factory import Factory
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanel




import pandas as pd
import os

import sys


kivy.require('1.10.1')
Window.clearcolor = (20, 20, 20, 1)
Window.size = (1000,800)


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class ParametreDialog(FloatLayout):
    fermeture_parametres=ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class TableOnglets(TabbedPanel):
    pass

class EcranPremier(Screen):
    pass


class EcranFct(Screen):
    pass


class EcranFctMethod(GridLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    
    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        contenu=LoadDialog(load=self.load,cancel=self.dismiss_popup)
        self._popup = Popup(title='Ouvrir un fichier', content=contenu,  size_hint=(0.9, 0.9))
        self._popup.open()
        
    def load(self, path, filename):
        donnees = pd.read_table(os.path.join(path, filename[0]),sep = '\t',header = 0)
        self.titre = "Echantillon: " + donnees["Sample Name"][1]
        #print(donnees)

        M, F, P, Echantillon_F = Traitement_1.lecture_fichier(os.path.join(path, filename[0]))
        print(os.path.join(path, filename[0]))

        self.dismiss_popup()
        self.corps = Traitement_1.traitement_donnees(M, F, Echantillon_F)

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Sauvegarder un  fichier", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(" \n")

        self.dismiss_popup()

    def ouverture_parametres(self):
        content = ParametreDialog(fermeture_parametres=self.fermeture_parametres,cancel=self.dismiss_popup)
        self._popup = Popup(title="Modifier des parametres", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def fermeture_parametres(self):


        self.dismiss_popup()



    def quitter(self):
       sys.exit(0)



class ScreenManagement(ScreenManager):
    pass       

    


class MyApp(App):
    
    title='DPN 3000'
    def build(self):
        self.icon ='logo.png'
    

Factory.register('EcranPremier', cls=EcranPremier)    
Factory.register('EcranFct', cls=EcranFct)
Factory.register('EcranFctMethod', cls=EcranFctMethod)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)
Factory.register('ParametreDialog', cls=ParametreDialog)
if __name__ == '__main__':


    app= MyApp()
    app.run()

    

    