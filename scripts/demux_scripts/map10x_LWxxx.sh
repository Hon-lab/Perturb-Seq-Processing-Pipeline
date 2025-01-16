#!/bin/bash

#SBATCH --job-name=map_10x_LWxxx
#SBATCH --partition=256GB,384GB,512GB
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00-20:00:00
#SBATCH --output=job_log.%j.out_LWxxx
#SBATCH --error=job_log.%j.err_LWxxx
#SBATCH --mail-user=mpathi.nzima@utSouthwestern.edu
#SBATCH --mail-type=ALL

STAR=/project/GCRB/Hon_lab/s166631/00.bin/STAR-2.5.2a/bin/Linux_x86_64/STAR
GENOME_REFERENCE_DIR=/project/GCRB/Hon_lab/s425140/00.Annotations/CELLRANGER_hg38/refdata-gex-GRCh38-2020-A
module load cellranger/7.0.0

echo $SLURM_CPUS_ON_NODE
export PATH=$PATH:$CELLRANGER

RESULTS_DIR=$PWD


### id is the name of the 10x library (much match name in csv file)
### libraries is the location of the csv file with information on library
### expect cells is not necessary but can help 10x call cells

cellranger count \
    --id='LWxxx_10x' \
    --libraries=lib_info_LWxxx.csv\
    --expect-cells=90000\
    --transcriptome=$GENOME_REFERENCE_DIR

