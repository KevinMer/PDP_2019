#coding: utf-8
import kivy

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

import pandas as pd
import os
import sys

kivy.require('1.10.1')
Window.clearcolor = (1, 1, 1, 1)
Window.size = (1000,800)
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)



class Root(GridLayout):
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
        print(donnees)
        self.dismiss_popup()
        self.corps=""
        for i in range(16):
            self.corps=self.corps + "Marqueur "+str(i)+": Contaminé \n \n"

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write("Ce truc fonctionne ayait confiance \n")

        self.dismiss_popup()


    def quitter(self):
       sys.exit(0)

class new_MyApp(App):
    title='DPN 3000'
    pass
    
Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)

if __name__ == '__main__':



    app= new_MyApp()
    app.run()

