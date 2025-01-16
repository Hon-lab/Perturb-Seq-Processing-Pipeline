#!/usr/bin/env python3
# coding: utf-8

import scipy
import statistics
import scanpy as sc
import numpy as np
import pandas as pd
import matplotlib as mpl
import collections
import sys
from collections import defaultdict
import matplotlib
from matplotlib import pyplot as plt
import scipy.io as io
#get_ipython().run_line_magic('matplotlib', 'inline')

matplotlib.rcParams['pdf.fonttype'] = 42

from _util_updated import nested_dict
from _util_updated import turn_point
from _util_updated import load_data
from _util_updated import filter_umi

lib1_csv = sys.argv[1]

### path to sgRNA annotation file as defined by the input from the shell scrips

csv_DIR = sys.argv[2]
sg_csv = (pd.read_csv(csv_DIR , delimiter='\t', header = None))
sg_csv.columns = ('ID', 'Seq')


### This is the input for the library, defined in the shell script
lib_1 = pd.read_csv(lib1_csv , compression='gzip',header=0,index_col = 0, sep=',', quotechar='"')

#first library
AGGR_DF = pd.DataFrame()

curr_df = lib_1
cell_lib = '-' + str(1)
cell_list = []
for cell in curr_df.columns:
    cell_list.append(cell + cell_lib)
curr_df.columns = cell_list
AGGR_DF = AGGR_DF.append(curr_df.T)
         
AGGR_DF = AGGR_DF.T

# ## Drop NaNs from sgRNA
AGGR_DF.dropna(axis=0, inplace=True)


### generates an intermediate file before performing the elbow method to determine the cutoffs
AGGR_DF.to_pickle('./sgRNA_DF_sgDropNaN.pkl')

sg_seq = []
for sg in AGGR_DF .index:
    sg_seq.append(sg.split('_')[-1])
AGGR_DF.index = sg_seq

print("sg_seq length: ", len(sg_seq))

### Filter sgRNA using the elbow method
AGGR_DF_adj,cutoffs = filter_umi(AGGR_DF)
temp_DF = AGGR_DF_adj

#replace sequence with guide name
new_name = []
for seq in temp_DF.index:
        name_index = sg_csv[sg_csv.Seq == seq].index
        sgRNA_name = sg_csv.ID[name_index].tolist()[0]
        new_name.append(sgRNA_name)
temp_DF.index = new_name      
AGGR_DF_adj_Final = temp_DF.T
AGGR_DF_adj_Final =AGGR_DF_adj_Final[ AGGR_DF_adj_Final.sum(axis=1) > 0]

#remove cells with greater than a certain # of sgRNA
AGGR_DF_adj_Final_3 = AGGR_DF_adj_Final[AGGR_DF_adj_Final.sum(axis=1) == 1]

print("new_name length: ",len(new_name))

sg_bool = AGGR_DF_adj_Final > 0

#sg_bool.sum(axis=1) ==1
sg1 = sg_bool.index[sg_bool.sum(axis=1) ==1]
sg2 = sg_bool.index[sg_bool.sum(axis=1) ==2]
sg3 = sg_bool.index[sg_bool.sum(axis=1) ==3]
sg4 = sg_bool.index[sg_bool.sum(axis=1) ==4]
sgnon = sg_bool.index[sg_bool.sum(axis=1) == 0]


### Print out the metrics for this library 
print('\n sgrna (>0 sgRNA) dirty cells = ', len(sg_bool.index[sg_bool.sum(axis=1) >0]))
print('\n sgrna (exactly 1 sgRNA) clean cells = ',len(sg1))

print('\n mean sgRNA: ',np.mean(sg_bool.sum(axis=1)))


### generate a histogram of the sgRNA to cell association
plt.rcParams['font.size'] = 20
plt.hist(sg_bool.sum(axis=1), bins=45)
plt.xlabel('# sgRNA')
plt.ylabel('# cells')
plt.savefig('sgna_distribution.png')

AGGR_DF_adj_Final.to_pickle('sgRNA_DF.pkl')

