#!/bin/bash -l
#SBATCH --job-name=snp_v_exm
#SBATCH --output snp_v_exm_%A.out
#SBATCH --partition=nrnb-compute
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --time=3:00:00

source setup.configure

python subroutines/snp_vs_exome_combine.py $OUTDIR

python subroutines/plot_snp_vs_exome.py $OUTDIR
