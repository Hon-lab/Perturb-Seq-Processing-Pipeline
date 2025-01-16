#!/usr/bin/env python3
#coding: utf-8

import numpy as np
import pandas as pd
import statistics as st
import re
import csv
import scanpy as sc 
import scanpy.external as sce
import phate
import matplotlib
from matplotlib import pyplot as plt
import warnings
from scipy.stats import binom
from scipy.stats import multinomial
import seaborn
from scipy.stats import hypergeom
import warnings
warnings.filterwarnings('ignore')


def adjust_feature(feature_matrix, feature_id):
    c, f = feature_matrix.shape
    feature_matrix = feature_matrix.copy().todense()
    
    for i in np.arange(f):
        feature_umi_array = np.asarray(feature_matrix[:,i]).squeeze()

        feature_umi_array_sort = feature_umi_array[np.argsort(feature_umi_array * -1)]
        feature_cumsum = np.cumsum(feature_umi_array_sort)

        cell_num = np.sum(feature_umi_array_sort > 0)

        turn_point = np.sum(np.diff(feature_cumsum) / np.sum(feature_umi_array) > (1 / cell_num))
        feature_matrix[np.where(feature_umi_array < feature_umi_array_sort[turn_point]), i] = 0
        
    return feature_matrix

# # change this for the right source directory for the files 
working_dir = '/project/GCRB/Hon_lab/s215194/Single_Cell/neuronal_pilot_02/_all_exp_combined/aggr_transcriptome/neuro_pilot_02_no_normalization_all/outs/count/'
ds = sc.read_10x_h5(working_dir + 'filtered_feature_bc_matrix.h5', gex_only=False)

ds.var_names_make_unique()
ds.obs_names_make_unique()

# Load and remove non-singlets and non-sgRNA cells

# # set this to the directory of the singlets
Singlet_DF = pd.read_pickle('/project/GCRB/Hon_lab/s215194/Single_Cell/neuronal_pilot_02/_all_exp_combined/aggr_dataframe/aggr_combined_df_full.pkl')

Singlet_DF = Singlet_DF.T ## transform the gRNA dataframe to keep rownames as cell ID
index_1 = Singlet_DF.index
index_2 =ds.obs.index
res = index_1.intersection(index_2, sort=None)
ds_sg = ds[res]

print('Percent of cells with sgRNA: ' + str(ds_sg.shape[0]/ds.shape[0]))

# uncomment out if you want to save at this point 
# ds_sg.write('/directory/exp_name_sgRNACells_filtered_no_embedding_no filter_am.h5ad')
# print('saved exp_name_sgRNACells_filtered_no_embedding_no filter_am.h5ad ')


######
######
######


#merget gene index
c_num, g_num = ds_sg.X.shape

all_singlet_idx = np.asarray(ds_sg.obs.index)


#get the high mito cells
mt_index = ds_sg.var.index[ds_sg.var.index.str.startswith('MT-')].tolist()
mt_expr = np.sum(ds_sg[:,mt_index].X, axis=1)
depth = np.sum(ds_sg.X, axis=1)
high_mito_idx = np.argwhere((mt_expr / depth) > 0.2)[:,0].squeeze()

#get the gene and cell index
chosen_cell_index = np.setdiff1d(all_singlet_idx, all_singlet_idx[high_mito_idx])

#filter the matrix
adata = ds_sg[chosen_cell_index, :]

sc.pp.filter_genes(adata, min_counts=1)         # only consider genes with more than 1 count
sc.pp.normalize_per_cell(adata, key_n_counts='n_counts_all') # normalize with total UMI count per cell # select highly-variable genes  # subset the genes

# normalize and add the raw data to the matrix 
sc.pp.log1p(adata)
adata.raw = adata
sc.pp.scale(adata) 


# save at this point to have the filtered matrix without any embeddings added yet
adata.write('/directory/exp_name_sgRNACells_filtered_no_embedding_filtered_all.h5ad')




######
######
######
######
######

