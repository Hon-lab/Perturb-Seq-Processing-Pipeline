#!/bin/tcsh

#SBATCH --job-name=aggr_DFs_All                      # job name
#SBATCH --partition=512GB                 # select partion from 128GB, 256GB, 384GB, GPU and super
#SBATCH --nodes=1                                         # number of nodes requested by user
#SBATCH --time=30-00:00:00                                # run time, format: D-H:M:S (max wallclock time)
#SBATCH --output=serialJob.%j.out                         # standard output file name
#SBATCH --error=serialJob.%j.time                         # standard error output file name
#SBATCH --mail-user=user@email.com           # specify an email address
#SBATCH --mail-type=ALL                                   # send email when job status change (start, end, abortion and etc.)

echo 'Hello World'

setenv PATH ~/.conda/envs/Single-Cell/bin:$PATH

echo 'Program is running with the current python version:'

which python
python --version

./_combine_dfs.py

