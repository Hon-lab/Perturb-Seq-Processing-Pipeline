#!/bin/tcsh

#SBATCH --job-name=process_transcriptome.py                # job name
#SBATCH --partition=256GB                  # select partion from 128GB, 256GB, 384GB, GPU and super
#SBATCH --nodes=1                                         # number of nodes requested by user
#SBATCH --time=60-00:00:00                                # run time, format: D-H:M:S (max wallclock time)
#SBATCH --output=serialJob.%j.out                         # standard output file name
#SBATCH --error=serialJob.%j.time                         # standard error output file name
#SBATCH --mail-user=mpathi.nzima@utsouthwestern.edu        # specify an email address
#SBATCH --mail-type=end                                   # send email when job status change (start, end, abortion and etc.)

setenv PATH ~/.conda/envs/Single-Cell/bin:$PATH

./_ProcessTranscriptome_no_rp_filtering.py