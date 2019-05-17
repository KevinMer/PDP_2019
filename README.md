# PDP_2019


Pour rendre exécutable:


La version exécutable qui sera obtenue ne sera fonctionnelle que sur le système exploitation où la manipulation aura été effectuée.

Regrouper les scripts (main_gui.py, pdf_feuille_resultat.py, Traitement2,logo.ico) situés dans le dossier V_en_cours dans un dossier.
Puis commande bash dans le path du nouveau dossier:

>python -m PyInstaller --name LACFoM --icon C:\Users\gauvr\Desktop\V_demo_6\logo.ico main_gui.py
(remplacer chemin du logo)
Un fichier spec est créé dans le dossier. 

Faire un dossier "data" dans le dossier où il y à le fichier spec, le main_gui,pdf_feuille...qui cotiendra le my.kv dedans et les images: croix.png,logo.png,loco_CHU.png

Les modifications du fichier spec se base sur la parti "packaging a simple app" 3. de la  page suivante: https://kivy.org/doc/stable/guide/packaging-windows.html

spécifié dans le fichier spec le chemin du data à la ligne "coll = COLLECT(exe, Tree('examples-path\\demo\\touchtracer\\'),"

en plus rajouter dans hiddenimports du fichier spec:  ['win32timezone'] 

modifié le nom à la ligne name='touchtracer' par LACFoM

enfin commande bash toujours toujours dans le path du même dossier :
>python -m PyInstaller LACFoM.spec


la version exe sera dans le dossier dist qui sera créé à la suite de la commande




/
