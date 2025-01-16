#!/bin/bash

#SBATCH --job-name=AGGR_lib_10x_neuro_pilot_all
#SBATCH --partition=512GB
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=30-00:00:00
#SBATCH --output=job_log.%j.out
#SBATCH --error=job_log.%j.err
#SBATCH --mail-user=user@email.com
#SBATCH --mail-type=end

STAR=/project/GCRB/Hon_lab/s166631/00.bin/STAR-2.5.2a/bin/Linux_x86_64/STAR
GENOME_REFERENCE_DIR=/project/GCRB/Hon_lab/s160875/02.annotation/Reference/10X_Genomics/hg38_cellranger-3.0.1/GRCh38/

module load cellranger/7.0.0

### id is what you want final library to be called, csv is the information for mapped transcriptome locations pulled from a csv file in the same directory
cellranger aggr\
    --id=aggr_libraries_10X_exp\
	--csv=aggr_libraries.csv\
	--normalize=none
