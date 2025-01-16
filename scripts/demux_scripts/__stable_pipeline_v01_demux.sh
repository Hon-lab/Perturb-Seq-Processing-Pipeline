#!/bin/tcsh

#SBATCH --job-name=LWxxx_Lib_demux_v2                   # job name
#SBATCH --partition=256GB,384GB,512GB                  # select partion from 128GB, 256GB, 384GB, GPU and super
#SBATCH --nodes=1                                         # number of nodes requested by user
#SBATCH --time=00-06:00:00                                # run time, format: D-H:M:S (max wallclock time)
#SBATCH --output=serialJob.%j.out_demux_LWxxx                         # standard output file name
#SBATCH --error=serialJob.%j.time_demux_LWxxx                         # standard error output file name
#SBATCH --mail-user=mpathi.nzima@utsouthwestern.edu           # specify an email address
#SBATCH --mail-type=end                                   # send email when job status change (start, end, abortion and etc.)

# setenv PATH /home2/s215194/.conda/envs/fba/bin:$PATH


### Each data dir points to the location of a seperate sequencing run. will combine both to map. The sgRNA reference is the annotation file with sgRNA sequences
set sgRNA_ref=/project/GCRB/Hon_lab/s215194/Single_Cell/Neuro_production_01/sgrna_mapping_ref.csv

set hto_ref=/project/GCRB/Hon_lab/s215194/Single_Cell/Process_scRNA_CMPILOT2/HTO/hto_ref.tsv

### the directory for the sgRNA processing python file
set SGRNA_DEMUX=./_processs_sgrna.sh

### the directory for the HTO processing python file
set HTO_DEMUX=./_processs_hto.sh

### the directory for the singlet processing python file
set PROC_SINGLETS=./_processs_singlets.sh

echo "beginning sgRNA processing and demux for singlets"
$SGRNA_DEMUX

echo "beginning HTO processing for singlets"
$HTO_DEMUX

echo 'processing singlets'
$PROC_SINGLETS

echo "\n this is the end for now"