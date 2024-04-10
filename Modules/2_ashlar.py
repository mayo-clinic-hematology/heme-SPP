# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 13:59:52 2023

@author: M304399
"""

# https://github.com/labsyspharm/ashlar

from pathlib import Path
from natsort import natsorted

import numpy as np
import re

import matplotlib.pylab as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300
import tifffile
from tqdm import tqdm
import tempfile

import shutil
#%% This scripts divides the images into folders based on their cycle
# this is done because that is the input into ashlar

def ashlar_input_formatter(path_tiles_folder : str=None):
    
    path_tiles_folder = Path(path_tiles_folder) # convert to path object 
    
    assert path_tiles_folder is not None and path_tiles_folder.exists(), "Error: no or invalid input path"
    
    # output tiffs into here
    path_ashlar_inputs = path_tiles_folder.parent / "ashlar" / "ashlar_inputs"
    path_ashlar_inputs.mkdir(parents=True, exist_ok=True)
    
    # create ashlar outputs folder for docker
    path_ashlar_outputs = path_tiles_folder.parent / "ashlar" / "ashlar_outputs"
    path_ashlar_outputs.mkdir(parents=True, exist_ok=True)
    
    list_path_tiles = list(path_tiles_folder.rglob("*.tif"))
    list_path_tiles = natsorted(list_path_tiles)
    
    # determine unique number of regions 
    list_dir_regions = [r.name for r in path_tiles_folder.glob("*") if r.is_dir()]
        
    # get number of regions
    list_regions = []
    for dir_name in list_dir_regions:
        reg = dir_name.split("_")[0]
        if reg not in list_regions:
            list_regions.append(reg)
    
    # create stack for each regions
    for region in tqdm(list_regions[:]):

        pass
    
        # create cycle folder
        path_cycle_output = path_ashlar_inputs / region # / 't001'
        path_cycle_output.mkdir(parents=True, exist_ok=True)
        
        print(f"processing region: {region}")
        
        # get all images for this region
        list_path_images = [t for t in list_path_tiles if region in str(t)]
        
        # get unique markers based on unique file suffix
        list_suffix_markers = set()
        for path_image in list_path_images:
            pass
            _,_,_, marker_suffix = path_image.stem.split("_",3)
            list_suffix_markers.add(marker_suffix)
        list_suffix_markers = natsorted(list_suffix_markers)
        
        for channel_num, name_suffix in enumerate(list_suffix_markers, start=1):
            pass
        
            list_channel_tiles = list(filter(re.compile(f".*{name_suffix}.*").search, [str(p) for p in list_path_images]))
            list_channel_tiles = natsorted(list_channel_tiles)
            
            for path_tile in list_channel_tiles:
                pass
                basename, cycle, _, channel_ext = path_tile.rsplit("_", 3)
                channel, _ = channel_ext.split(".")
                new_channel = "c" + str(channel_num).zfill(3)
                filename = Path(path_tile).name.replace(cycle, "t001").replace(channel, new_channel)
                
                # skip file if already exists to avoid recopying
                path_new_file = path_cycle_output / filename
                
                if not path_new_file.exists():
                    # shutil.copy2(path_tile, path_new_file)
                    print(f"Copying: {path_tile} --> {path_new_file}")

            #%%
if __name__ == "__main__":
    
    # for each tile folder:
        
    # path_tiles_folder = Path(r"M:\Projects\DLBCL\20211222_CR082480A1_Villasboas_processed_computer\processed_2021-12-26\tiles")
    # path_tiles_folder = Path(r"M:\Projects\PTLD\20220203_LYMLEO452 PTLD A_Villasboas_processed_2022-02-10_tiles\tiles")
    

    path_projects = Path(r"M:\Projects\SMM")
    
    list_path_tiles = [p for p in path_projects.rglob("*tiles*")]
    
    for path_tiles_folder in list_path_tiles[:]:
        pass
        print(f"Processing: {path_tiles_folder.parent.name}")
        ashlar_input_formatter(path_tiles_folder)
    