#!/bin/bash -l
#SBATCH --job-name=gnomad_v_ukbb_2
#SBATCH --partition=nrnb-compute
#SBATCH --time=2:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --cpus-per-task=1
#SBATCH --output=gnomad_v_ukbb_%A.log
source setup.configure

chromosomes=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 'X' 'Y')

> $OUTDIR/combined_data.txt

for chr in ${chromosomes[@]}
do
        echo "Adding chromsome" $chr" data"
        join -1 2 -2 2 -a1 -e0 -o'1.1,0,1.3,2.3' \
        $OUTDIR/exome_qc_chr${chr}_overlap_counts.txt \
        $OUTDIR/gnomad_chr${chr}_overlap_counts.txt \
        >> $OUTDIR/combined_data.txt
        wc -l $OUTDIR/combined_data.txt
done

echo "Created combined dataset"

python subroutines/plot_gnomad_v_exome.py $OUTDIR
