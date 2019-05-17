# PDP_2019


Pour rendre exécutable:


La version exécutable qui sera obtenue ne sera fonctionnelle que sur le système exploitation où la manipulation aura été effectuée.

Regrouper les scripts (main_gui.py, pdf_feuille_resultat.py, Traitement2) situés dans le dossier V_en_cours dans un dossier.
Puis commande bash:

>python -m PyInstaller --name LACFoM --icon C:\Users\gauvr\Desktop\V_demo_6\logo.ico main_gui.py

Un fichier spec est créé. 
Modifier le fichier spec comme suit: https://kivy.org/doc/stable/guide/packaging-windows.html
Faire un dossier "data" avec le my.kv dedans et les images: croix.png,logo.png,loco_CHU.png
en plus rajouter dans hiddenimports:  ['win32timezone'] 

enfin commande bash:
>python -m PyInstaller LACFoM.spec


version exe dans dist




