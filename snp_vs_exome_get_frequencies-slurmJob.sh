#!/bin/bash -l
#SBATCH --job-name=snp_v_exm
#SBATCH --output snp_v_exm_%A.out
#SBATCH --partition=nrnb-compute
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --time=3:00:00
#SBATCH --array=0-23

source setup.configure

chromosomes=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 'X' 'Y')
CHR=${chromosomes[$SLURM_ARRAY_TASK_ID]}

# Get frequencies for Exome data and snp chip data
	# Snpchip data
$plink --bfile $ukbb_snp_path/ukb_snp_chr$CHR \
		--keep $ukbb_exome_path/ukb23155_c22_b0_v1.fam \
		--geno 0.98 \
		--mind 0.98 \
		--hwe 0.000001 \
		--maf 0.001 \
		--freq \
		--out $OUTDIR/chr${CHR}_snp_qc_hwe_dropped

$plink --bed $ukbb_exome_path/ukb23155_c${CHR}_b0_v1.bed \
		--bim $ukbb_exome_path/UKBexomeOQFE_chr${CHR}.bim \
		--fam $ukbb_exome_path/ukb23155_c22_b0_v1.fam \
		--geno 0.98 \
		--mind 0.98 \
		--hwe 0.000001 \
		--maf 0.001 \
		--freq \
		--out $OUTDIR/chr${CHR}_exome_hwe_dropped
