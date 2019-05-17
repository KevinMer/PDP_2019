# PDP_2019


Pour rendre exécutable:


La version exécutable qui sera obtenue ne sera fonctionnelle que sur le système exploitation où la manipulation aura été effectuée.

Regrouper les scripts (main_gui.py, pdf_feuille_resultat.py, Traitement2) situés dans le dossier V_en_cours dans un dossier.
Puis commande bash dans le path du nouveau dossier:

>python -m PyInstaller --name LACFoM --icon C:\Users\gauvr\Desktop\V_demo_6\logo.ico main_gui.py
(remplacer chemin du logo)
Un fichier spec est créé. 
Modifier le fichier spec comme suit: https://kivy.org/doc/stable/guide/packaging-windows.html
Faire un dossier "data" avec le my.kv dedans et les images: croix.png,logo.png,loco_CHU.png
en plus rajouter dans hiddenimports du fichier spec:  ['win32timezone'] 

enfin commande bash toujours tuojours dans le path du même dossier :
>python -m PyInstaller LACFoM.spec


version exe dans le dossier dist




