#!/bin/bash -l
#SBATCH --job-name=get_sites
#SBATCH --partition=nrnb-compute
#SBATCH --time=2:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --cpus-per-task=1
#SBATCH --array=0-23
#SBATCH --output=get_sites_%A_%a.log
source setup.configure

chroms=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 'X' 'Y')
chr=${chroms[$SLURM_ARRAY_TASK_ID]}
echo $chr

## Get gene positions ---------------------------------------------------
outfile=$OUTDIR/chr${chr}_sites_gnomad_hg38.tsv
zgrep "^[^#]" $gnomad_path/gnomad.exomes.r2.1.1.sites.${chr}.liftover_grch38.vcf.gz | \
        awk -v out=$outfile '{print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $5 > out}'
echo "CHR "${chr}" gnomad completed."

python subroutines/ukb_exome_prep.py $chr $OUTDIR
# clean up the position file
out=$OUTDIR/temp_${chr}.temp
awk -v out=$out '$3!="test" && $3!="Gene" {print $0 > out}' \
        $OUTDIR/chr${chr}_gene_positions.tsv
sort -k 2n $OUTDIR/temp_${chr}.temp > \
	$OUTDIR/chr${chr}_gene_positions_clean.tsv

echo "CHR "${chr}" ukbb completed."

## Subset and annotate
## UKBB QC
$plink --bed $ukbb_exome_path/ukb23155_c${chr}_b0_v1.bed \
        --bim $ukbb_exome_path/UKBexomeOQFE_chr${chr}.bim \
        --fam $ukbb_exome_path/ukb23155_c22_b0_v1.fam \
        --geno 0.98 \
        --mind 0.98 \
        --make-just-bim \
        --out $OUTDIR/exome_qc_chr$chr.qced

## UKBB susbet & annotate
sort -k 2 $OUTDIR/chr${chr}_gene_positions_clean.tsv > $OUTDIR/temp_chr${chr}.temp

echo "Starting "$chr"------------------------------------"
sort -k 4 $OUTDIR/exome_qc_chr$chr.qced.bim | \
        join -1 2 -2 4 -o'1.1,0,2.2,1.3,2.5,2.6' $OUTDIR/temp_chr${chr}.temp - \
        > $OUTDIR/exome_qc_chr${chr}_gnomad_overlap.txt
echo "Finised overlap------------------------------------"
cat $OUTDIR/exome_qc_chr${chr}_gnomad_overlap.txt | \
        datamash -s -W -g 1,4 count 3 > $OUTDIR/exome_qc_chr${chr}_overlap_counts.txt

echo "Finished "$chr"------------------------------------"
rm $OUTDIR/temp_chr${chr}.temp

## gnomAD subset & annotate
sort -k 2 $OUTDIR/chr${chr}_gene_positions_clean.tsv > $OUTDIR/temp_chr${chr}.temp

echo "Starting "$chr"------------------------------------"
cat $OUTDIR/chr${chr}_sites_gnomad_hg38.tsv | sort -k 2 | \
        join -1 2 -2 2 -o'1.1,0,2.3,1.3,2.4,2.5' \
        $OUTDIR/temp_chr${chr}.temp - > $OUTDIR/chr${chr}_overlap_sites.txt
echo "Finished "$chr"------------------------------------"
cat $OUTDIR/chr${chr}_overlap_sites.txt | \
        datamash -s -W -g 1,4 count 3 > $OUTDIR/gnomad_chr${chr}_overlap_counts.txt
rm $OUTDIR/temp_chr${chr}.temp


