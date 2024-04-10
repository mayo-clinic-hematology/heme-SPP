# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 10:04:23 2024

@author: m304399
"""
from pathlib import Path
from natsort import natsorted

import numpy as np

import pandas as pd
#%% This scrip generates the marker.csv files for each of the regions given a path to the stitched images folder


path_stitched_dirs = Path(r"Z:\CODEX Processed files\20220203_LYMLEO452 PTLD A_Villasboas\processed_2022-02-10\stitched")
path_output = Path(r"M:\Projects\PTLD\20220203_LYMLEO452 PTLD A_Villasboas_processed_2022-02-10_tiles\ashlar\ashlar_outputs")


# select for "reg###" folders
list_reg_dirs = [p for p in list(path_stitched_dirs.glob("*")) if "reg" in str(p.stem) and p.is_dir()]


dict_filters = {1 : "DAPI",
                2 : "AF750",
                3 : "Atto550",
                4 : "Cy5"
                }

# iterate through folders
for path_dir in list_reg_dirs[:1]: # grab the first one only since they are all the same
    pass
    list_files = path_dir.glob(f"{path_dir.name}_*.tif") # exclude the complete tiff stack generated
    list_files_sorted = natsorted(list_files)
    
    
    ##marker file structure: channel_number, cycle_number, marker_name, filter
    
    # channel_number = index
    list_channel_number = np.arange(len(list_files_sorted)) + 1
    
    list_cycle_number = [int(m.stem.split("_",2)[1].replace("cyc","")) for m in list_files_sorted]
    
    list_markers = [m.stem.rsplit("_",1)[1] for m in list_files_sorted]
    
    # list_filter
    list_filter = [int(m.stem.split("_",3)[2].replace("ch","")) for m in list_files_sorted]
    pd_series_filters = pd.Series(list_filter).map(dict_filters)
    
    
    df = pd.DataFrame({'channel_number' : list_channel_number, 
                       'cycle_number' : list_cycle_number, 
                       'marker_name' : list_markers, 
                       'filter' : pd_series_filters})
    
    path_output_csv = path_output / f"markers.csv"
    print(f"Output: {path_output_csv}")
    df.to_csv(path_output_csv, index=False)
    
    
    

