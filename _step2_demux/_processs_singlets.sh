#!/bin/tcsh

#SBATCH --job-name=process_singlets              # job name
#SBATCH --partition=256GB                  # select partion from 128GB, 256GB, 384GB, GPU and super
#SBATCH --nodes=1                                         # number of nodes requested by user
#SBATCH --time=60-00:00:00                                # run time, format: D-H:M:S (max wallclock time)
#SBATCH --output=serialJob.%j.out                         # standard output file name
#SBATCH --error=serialJob.%j.time                         # standard error output file name
#SBATCH --mail-user=mpathi.nzima@utsouthwestern.edu        # specify an email address
#SBATCH --mail-type=end                                   # send email when job status change (start, end, abortion and etc.)

setenv PATH ~/.conda/envs/Single-Cell/bin:$PATH

### set the directory for the singlet processing python file
set SGRNA_DEMUX = /project/GCRB/Hon_lab/s215194/Single_Cell/Neuro_production_01/demux_scripts/_Singlet_sgRNA.py

### Definte the directories for any relevant sgRNA Marix Feature Count file
set hto_singlets = `ls HTO_Singlets_DF.pkl`
set sgrna_singlets =  `ls sgRNA_DF.pkl`


echo $hto_singlets
echo $sgrna_singlets

### call the sgrna demultiplexing file and define the input file
$SGRNA_DEMUX $hto_singlets $sgrna_singlets