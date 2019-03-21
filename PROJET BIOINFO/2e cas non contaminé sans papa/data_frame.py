import pandas as pd

df = pd.read_table("181985_xfra_ja_200618_PP16.txt",sep = '\t',header = 0)
Allele = df[["Allele 1","Allele 2", "Allele 3"]].values
print(Allele[2])
print(Allele[3])
print(Allele[3][0] not in Allele[2])

#for val in range(df.shape[0]-1):
#    if df["Allele 1"][val] == df["Allele 2"][val+1]:
#        print(df["Marker"][val])
#        if Allele[val] in Allele[val + 1]:
