#!/usr/bin/env python3

import os
import re
import sys
import collections
import argparse
import tables
import itertools
import matplotlib
import numba


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
import scipy.sparse as sp_sparse

from multiprocessing import Pool
from collections import defaultdict
from scipy import sparse, io
from scipy.sparse import csr_matrix
from multiprocessing import Pool

np.random.seed(0)
print(str(sys.getrecursionlimit()), file=sys.stderr, flush=True)
sys.setrecursionlimit(100000)
print(str(sys.getrecursionlimit()), file=sys.stderr, flush=True)

# define the directory for the sub folders of all the different lanes to get the individual dataframes
DIR = '/project/GCRB/Hon_lab/s215194/Single_Cell/neuronal_pilot_02/'

# the library names for ALL the libraries in the directory, which you would like to aggregate
df_all = ['LWXX', ... ,'LWXX']

print('concatenating libraries', file=sys.stderr, flush=True)

# create the blank dataframe to subsequently append with each dataframe in the loop
idf = pd.DataFrame()

# create a counter that will number the libraries sequentially as  "-1" "-2" etc.
counter = 1

# open the dataframe, and loop through to add the counter to the cell ID so we know which library it comes from
for i in df_all:
    df = pd.read_pickle(DIR + str(i) + '/_step2_demux/'  + 'final_combined_sgRNA_multiplets_HTO_singlets.pkl').T
    df.columns = [i.split('-')[0] + ('-' + str(counter))  for i in df.columns ]
    
    print(i + ': ' + str(df.shape))
    _, x = idf.shape
    if x == 0:
        idf = df
    else:
        idf = pd.concat([idf, df], axis=1)
    counter= counter + 1
    print (counter)

# finally drop any NaN values that are in the datafram as an artefact of the concatenation
idf.dropna(axis=0, inplace=True)    
idf.to_pickle('aggr_combined_df_full.pkl')
                  
