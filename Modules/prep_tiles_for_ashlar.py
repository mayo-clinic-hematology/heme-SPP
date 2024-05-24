# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 13:59:52 2023

@author: M304399
"""

# https://github.com/labsyspharm/ashlar
import argparse,re,shutil
from pathlib import Path
from natsort import natsorted
from tqdm import tqdm
import pandas as pd
import numpy as np
# This scripts divides the images into folders based on their cycle to format as input into ashlar

def ashlar_input_formatter(path_tiles_folder : str=None):
    
    path_tiles_folder = Path(path_tiles_folder) # convert to path object 
    
    assert path_tiles_folder is not None and path_tiles_folder.exists(), "Error: no or invalid input path"
    
    # output tiff directory
    path_ashlar_inputs = path_tiles_folder.parent / "raw"
    path_ashlar_inputs.mkdir(parents=True, exist_ok=True)
    
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
    
    # create stack for each region
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
                    shutil.copy2(path_tile, path_new_file)
                    # print(f"Copying: {path_tile} --> {path_new_file}")

def marker_csv_generator(path_project : str=None):

    ch_names = Path(path_project / "channelNames.txt")

    df_channel_names = pd.read_csv(ch_names , names = ["marker_name"])

    dict_filters = {1 : "DAPI",
                    2 : "AF750",
                    3 : "Atto550",
                    4 : "Cy5"
                    }

    # channel_number = index
    list_channel_number_in_cycle = [idx % 4 + 1 for idx in np.arange(len(df_channel_names))]
    list_channel_number = np.arange(len(df_channel_names)) + 1

    list_cycle_number = [idx // 4 + 1 for idx in np.arange(len(df_channel_names))]
    list_markers = df_channel_names['marker_name'].values

    pd_series_filters = pd.Series(list_channel_number_in_cycle).map(dict_filters)

    df = pd.DataFrame({'channel_number' : list_channel_number, 
                    'cycle_number' : list_cycle_number, 
                    'marker_name' : list_markers, 
                    'filter' : pd_series_filters})

    # path_output_csv = path_project.parent / "markers.csv"
    path_output_csv = path_project / "markers.csv"

    print(f"Output: {path_output_csv}")
    df.to_csv(path_output_csv, index=False)


if __name__ == "__main__":

        # Enable for testing script locally
    if False:
        # set arguments for testing
        import sys
        sys.argv.extend(['-i', '/home/mdhowe/projects/MM_risk_radiomics/data'])

    parser = argparse.ArgumentParser(description='Convert CODEX processor directory to OME.TIFs')
    parser.add_argument('-i', '--indir', help='MCMICRO formatted directory containing a tiles directory and channelNames.txt list', nargs='?', type=str, dest="cdxDir", metavar="DIR",required=True)

    args = parser.parse_args()
    path = Path(args.cdxDir)
    
    list_path_tiles = [p for p in path.rglob("*tiles*")]
    
    for path_tiles_folder in list_path_tiles[:]:
        pass
        print(f"Processing: {path_tiles_folder.parent.name}")
        ashlar_input_formatter(path_tiles_folder)

    marker_csv_generator(path)