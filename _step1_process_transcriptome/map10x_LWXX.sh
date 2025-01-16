#!/bin/bash

#SBATCH --job-name=map_10x_LW371
#SBATCH --partition=256GB
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=30-00:00:00
#SBATCH --output=job_log.%j.out
#SBATCH --error=job_log.%j.err
#SBATCH --mail-user=user@website.com
#SBATCH --mail-type=ALL

#
STAR=/project/GCRB/Hon_lab/s166631/00.bin/STAR-2.5.2a/bin/Linux_x86_64/STAR

# The genome reference build to be mapped on
GENOME_REFERENCE_DIR=/project/GCRB/Hon_lab/s425140/00.Annotations/CELLRANGER_hg38/refdata-gex-GRCh38-2020-A

# The 10X cell ranger version to load on the cluster, for running the mapping
module load cellranger/7.0.0

echo $SLURM_CPUS_ON_NODE
export PATH=$PATH:$CELLRANGER

RESULTS_DIR=$PWD


### id is the name of the 10x library (much match name in csv file to keep track of data)
### libraries is the location of the csv file with information on library, modifify if not stored in the directory the file is run in
### expect cells is not necessary but can help 10x call cells since Cell Ranger tends to overcall cells naturally

cellranger count \
    --id='LWXX_10x' \
    --libraries=lib_info_LWXX.csv\
    --expect-cells=90000\
    --transcriptome=$GENOME_REFERENCE_DIR

