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

### Path to HTO demultiplex output. This combines them and then makes the call of which cells are singlets. Important, this does not call HTO. that is done in FBA, make sure you use demultiplex output
lib_1 = pd.read_csv(lib1_csv, compression='gzip',header=0,index_col = 0, sep=',', quotechar='"')

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

### Remove multiple HTO cells
singlets = []
multiplets = []
for cell in AGGR_DF.columns:
    if AGGR_DF[cell].sum() == 1:
        singlets.append(cell)
    elif AGGR_DF[cell].sum() > 1:
        multiplets.append(cell)

### Print out the metrics for this library into the out file
print ( '\n hto singlets:',len(singlets))
print ('hto multiplets:',len(multiplets))

AGGR_DF_Singlets = AGGR_DF[singlets].T


AGGR_DF_adj_Final = AGGR_DF

sg_bool = AGGR_DF_adj_Final > 0

sg1 = sg_bool.index[sg_bool.sum(axis=1) ==1]
sg2 = sg_bool.index[sg_bool.sum(axis=1) ==2]
sg3 = sg_bool.index[sg_bool.sum(axis=1) ==3]
sg4 = sg_bool.index[sg_bool.sum(axis=1) ==4]
sgnon = sg_bool.index[sg_bool.sum(axis=1) == 0]
sum(sg_bool.sum(axis=0) >0)
#sg_bool.index[sg_bool.sum(axis=0) ==1]


### Generate a Histogram of the number of HTOs per cell
len(sg1)
np.mean(sg_bool.sum(axis=1))
plt.rcParams['font.size'] = 20
plt.hist(sg_bool.sum(axis=0), bins=45)
plt.xlabel('# HTO')
plt.ylabel('# cells')
plt.savefig('./HTO_distribution.png')


### Save the singlets to a pickle file that will contain the oligo barcode to cell association
AGGR_DF_Singlets.to_pickle('HTO_Singlets_DF.pkl')
