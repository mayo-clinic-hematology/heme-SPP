# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 10:07:02 2023

@author: M304399
"""

from pathlib import Path
import tifffile


import matplotlib.pylab as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi']=300

import pandas as pd

import numpy as np
#%%

path_project = Path(r"M:\Projects\DLBCL")

# csv
path_classifications = path_project / r"phenotype analysis\SCIMAP\DLBCL_GITR_ROI005_cell_phenotypes.csv"
path_features = path_project / r"phenotype analysis\SCIMAP\allmarkers_reg005_qcd_withids_added_GITR.csv"

#images
path_ome_tiff = path_project / r"20211222_CR082480A1_Villasboas\OMETIFF\reg005.ome.tiff"
path_mask = path_project / r"20211222_CR082480A1_Villasboas\SEGMASKS\reg005_WholeCellMask.tiff"


df_classifications = pd.read_csv(path_classifications)
df_classifications = df_classifications.drop(['Unnamed: 0'], axis=1)

df_features = pd.read_csv(path_features)
df_features['label'] = df_features['cellid'].apply(lambda x : x.split("_")[1])

# join based on object_id
df_joined = df_features.join(df_classifications.set_index("object_id"), on="Object ID")
df_joined['label'] = df_joined['label'].astype({'label':'int32'}) 

# Subset data frames into unknowns
df_celesta_unknown = df_joined[(df_joined["CELESTA_class"]=='Unknown') |
                               (df_joined["CELESTA_class"]==('Other cells'))
                               ]
df_seurat_unknown = df_joined[df_joined['Seurat_class']=='Unclassifiable']


# calculate similar unknowns on both datasets
df_both_unknown = df_joined[(df_joined['Seurat_class']=='Unclassifiable') &
                            ((df_joined["CELESTA_class"]=='Unknown') |
                             (df_joined["CELESTA_class"]==('Other cells')))
                             ]

#%% Visualize mask overlap based on classifications

# Modify mask
path_output = Path(r"M:\Projects\DLBCL\unknowns analysis")

mask = tifffile.imread(path_mask).squeeze()

# create mask of celeste unknowns
mask_celeste = np.full(mask.shape,fill_value=False)
for l in df_celesta_unknown['label'][:]:
    pass
    mask_celeste[mask==l] = True
tifffile.imwrite(path_output / "mask_celeste_unknowns.tiff", mask_celeste)

# create mask of seurat unknowns
mask_seurat = np.full(mask.shape,fill_value=False)
for l in df_seurat_unknown['label'][:]:
    pass
    mask_seurat[mask==l] = True 
tifffile.imwrite(path_output / "mask_seurat_unclassifiables.tiff", mask_seurat)

# compute bitwise AND for cells missing in both
mask_and = np.bitwise_and(mask_celeste,mask_seurat)
tifffile.imwrite(path_output / "mask_seurat_celeste_bitwise_and.tiff", mask_and)






