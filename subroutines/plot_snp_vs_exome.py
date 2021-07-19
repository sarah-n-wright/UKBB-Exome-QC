import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns; sns set

OUTDIR=str(sys.argv[1])

exome_maf = pd.read_csv(OUTDIR + "/exome_maf_final.tsv", sep="\t", index_col=0)
snp_maf = pd.read_csv(OUTDIR + "/snp_maf_final.tsv", sep="\t", index_col=6)

mpl.rcParams['figure.dpi']= 200
df_maf = snp_maf.join(exome_maf, how="left", lsuffix=' snpchip', rsuffix=' exome')

df_maf["MAF exome"] = df_maf["MAF exome"].replace(to_replace=float('nan'), value=0.0) 

plt.figure()
sns.jointplot(x='MAF exome', y='MAF snpchip',data=df_maf, s=3, marginal_kws=dict(bins=np.linspace(0, 0.5,40)))
plt.savefig(OUTDIR + "/snp_v_exm_compare.png")