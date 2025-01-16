#!/bin/bash


### If there are different source folders for different batches/lanes, this is the optimum script to use. This will create
### all the folders and subfolders in the range, then copy the template scrips from the demux_scripts folder, into the 
### relevant directories to run


for i in {308..335}; do
    if [ $i -ge 328 ] && [ $i -le 335 ]; then
        echo $i
        mkdir LW${i}
        mkdir LW${i}/_step1_process_transcriptome/
        cp map10x_LWxx2.sh LW${i}/_step1_process_transcriptome/map10x_LW${i}.sh
        cp lib_info_LWxx2.csv LW${i}/_step1_process_transcriptome/lib_info_LW${i}.csv

        mkdir LW${i}/_step2_demux/
        cp demux_scripts/__stable_pipeline_v01.sh LW${i}/_step2_demux/
        cp demux_scripts/__stable_pipeline_v01_demux.sh LW${i}/_step2_demux/
        cp demux_scripts/_processs_hto.sh LW${i}/_step2_demux/
        cp demux_scripts/_processs_sgrna.sh LW${i}/_step2_demux/
        cp demux_scripts/_processs_singlets.sh LW${i}/_step2_demux/
        cp demux_scripts/_util_updated.py LW${i}/_step2_demux/

        continue
    else
        echo $i
        mkdir LW${i}
        mkdir LW${i}/_step1_process_transcriptome/
        cp map10x_LWxx1.sh LW${i}/_step1_process_transcriptome/map10x_LW${i}.sh
        cp lib_info_LWxx1.csv LW${i}/_step1_process_transcriptome/lib_info_LW${i}.csv

        mkdir LW${i}/_step2_demux/
        cp demux_scripts/__stable_pipeline_v01.sh LW${i}/_step2_demux/
        cp demux_scripts/__stable_pipeline_v01_demux.sh LW${i}/_step2_demux/
        cp demux_scripts/_processs_hto.sh LW${i}/_step2_demux/
        cp demux_scripts/_processs_sgrna.sh LW${i}/_step2_demux/
        cp demux_scripts/_processs_singlets.sh LW${i}/_step2_demux/
        cp demux_scripts/_util_updated.py LW${i}/_step2_demux/
    fi
done