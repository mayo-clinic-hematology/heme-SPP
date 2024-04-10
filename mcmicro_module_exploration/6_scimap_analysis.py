# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 09:06:03 2023

@author: M304399
"""

from pathlib import Path

import tifffile
from tifffile import TiffFile
from collections import defaultdict

import matplotlib.pylab as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300

from pprint import pprint

import anndata as ad
import scimap as sm
import pandas as pd
import scanpy as sc

import seaborn as sns

from natsort import natsorted

from skimage.measure import regionprops_table
#%% Load data

# paths to dataset
path_project = Path(r"Y:\003 CODEX\MCMICRO\SMM_project\20230522_BR1010694BR1034362_Gonsalves_3_membrane")
path_gates = path_project / r"gates\SMM_20230522_BR1010694BR1034362_Gonsalves_3_membrane_median_reg001_gated_channel_ranges.csv (10).csv"
path_channel_names = path_project / "markers.csv"
path_signature_matrix = Path(r"M:\Projects\Villasboas-CODEX/phenotype_workflow.csv")

# load image 
path_image = path_project / r"registration\reg001.ome.tiff"


#%% Compute MCMICRO and Signature matrix marker overlap
# Load signature matrix for phenotyping 
df_phenotype = pd.read_csv(path_signature_matrix) # signature matrix to be fed into scimap
list_phenotype_markers = [item for item in list(df_phenotype.keys()) if "Unnamed" not in item]
list_phenotype_markers.append('Ki-67')

# load MCMICRO quantification
path_mcmicro_csv = path_project / r"quantification\median_reg001--mesmer_cell.csv"
df_mcmicro = pd.read_csv(path_mcmicro_csv)
list_mcmicro_markers = [k.rsplit("_",2)[0] for k in list(df_mcmicro.keys()) if 'intensity' in k]

# compute markers overlap
list_marker_overlap = list(set(list_phenotype_markers).intersection(list_mcmicro_markers))
#%%
# filter signature matrix based on markers that we have
list_to_subset_signature_matrix = [v for v in df_phenotype.keys() \
                                   if v in list_marker_overlap or \
                                   "Unnamed" in v
                                       ]

df_phenotype = df_phenotype[list_to_subset_signature_matrix]

list_markers = [f"{v}_intensity_median" for v in list_marker_overlap] + \
            ['CellID', 'X_centroid', 'Y_centroid', 'Area', 'MajorAxisLength', 'MinorAxisLength', 'Eccentricity', 'Solidity', 'Extent', 'Orientation']

list_remove = [k for k in list(df_mcmicro.keys()) if k not in list_markers]

adata = sm.pp.mcmicro_to_scimap([path_mcmicro_csv], drop_markers=list_remove)

df_manual_gate = pd.read_csv(path_gates)

df_gates =  df_manual_gate[['channel', 'gate_start']]

adata = sm.pp.rescale(adata, gate=df_gates)

#%%

dict_rename = {k : f"{k}_intensity_median" for k in list_phenotype_markers}
df_phenotype = df_phenotype.rename(columns=dict_rename)

adata = sm.tl.phenotype_cells (adata, phenotype=df_phenotype,
                               label="phenotype", 
                               # pheno_threshold_abs= 10
                               ) 

adata.obs['phenotype'].value_counts()


#%% visualize phenotyping

# df_channel_names = pd.read_csv(path_channel_names)
# list_channels = list(df_channel_names['marker_name'].values)

# sm.pl.image_viewer(path_image, adata, 
#                    overlay = 'phenotype', 
#                    point_color='white', 
#                    point_size=6,
#                    markers=list_marker_overlap,
#                    channel_names=list_channels
#                    )


# View Leiden clustering
# sm.pl.image_viewer(image_path, adata, overlay = 'leiden', point_color='white', point_size=6)

#%%
# #%% Create anndata object from df

# # generate matrix of markers
# list_metadata = ['CellID',
#                 'X_centroid',
#                 'Y_centroid',
#                 'Area',
#                 'MajorAxisLength',
#                 'MinorAxisLength',
#                 'Eccentricity',
#                 'Solidity',
#                 'Extent',
#                 'Orientation'
#                 ]

# list_markers = [s for s in df.keys() if "median" in s ]
# # list_markers = [s for s in df.keys() if "median" not in s and\
# #                                         "intensity" not in s and\
# #                                         "gini" not in s and\
# #                                         s not in list_metadata
# #                 ]

# # load dataframe and subset by markers
# df_counts = df[list_markers]

# ### rename markers 
# dict_cols_renamed = {c:c.rsplit('_',2)[0] for c in list_markers}
# df_counts = df_counts.rename(columns=dict_cols_renamed)

# # only keep selected markers 
# # path_selected_markers  = Path(r"M:\Projects\DLBCL\MDH_phenotype_workflow\phenotype_workflow.csv")
# # df_selected_markers = pd.read_csv(path_selected_markers)
# # df_selected_markers = [m for m in df_selected_markers.keys() if "Unnamed" not in m]
# # df_counts = df_counts[df_selected_markers]


# ## assemble anndata object
# adata = ad.AnnData(df_counts)
# adata.obs = df[list_metadata]
# adata.uns['all_markers'] = list(df_counts.keys())
# adata.raw = adata.copy()

# #%% ################## specific for QuPath quantification files
# # dict_marker_status = {}
# # for m in list_markers:
# #     if "DAPI" in m or "Background" in m:    
# #         dict_marker_status[m] = "n/a"
# #     else:
# #         dict_marker_status[m] = ""

# # # adata counts
# # df_marker_status = pd.DataFrame(dict_marker_status, columns=['marker', ''])
# # list_marker_to_exclude = [m for m in adata.var.index if 'DAPI' in m or "Background" in m ]
# # df_markers = df[list_markers]

# ## rename columns 
# # dict_cols_renamed = {c:c.split(':')[0] for c in df_markers.keys()}
# # df_markers = df_markers.rename(columns=dict_cols_renamed)

# # get positions
# # list_obs = [ 'Centroid X µm', 'Centroid Y µm', 'Area µm^2'] # 'cellid', 'Area um^2'
# # df_positions = df[list_obs].copy()
# # df_positions.loc[:,'X_centroid'] = df_positions['Centroid X µm'] / 377.47e-3
# # df_positions.loc[:,'Y_centroid'] = df_positions.loc[:,'Centroid Y µm'] / 377.47e-3
# # df_positions = df_positions.rename(columns= {'Centroid X um': 'X_centroid', 'Centroid Y um' : 'Y_centroid'})

# #%% Create anndata object

# # drop features 
# # list_marker_to_exclude = [m for m in adata.var.index if 'DAPI' in m or "Blank" in m or "Empty" in m ]
# # adata = sm.hl.dropFeatures(adata, \
# #                            drop_markers=list_marker_to_exclude,
# #                                 subset_raw=False
# #                                )

# # print(f"Markers used")
# # for m in adata.var.index:
# #     print(m)

# #%% Visualize highly expressed markers 

# sc.pl.highest_expr_genes(adata, n_top=20)

# sc.tl.pca(adata, svd_solver='arpack')
# sc.pl.pca(adata, color='CD68')

# # sc.pl.pca_variance_ratio(adata)
# # adata.write("scimap_data.h5ad")

# sns.histplot(adata.obs['Area'])

# #%% Create neighborhood graph and visualize UMAP's

# sc.pp.neighbors(adata, n_neighbors=30, n_pcs=10)
# sc.tl.umap(adata)
# sc.pl.umap(adata, color=['CD4',
#                          'CD8',
#                          'CD45',
#                          'CD3e',
#                          'CD20'
#                          ],
#            # cmap='vlag',
#            use_raw=False,
#            )

# sc.tl.leiden(adata, resolution=.5)

# sc.pl.umap(adata, color=['leiden', 
#                          'CD3e',
                         
#                          ],
#                # cmap='vlag'
#               wspace= .25 ,
#            )

# #%% RANK GENES BY CLUSTER

# sc.tl.rank_genes_groups(adata, 'leiden', method='t-test')
# sc.pl.rank_genes_groups(adata, n_genes=10, sharey=False, fontsize=16)
# #%% 

# path_image = path_project / "ashlar/ashlar_outputs/reg005.ome.tiff"
# marker_of_interest = 'CD3e'

# sm.pl.gate_finder(path_image, adata, marker_of_interest,
#                   from_gate=5, to_gate=9, increment=0.1,
#                     markers=['CD45', 'CD3e', 'CD8', 'CD20', 'CD21']
#                    )

# #%%

# sm.pp.rescale(adata, gate="gate_file.csv",)
# #%% 







