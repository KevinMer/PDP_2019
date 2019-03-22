
import pandas as pd
import numpy as np

df = pd.read_table("PP16_DMPK_MARTIN_061118_PP16.txt",sep = '\t',header = 0)
vrai_df = df.replace(np.nan, '', regex=True)
Allele = vrai_df[["Allele 1","Allele 2", "Allele 3"]].values
Hauteur = vrai_df[["Height 1","Height 2", "Height 3"]].values

print(Allele[1])