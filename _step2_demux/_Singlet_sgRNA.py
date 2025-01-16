#!/usr/bin/env python3
# coding: utf-8


import scipy
import statistics
import scanpy as sc
import numpy as np
import pandas as pd
import matplotlib as mpl
import sys
import collections
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

hto_pkl = sys.argv[1]
sgrna_pkl = sys.argv[2]

### Dataframes from sgRNA and HTO outputs
Singlet_DF = pd.read_pickle(hto_pkl)
sgRNA_DF = pd.read_pickle(sgrna_pkl)


### Find all cells in singlet and sgRNA dataframes
overlap_cells = [i for i in Singlet_DF.index if i in sgRNA_DF.index]

#### Only keep cells also found in singlet df
Subset_DF = sgRNA_DF.loc[overlap_cells]

### Overlap the cells only found as HTO singlets, as well as containing sgRNAs
Subset_DF.to_pickle('final_combined_sgRNA_multiplets_HTO_singlets.pkl')

sg_bool = Subset_DF > 0

#sg_bool.sum(axis=1) ==1
sg1 = sg_bool.index[sg_bool.sum(axis=1) ==1]
sg2 = sg_bool.index[sg_bool.sum(axis=1) ==2]
sg3 = sg_bool.index[sg_bool.sum(axis=1) ==3]
sg4 = sg_bool.index[sg_bool.sum(axis=1) ==4]
sgnon = sg_bool.index[sg_bool.sum(axis=1) == 0]

### Output the metrics for the final overalap
print('\n \n clean cells (exacly 1 sgRNA) = ',len(sg1))
print('dirty cells (>0 sgRNA) = ',len(Subset_DF>1))

avg_sgrna = np.mean(sg_bool.sum(axis=1))
max_sgrna = np.max(sg_bool.sum(axis=1))

print('\n avg_sgrna: ', avg_sgrna)
print('max_sgrna', max_sgrna)


### generates a histogram of the final Singlet sgRNA per cell distribution 
plt.rcParams['font.size'] = 20
plt.hist(sg_bool.sum(axis=1), bins=30)
plt.xlabel('# sgRNA')
plt.ylabel('# cells')
plt.savefig('singlet_sgrna_distrib_updated.png')

