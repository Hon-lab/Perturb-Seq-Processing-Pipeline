#!/bin/tcsh

#SBATCH --job-name=S1_Singularity_processing                  # job name
#SBATCH --partition=256GB,512GB,384GB                  # select partion from 128GB, 256GB, 384GB, GPU and super
#SBATCH --nodes=1                                         # number of nodes requested by user
#SBATCH --time=01-00:00:00                                # run time, format: D-H:M:S (max wallclock time)
#SBATCH --output=serialJob.%j.out_LWxxx_full                         # standard output file name
#SBATCH --error=serialJob.%j.time_LWxxx_full                         # standard error output file name
#SBATCH --mail-user=mpathi.nzima@utsouthwestern.edu           # specify an email address
#SBATCH --mail-type=end                                   # send email when job status change (start, end, abortion and etc.)



### Each data dir points to the location of a seperate sequencing run. will combine both to map. The sgRNA reference is the annotation file with sgRNA sequences

set sgRNA_ref=/project/GCRB/Hon_lab/s426305/Sequencing_data_analysis/10X/LW318/sgRNA/make_sgRNA_ref/sgRNA_ref_list_uniq_reverse.txt

set hto_ref=/project/GCRB/Hon_lab/s215194/Single_Cell/Process_scRNA_CMPILOT2/HTO/hto_ref.tsv

### the directories for each sequencing run
set DATA_DIR_sgrna=/project/GCRB/Hon_lab/shared/data/sequencing_data/2023/2023-12-24-Novogene-NovaSeq.Hon4-6/sgRNA/
set DATA_DIR_hto=/project/GCRB/Hon_lab/shared/data/sequencing_data/2023/2023-12-24-Novogene-NovaSeq.Hon4-6/HTO/


module load singularity/3.9.9

set library_name=`pwd | perl -ne '@a = split(/\//, $_); pop(@a); print(pop(@a));'`
echo $library_name

set container_image=/project/GCRB/Hon_lab/shared/container_images/fba/fba_v0.sif
echo $container_image

### combine the libraries for the different features (i.e sgRNA libraries and HTO Libraries)


## Get the fastq files

# echo "catting sgRNA QC fastqs"
# zcat $DATA_DIR_sgrna/$library_name\B_S*_L00*_R1_001.fastq.gz | head -1000000 | gzip > $library_name\_sgrna_R1.fastq.gz
# zcat $DATA_DIR_sgrna/$library_name\B_S*_L00*_R2_001.fastq.gz | head -1000000 | gzip > $library_name\_sgrna_R2.fastq.gz
#
# echo "catting HTO QC fastqs"
# zcat $DATA_DIR_hto/$library_name\C_S*_L00*_R1_001.fastq.gz | head -1000000 | gzip > $library_name\_hto_R1.fastq.gz
# zcat $DATA_DIR_hto/$library_name\C_S*_L00*_R2_001.fastq.gz | head -1000000 | gzip > $library_name\_hto_R2.fastq.gz

echo "catting sgRNA fastqs"
cat $DATA_DIR_sgrna/$library_name\B_S*_L00*_R1_001.fastq.gz > $library_name\_sgrna_R1.fastq.gz
cat $DATA_DIR_sgrna/$library_name\B_S*_L00*_R2_001.fastq.gz > $library_name\_sgrna_R2.fastq.gz

echo "catting HTO fastqs"
cat $DATA_DIR_hto/$library_name\C_S*_L00*_R1_001.fastq.gz > $library_name\_hto_R1.fastq.gz
cat $DATA_DIR_hto/$library_name\C_S*_L00*_R2_001.fastq.gz > $library_name\_hto_R2.fastq.gz


## Get the cell barcode ID's

zcat /project/GCRB/Hon_lab/s215194/Single_Cell/TF_perturbseq_full_remapped/$library_name\/_step1_process_transcriptome/$library_name\_10x/outs/filtered_feature_bc_matrix/barcodes.tsv.gz > $library_name\.barcodes.tsv \


## Feature extraction

echo "beginning sgRNA extract"
singularity exec $container_image \
fba extract \
	-1 $library_name\_sgrna_R1.fastq.gz \
	-2 $library_name\_sgrna_R2.fastq.gz \
	-w $library_name\.barcodes.tsv \
	-f $sgRNA_ref \
	-o $library_name\_sgrna_feature_barcoding_output.tsv.gz \
	-r1_c 0,16 \
	-r2_c 63,82

echo "beginning HTO extract"
singularity exec $container_image \
fba extract \
	-1 $library_name\_hto_R1.fastq.gz \
	-2 $library_name\_hto_R2.fastq.gz \
	-w $library_name\.barcodes.tsv \
	-f $hto_ref \
	-o $library_name\_hto_feature_barcoding_output.tsv.gz \
	-r1_c 0,16 \
	-r2_c 10,25

echo "beginning sgRNA count"
singularity exec $container_image \
fba count \
	-i $library_name\_sgrna_feature_barcoding_output.tsv.gz \
	-o $library_name\_sgrna_matrix_featurecount.csv.gz \
	-us 16 \
	-ul 12 \
	-um 2 \
	-ud percentile

echo "beginning HTO count"
singularity exec $container_image \
fba count \
	-i $library_name\_hto_feature_barcoding_output.tsv.gz \
	-o $library_name\_hto_matrix_featurecount.csv.gz \
	-us 16 \
	-ul 12 \
	-um 1 \
	-ud percentile

echo "beginning HTO demux"
singularity exec $container_image \
fba demultiplex \
	-dm 5-2019\
	-i $library_name\_hto_matrix_featurecount.csv.gz\
	--output_directory hto_demultiplexed_$library_name\
	-nc 20\

echo "removing fastqs"
rm *fastq.gz

echo "\n this is the end for now"

