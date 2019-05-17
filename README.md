# PDP_2019


Pour rendre exécutable:


La version exécutable qui sera obtenue ne sera fonctionnelle que sur le système exploitation où la manipulation aura été effectuée.

Regrouper les scripts (main_gui.py, pdf_feuille_resultat.py, Traitement2,logo.ico) situés dans le dossier V_en_cours dans un dossier. (Exemple ici V_demo_6)
Puis commande bash dans le path du nouveau dossier:

>python -m PyInstaller --name LACFoM --icon C:\Users\gauvr\Desktop\V_demo_6\logo.ico main_gui.py
(remplacer chemin du logo)


Un fichier spec est créé dans le dossier. 
Faire un dossier "data" dans le dossier contenant le fichier spec qui contiendra le script my.kv et les images : croix.png, logo.png, loco_CHU.png

Les modifications du fichier spec se basent sur la partie "Packaging a simple app" point 3 de la  page suivante: https://kivy.org/doc/stable/guide/packaging-windows.html

Spécifier dans le fichier spec le chemin du "data" à la ligne "coll = COLLECT(exe, Tree('examples-path\\demo\\touchtracer\\'),"

Toujours dans le fichier spec, rajouter en plus dans hiddenimports:  ['win32timezone'] 
Modifier le nom à la ligne name='touchtracer' par name='LACFoM'

enfin commande bash toujours dans le path du même dossier :
>python -m PyInstaller LACFoM.spec


La version exe se trouvera dans le dossier "dist" qui sera créé à la suite de la commande.



