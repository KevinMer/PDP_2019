import pandas as pd

df = pd.read_table("181985_xfra_ja_200618_PP16.txt",sep = '\t',header = 0)

if df.shape[0] > 32:
    print("Pere présent")
else:
    print("Pere absent")

#for val in range(df.shape[0]-1):
#    if df["Allele 1"][val] == df["Allele 2"][val+1]:
#        print(df["Marker"][val])

def concordance(data_frame):
    Allele = data_frame[["Allele 1","Allele 2", "Allele 3"]].values
    print(Allele)
    for val in range(data_frame.shape[0] - 1):
        if Allele[val] in Allele[val + 1]:
            print("Ok")
