import pandas as pd
from Class import*



def nb_pic_patient(patient,no_marker):
    nb_pic = 3
    if patient == "mere":
        ls_allele = M[no_marker].allele
        conclu = "La mere"
    else:
        ls_allele = F[no_marker].allele
        conclu = "Le foetus"
    for i in range(len(ls_allele)):
        if ls_allele[i]==0.0:
            nb_pic = nb_pic-1
    if nb_pic >1:
        print (conclu,"a",nb_pic,"pics.")
    else:
        print (conclu,"a",nb_pic,"pic.")
    return nb_pic


def contamination_marqueur(mere,foetus,no_marker):
    if nb_pic_patient("foetus",no_marker) == 3:
        print ("Le foetus est hétérozygote.")
        print ("Le marqueur",F[no_marker].marqueur,"est contamine.")
        #calcul contamination htz

        
    elif nb_pic_patient("mere",no_marker) == 1:
        print ("La mere est homozygote.")
        print ("Le marqueur",M[no_marker].marqueur,"n'est pas informatif.")


    elif nb_pic_patient("foetus",no_marker) == 2:
        print ("La mere est heterozygote.")
        if (foetus[no_marker].allele_semblable(foetus[no_marker].Semblable,mere[no_marker])):

            if foetus[no_marker].homozygote_contamine(mere,no_marker):

                print ("Le foetus est homozygote.")
                ("Le marqueur",F[no_marker].marqueur,"est contamine.")
                #calcul contamination hmz
            else:
                print ("Le foetus est heterozygote.")
                print ("Le foetus possede probablement les memes alleles que sa mere.")
                print ("Le marqueur",F[no_marker].marqueur,"est non informatif.")
        elif mere[no_marker].echo(foetus[no_marker]):
            print ("Le pic du foetus se trouve dans l'echo")
            print ("Le marqueur",F[no_marker].marqueur,"est non informatif")

        else:
            print("La mere n'a pas le meme profil allelique que le foetus")
            print ("Le pic de la mere ne se situe pas dans l'echo du pic du foetus")
            print ("Le marqueur",F[no_marker].marqueur,"n'est pas contamine")

    elif nb_pic_patient("foetus",no_marker) ==1:
        if mere[no_marker].echo(foetus[no_marker]):
            print ("Le pic de la mere se situe dans l'echo du pic du foetus")
            print ("Le marqueur",F[no_marker].marqueur,"n'est pas informatif")
        else:
            print ("Le pic de la mere ne se situe pas dans l'echo du pic du foetus")
            print ("Le marqueur",F[no_marker].marqueur,"n'est pas contamine")
            
if __name__ == "__main__":
    M,F,P = lecture_donnees("PP16_DMPK_MARTIN_061118_PP16.txt")
    verif_concordance(M,F)
    for i in range(16):
        print(M[i].allele)
        print(M[i].hauteur)
        print(F[i].allele)
        print(F[i].hauteur)
        print(M[i].marqueur)
        contamination_marqueur(M,F,i)
        print("  ")
        print("  ")