## Define sets of markers that you would like to see the feature plots for and save below
## only done this way to skip having to define them later on mutiple times

 markers = ['louvain','TBX5', 'MALAT1', 'NPPA', 
            'TNNT2','ACTA2','FN1','IRX2', 'SOX2', 'DCX', 'LUM', 
            'ISL1', 'WT1', 'EPCAM', 'EOMES', 'HAND1', 'MESP1', 'ROR2']

markers2 = [ 'louvain', 'TNNT2', 'FN1', 'NPPA', 'ACTA2', 'IRX4', 'MYH7', 'HEY2', 'SOX4', 'NKX2-5','ISL1']

markers3 =['louvain','COL1A1', 'PLVAP','TTR', 'SOX2']

nsc_markers = ['louvain','FABP7','EGFR','EGR1','PCGF5','RELN','SLC1A3','NR2E1']

nsc_markers2 = ['louvain','POU3F2','FGFR1','MAP2','NEFL','NR4A2','PAX3','PAX6','S100B','SOX11','SOX21','SOX4','EOMES','TUBB3']

ag_markers = ['louvain','AQP4','AQP9','GFAP','ASCL1','DCX','RBFOX3']



### Cluster Cells

sc.tl.pca(adata, random_state= 0)
sc.pp.neighbors(adata,use_rep='X_pca',random_state = 0)

#assign louvain clusters, increased resolution means increased cluster number
sc.tl.louvain(adata,resolution = 0.2,random_state = 0)
params = 'resolution = 0.1'
print('\n louvain(adata,resolution = 0.2,random_state = 0')

sc.pp.neighbors(adata,use_rep='X_pca',random_state = 0)

sc.tl.paga(
    adata,
    groups='louvain', 
)

sc.pl.paga(
    adata, 
    color=['louvain'], 
    use_raw=True,
    layout='fr',
    threshold=0.01,
    node_size_scale=0.5,
    node_size_power=0.9,
    edge_width_scale=1,
)

sc.tl.umap(
    adata,
    init_pos='paga',
    random_state = 0
)

# Save the newly created umap embedding to your directory
adata.write('/directory/exp_name_sgRNACells_filtered_w_embedding_all.h5ad')

sc.pl.umap(
    adata,
    color=['louvain'], 
    vmin=0,  legend_loc='on data', legend_fontsize=8, save='louvain' + params + '.png', title=params
)

clus0cells = adata[adata.obs.louvain=='0']
print=('cluster 0 cells =', clus0cells)
clus1cells = adata[adata.obs.louvain=='1']
print=('cluster 1 cells =', clus1cells)
clus2cells = adata[adata.obs.louvain=='2']
print=('cluster 2 cells =', clus2cells)
clus3cells = adata[adata.obs.louvain=='3']
print=('cluster 3 cells =', clus3cells)
clus3cells = adata[adata.obs.louvain=='4']
print=('cluster 4 cells =', clus3cells)
 

sc.pl.umap(
    adata,
    color=markers, 
    vmin=0,  legend_loc='on data', legend_fontsize=8, save='markers' + params + '.png', title=params
)

sc.pl.umap(
    adata,
    color=markers2, 
    vmin=0,  legend_loc='on data', legend_fontsize=8, save='markers2' + params + '.png', title=params
)

sc.pl.umap(
    adata,
    color=markers3, 
    vmin=0,  legend_loc='on data', legend_fontsize=8, save='markers3' + params + '.png', title=params
)

sc.pl.umap(
    adata,
    color=nsc_markers, 
    vmin=0,  legend_loc='on data', legend_fontsize=8, save='nsc_markers' + params + '.png', title=params
)

sc.pl.umap(
    adata,
    color=nsc_markers2, 
    vmin=0,  legend_loc='on data', legend_fontsize=8, save='nsc_markers2' + params + '.png', title=params
)

sc.pl.umap(
    adata,
    color=ag_markers, 
    vmin=0,  legend_loc='on data', legend_fontsize=8, save='ag_markers' + params + '.png', title=params
)

