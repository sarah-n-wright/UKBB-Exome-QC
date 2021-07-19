# UKBB-Exome-QC

The included scripts are made available to repeat previous analysis (Jia et al **Thousands of missing variants in the UK Biobank are recoverable by genome realignment** *Annals of Human Genetics* 2020. DOI: 10.1111/ahg.12383) for the latest release of 200,000 exomes from the UK Biobank. The results demonstrate the update OQFE pipeline successfully handles alternative contigs in the GRCh38 reference genome. 

## Dependencies

Tools:  
* plink version 1.9 (https://www.cog-genomics.org/plink/1.9/)
* python 2.7; (with: pandas, seaborn, matplotlib.pyplot, numpy, sys)
* datamash (https://www.gnu.org/software/datamash/)
* (Optional) slurm (https://slurm.schedmd.com/archive/slurm-18.08.7/quickstart.html) to enable distributed computation. Scripts with and without this capability are provided. 
  
Data:  
* UKBB 200k whole-exome data in plink .bed/.bim/.fam format, separate file sets for each chromosome
* UKBB snp-chip genotyping data in plink .bed/.bim/.fam format. separate files sets for each chromosome
* Ranges of UKBB whole exome targeted regions with associated genes. Included as 'data/glist-hg38' ()
* SNP-Chip variants lifted over into GRCh38 coordinates and subset to variants contained by exome-sequencing regions. Included as `data/ukb_snpchip_chrall_exomeseq_hg38.intersect.vcf'
* gnomAD V2 liftover GRCh38 sites only Exome VCF files (https://gnomad.broadinstitute.org/downloads)
 
## Setup

Modify setup.configure to point to local file locations. *Distributed computation Note:* you will need to modify the #SBATCH headers to match your setup.  

## SNP vs Exome
**Option 1:** Run `bash snp_vs_exome.sh` to perform analysis and produce the summary plot.  
**Option 2:** First run `sbatch snp_vs_exome-slurmJob1.sh` until completion, followed by `sbatch snp_vs_exome-slurmJob2.sh` to perform the same analysis using distributed computation. *Note:* you will need to modify the #SBATCH headers to match your setup.  

All intermediate files and final outputs will be saved in the directory specified in `setup.configure`  

## gnomAD vs Exome
**Option 1:** Run bash `gnomad_v_exome.sh` to perform analysis and produce the smummary plot. *Note:* this script may take significant time to execute due to the size of the gnomAD files.
**Option 2:** Run `gnomad_v_exome-slurmJob1.sh` until completion followed by `gnomad_v_exome-slurmJob2.sh` to perform the same analysis using distributed computation.

All intermediate files and final outputs will be saved in the directory specified in `setup.configure`  

## Optional Jupyter Notebook

As well as the .png plots produced by the included scripts, the results can also be viewed in the provided `Plot Final Comparisons.ipynb` notebook.

## TODOs
ToDo: Need to tune the SNP plot.

Done: Consolidated and tested the SNP pipeline
