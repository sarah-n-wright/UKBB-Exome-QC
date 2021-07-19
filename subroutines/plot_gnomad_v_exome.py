import sys
sys.path.append("/cellar/users/snwright/.conda/envs/MyPy/lib/python37.zip")
sys.path.append("/cellar/users/snwright/.conda/envs/MyPy/lib/python3.7")
sys.path.append("/cellar/users/snwright/.conda/envs/MyPy/lib/python3.7/lib-dynload")
sys.path.append("/cellar/users/snwright/.conda/envs/MyPy/lib/python3.7/site-packages")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

outdir=str(sys.argv[1])

df = pd.read_csv(outdir+"/combined_data.txt", sep="\s+", header=None)
df.columns = ["CHR", "Gene", "UKBB", "gnomAD"]

plt.figure()
fig=sns.jointplot(y="gnomAD", x="UKBB", data=df, s=1, xlim=(-40, 3000), ylim=(-40, 3000), marginal_kws=dict(bins=list(range(0,31000,100))))
#plt.savefig("~/Data/Transfer/combo_NOQC.png")
plt.savefig(outdir+"/gnomad_v_ukbb.png")
print("Done.")

