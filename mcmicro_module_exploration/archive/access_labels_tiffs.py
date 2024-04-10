# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 12:04:54 2023

@author: M304399
"""

from pathlib import Path

import matplotlib.pylab as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300

from tifffile import TiffFile
import tifffile

from natsort import natsorted

from skimage.measure import regionprops_table
from numpy.ma import masked_array
import numpy as np

import pandas as pd
import math

import datetime

import seaborn as sns

path_project = Path(r"C:\Users\m304399\Desktop\20230620_TMA5Joker_Villasboas")

#%% LOAD IMAGES AND PLOT EXPRESSION ACROSS MASK

list_tiffs = [p for p in (path_project / 'reg001').glob("*") \
                   if 'reg001.tif' not in p.name and \
                       'Empty' not in p.name and \
                       'Blank' not in p.name]
list_tiffs = natsorted(list_tiffs)

path_mask = path_project / 'output' / 'SEGMASKS' / 'reg001_WholeCellMask.tiff' 

mask = tifffile.imread(path_mask).squeeze()

def intensity_median(roi_mask, roi_intensity):
    roi_mask_inverted = np.invert(roi_mask)
    masked_image = masked_array(roi_intensity, mask=roi_mask_inverted)       
    return np.ma.median(masked_image)
    
extra_properties = [intensity_median]

df_all_features = pd.DataFrame()

for path_image in list_tiffs[:]:
    pass
    dict_image_features = {}
    
    # parse filenames --> add metadata to dict
    reg, cycle, channel, marker = path_image.stem.split('_')
    cycle = int(cycle.replace("cyc",""))
    channel = int(channel.replace("ch",""))
    
    # load image to process
    im = tifffile.imread(path_image)
    
    # get regionprops for each region
    props = regionprops_table(mask, 
                              intensity_image=im, 
                              properties=['label',
                                          'area', 
                                          'eccentricity', 
                                          'intensity_mean',
                                          'feret_diameter_max'],
                              extra_properties=extra_properties)
    
    df = pd.DataFrame(props)
    
    df['reg'] = reg
    df['cycle'] = cycle
    df['channel'] = channel
    df['marker'] = marker
    
    df_all_features = pd.concat([df_all_features, df])
    
df_all_features['intensity_median_normalized'] = df_all_features['intensity_median'] / np.max(df_all_features['intensity_median'])

date = datetime.datetime.now()
date_str = f"{date.year}{date.month}{date.day}"
df_all_features.to_csv(path_project / f"{date_str}_whole_cell_features.csv")
#%% plot features

# Comment in features to plot
features_to_plot = [
            'area', 
            # 'intensity_mean',
            # 'feret_diameter_max',
            # 'intensity_median',
            # 'intensity_median_normalized'
            ]

# generates a list of markers to plot
list_markers = list(df_all_features['marker'].unique())

for marker in list_markers: # iterate through markers 
    for feat in features_to_plot:# iterate through features
        pass
        
        # creat subset of dataframe
        df_subset = df_all_features[(df_all_features['marker'] == marker) #&
                                    # (df_all_features['intensity_median'] < 200)
                                    ]
        # generate plot 
        sns.histplot(data=df_subset,
                     x = feat,
                     hue = 'marker',
                     # kde=True
                      # fill=False,
                     )
        plt.title(f"{marker} \n{feat}")
        plt.show()


#%% QC --> look at extreme values

outliers = df_all_features[(df_all_features['marker'] == 'NRX-70') &
                            (df_all_features['intensity_median'] > 4000)]
sns.histplot(data=outliers, x='intensity_median')





