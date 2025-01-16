# Perturb-Seq-Processing-Pipeline

## Pipeline and Experimental Overview
![TF_PerturbSeq_worflow_white_background](https://github.com/user-attachments/assets/d3fea3c2-b94d-431d-8e6e-71d862a72a79)




This version of the stable pipeline is to perform all the pre-processing and processing steps required, from **FASTQ** to **h5ad**, for a standard Perturb Seq experiment prepared using 10X (or equivalent). 
This pipeline contains both the scripts, and container images needed to successfully process a Perturb Seq, as well as generate the files needed to perform any downstream analysis.
 
## Required input files:
- sgRNA reference tsv/csv file:
	- **Note**. It will also be important to know length of sgRNAs the length of reads and position of sgRNAs on the reads
- Minimal requirements:
	- Column 1: Unique ID of sgRNA  saved as ***sgRNA_ref.tsv***
	- Column 2: Reverse compliment sequence of sgRNA (for 5 Prime sequencing)
- HTO reference tsv/csv file:
	- Note. It will also be important to know length of HTOs
- Minimal requirements:
	- Column 1: ID of HTO (e.g. HTO1, HTO2 etc.)
	- Column 2: Reverse compliment sequence of HTO
- FASTQs for Transcriptome, sgRNA and HTO (R1, R2, I1 and I2, for however many sequencing events and lanes)

## Container Images Provided (Found on Docker.io at https://hub.docker.com/repository/docker/mnzima/hon_lab_container_images/general):
 - FBA
 	- A container environment with all the packages required to run the FBA fucntions (see https://fba.readthedocs.io/en/latest/index.html)
 - PySpade 0.1.5
	- A container environment with all the packages required to run PySpade for Differential Expression Analysis (see https://github.com/Hon-lab/pySpade/tree/main?tab=readme-ov-file) 
 - Python Image 
	- A container environment with all the packages required to run the python packages and fucntions (see the **reference .yml** files for details)     



<br><em> **Note**:
The relevant folders and scripts can be be copied over manually, or the _make_folders_and_files.sh shell script can be used to automatically generate the the 
files and directories needed for all the subsequent steps. Further instrucrtions can be found in the script.</br></em>

## Processing Steps

> ### The folders for the subsequent steps can be automatically generated using ___make_files_and_folders.sh___ in the **reference scripts** folder


### Step 1 - Process Transcriptome (10X Cell Ranger) 
- Modify the lib_info_XXXX.csv to include sequencing lane info for current lane
	- Run map10x_XXXX.sh
		- **Note.** The number of expected cells will need to be known for this script to help 10X better estimate the number of cells to call
	- Output Files/Folder:
		- This will create the directory and the series of 10X outputs (.h5 files outputs) required for **Step 2**


### Step 2 - Count, Extract and Demultiplexing of sgRNA and HTO
- Required Files:
	- 10X output filtered_feature_bc_matrix/barcodes.tsv.gz
- Required Scripts:
	- process_sgrna.sh
	- call_sgrna.py
	- process_hto.sh
	- call_hto.py
	- process_singlets.sh
	- call_singlets.py
	- __stable_pipeline_V0.sh
	- __stable_pipeline_v01_demux.sh
- Make the following modifications to ***stable_pipeline_V0.sh***:
	- Set the data directory for the FASTQs
	- Read length and position of the sgRNAs on the FASTQ reads (sgRNA length is typically 19 or 20bp)
	- Read length and position of the HTOs on the FASTQ reads
	- Note. This file can be modified to run a quick QC on the first 1M reads if desired.
- Output Files:
	- sgRNA_DF.pkl
	- sgna_distribution.png
	- HTO_Singlets_DF.pkl
	- HTO_distribution.png
	- singlet_sgrna_distrib_updated.png
	- final_combined_sgRNA_multiplets_HTO_singlets.pkl


### Step 3 - Aggregation 
- Required Files:
	- final_combined_sgRNA_multiplets_HTO_singlets.pkl
- Required Scripts (can be run in parallel):
	- Aggregate Transcriptome:
 		- aggr_libraries.csv (for all the libraries you wish to aggregate, in order)
		- aggr10x.sh
	- Make the following modifications to ***aggr_libraries.csv***:
		- Add the library name and directory for the h5 output file (from **Step 2**) 
	- Output Files:
		- This will create the directory and the aggregated 10X output (.h5 files output) needed for **Step 4**      
	- Aggregate Dataframe:
		- combine_dfs.py (for all the libraries you wish to aggregate, in order. This must correspond to the order and number of libraries for the aggregated Transcriptome)
		- combine_df.sh
	- Make the following modifications to combine_dfs.py:
		- Add the list of libraries and head directory for the ***final_combined_sgRNA_multiplets_HTO_singlets.pkl*** output files (from **Step 2**) 
	- Output Files:
		- This will create the aggregated aggr_combined_df_full.pkl needed for **Step 4**  



### Step 4 - Process Transcriptome 
- Required Files:
  	- filtered_feature_bc_matrix.h5 (aggregate file created in **Step 3**, found in the Cell Ranger output folder)
	- aggr_combined_df_full.pkl
- Required Scripts:
	- ProcessTranscriptome.py
	- ProcessTranscriptome.sh
- Make the following modifications to ProcessTranscriptome.py:
	- Add the directories for the two required input files for the script  
	- Add the directories for the desired output files to be saved (you can generate intermediate output files at different stages of processing depending on your needs)
- Output files:
	- VX_XXXX_sample_unfiltered_HTOsinglets_sgRNA_multiplets_experiment_title_date.h5ad
	- Feature Plots for defined genes (e.g. umap_cardiac_markers.png)

