# PDP_2019


Pour rendre excutable:
la version exéctutable qui sera obtenue ne sera focntionnelle uniquement sur le système exploitation où la manipulation à était faite.

regrouper les scripts dans un dossier
Puis commande bash:

>python -m PyInstaller --name LACFoM --icon C:\Users\gauvr\Desktop\V_demo_6\logo.ico main_gui.py

un fichier spec est créé 
modif le fichier scpec comme suit:https://kivy.org/doc/stable/guide/packaging-windows.html
faire un dossier data avec le my.kv dedans et les images: croix.png,logo.png,loco_CHU.png
en plus rajouter dans hiddenimports:  ['win32timezone'] 

enfin commande bash:
>python -m PyInstaller LACFoM.spec


version exe dans dist




