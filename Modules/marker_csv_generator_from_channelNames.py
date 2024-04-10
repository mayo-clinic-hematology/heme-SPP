# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 10:04:23 2024

@author: m304399
"""
from pathlib import Path
from natsort import natsorted

import numpy as np

import pandas as pd
#%% This scrip generates the marker.csv file given a channelsname.csv file

path_dataset = [p / "channelNames.txt" for p in Path(r"M:\Projects\SMM").glob("*") if p.is_dir()]

for path_channel_names in path_dataset:
    pass
    df_channel_names = pd.read_csv(path_channel_names , names = ["marker_name"])
    
    dict_filters = {1 : "DAPI",
                    2 : "AF750",
                    3 : "Atto550",
                    4 : "Cy5"
                    }
    
    # channel_number = index
    list_channel_number_in_cycle = [idx % 4 + 1 for idx in np.arange(len(df_channel_names))]
    list_channel_number = np.arange(len(df_channel_names)) + 1

    list_cycle_number = [idx //4 + 1 for idx in np.arange(len(df_channel_names))]
    list_markers = df_channel_names['marker_name'].values
    
    pd_series_filters = pd.Series(list_channel_number_in_cycle).map(dict_filters)
    
    df = pd.DataFrame({'channel_number' : list_channel_number, 
                       'cycle_number' : list_cycle_number, 
                       'marker_name' : list_markers, 
                       'filter' : pd_series_filters})
    
    path_output_csv = path_channel_names.parent / "markers.csv"
    
    print(f"Output: {path_output_csv}")
    df.to_csv(path_output_csv, index=False)

#%%

df_first = None
df_sum = pd.DataFrame()

for pos, p in enumerate(path_dataset):
    pass
    if df_first is None:
        df_first = pd.read_csv(p)
        df_sum[pos] = df_first
    else:
        df_second  = pd.read_csv(p)
        equals = df_first.equals(df_second)
        print(equals)
        df_sum[pos] = df_second


