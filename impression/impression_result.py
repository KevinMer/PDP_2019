#-*- coding: utf-8 -*-
import sys

def impression(path,pdf):
    '''path (string) : path to the directory in which the pdf file is stored
       pdf (string) : name of the file
    '''
    
    if sys.platform == "win32":
        import win32api
        import win32print
        
        win32api.ShellExecute (0,"print",path+pdf,'/d:"%s"' % win32print.GetDefaultPrinter (),".",0)

    
    else:
        import subprocess
        
        subprocess.Popen(['lpr','-o','landscape','-o','fit-to-page',path+pdf])


if __name__ == "__main__":
    if sys.platform == "win32":
        path= "D:\\Nouveau dossier\\"
        pdf= "Résultat.pdf"
    if sys.platform == "linux":
        path= "/home/mirna/Documents/projet/aicfm/PDP_2019/export_pdf_2/"
        pdf= "Résultat.pdf"
    impression(path,pdf)
