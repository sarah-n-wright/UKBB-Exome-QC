import sys
import pandas as pd
import numpy as np

OUTDIR=str(sys.argv[1])

## Restrict to the overlapping positions
snpchip = pd.read_csv("data/ukb_snpchip_chrall_exomeseq_hg38.intersect.vcf", sep="\t", skiprows=2)
snpchip['#CHROM'] = snpchip['#CHROM'].replace(to_replace='X', value=23) 
snpchip['#CHROM'] = snpchip['#CHROM'].replace(to_replace='Y', value=24)
snpchip["SNP"] = snpchip["#CHROM"].astype('str')+':'+ snpchip["POS"].astype('str')+':'+snpchip["REF"]+':'+snpchip["ALT"]

#Subset the two datasets
chrs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 19, 20, 21, 22, 'X', 'Y']

for c in chrs:
    # First version:
    # snp_file = "exome_debug/snp_chip_compare/chr"+str(c)+"_snp_chip.frq"
    # exome_file = "exome_debug/chr"+str(c)+"_all_maf.frq"
    # Second version:
    snp_file = OUTDIR + "/chr"+str(c)+"_snp_qc_hwe_dropped.frq"
    exome_file = OUTDIR + "/chr"+str(c)+ "_exome_hwe_dropped.frq"
    snp = pd.read_csv(snp_file, sep = "\s+")
    exm = pd.read_csv(exome_file, sep = "\s+")
    include_snps = snpchip.loc[(snpchip["ID"].isin(snp["SNP"])), ("ID", "SNP")]
    snp = snp.merge(include_snps, left_on="SNP", right_on="ID")
    snp_set = set(snp["SNP_y"])
    exm_set = exm["SNP"]
    shared = snp_set.intersection(exm_set)
    print(c, ":", len(shared))
    snp = snp.loc[(snp["SNP_y"].isin(shared))]
    exm = exm.loc[(exm["SNP"].isin(shared))]
    snp.to_csv(OUTDIR + "/chr"+str(c)+"_snp_exm_overlap_hwe_dropped.frq", sep = "\t", index=False)
    exm.to_csv(OUTDIR + "/chr"+str(c)+"_exm_maf_snp_overlap_hwe_dropped.frq", sep = "\t", index=False)

# compile exome all together
exome_maf =pd.read_csv(OUTDIR + "/chr"+str(1)+"_exm_maf_snp_overlap_hwe_dropped.frq", sep = "\t", index_col=0)
chrs = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,17,19,20,21,22,'X','Y']
for c in chrs:
    add = pd.read_csv(OUTDIR + "/chr"+str(c)+ "_exm_maf_snp_overlap_hwe_dropped.frq", sep = "\t", index_col=0)
    exome_maf = exome_maf.append(add)

# compile all snp
snp_maf =pd.read_csv(OUTDIR + "/chr"+str(1)+"_snp_exm_overlap_hwe_dropped.frq", sep = "\t", index_col=0)
print(snp_maf.shape)
chrs = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,17,19,20,21,22,'X','Y']
for c in chrs:
    add = pd.read_csv(OUTDIR + "/chr"+str(c)+ "_snp_exm_overlap_hwe_dropped.frq", sep = "\t", index_col=0)
    snp_maf = snp_maf.append(add)
snp_maf.head()
snp_maf.shape

# Write outputs to output directory
exome_maf.to_csv(OUTDIR + "/exome_maf_final.tsv", sep="\t", index = False)
snp_maf.columns = ["ID", "A1", "A2", "MAF", "NCHROBS", "ID2", "SNP"]
snp_maf.to_csv(OUTDIR + "/snp_maf_final.tsv", sep="\t", index=False)