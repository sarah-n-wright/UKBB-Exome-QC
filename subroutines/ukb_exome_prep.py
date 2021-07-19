import sys
sys.path.append("/cellar/users/snwright/.conda/envs/MyPy/lib/python37.zip")
sys.path.append("/cellar/users/snwright/.conda/envs/MyPy/lib/python3.7")
sys.path.append("/cellar/users/snwright/.conda/envs/MyPy/lib/python3.7/lib-dynload")
sys.path.append("/cellar/users/snwright/.conda/envs/MyPy/lib/python3.7/site-packages")

import pandas as pd

input_chr = str(sys.argv[1])
outdir= str(sys.argv[2])

ranges = pd.read_csv("data/glist-hg38", sep="\s+", header=None)
ranges.columns = ["CHR", "start", "end", "Gene"]
ranges["CHR"] = ranges["CHR"].astype(str)

sub_range = ranges.loc[(ranges["CHR"]==input_chr)]

out_ranges = pd.DataFrame({"CHR":input_chr,"POS":0,"Gene":"test"}, index =[0])
first = True
for index, row in sub_range.iterrows():
        print(row['start'], row['end'])
        start = row["start"]
        end = row["end"]
        add = pd.DataFrame({"CHR":input_chr, "POS":range(start, end+1), "Gene":row["Gene"]})
        if first:
                add.to_csv(outdir +"/chr"+input_chr+"_gene_positions.tsv", sep="\t", index=False)
                first = False
        else:
                add.to_csv(outdir + "/chr"+input_chr+"_gene_positions.tsv", sep="\t", index=False, header=None, mode="a")
print("Saved to file.")
