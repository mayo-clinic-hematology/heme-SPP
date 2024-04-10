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

import shutil
#%% This scripts divides the images into folders based on their cycle
# this is done because that is the input into ashlar

# path_tiles_folder = Path(r"M:\Projects\DLBCL\20211222_CR082480A1_Villasboas_processed_computer\processed_2021-12-26\illumination_correction")
path_tiles_folder = Path(r"M:\Projects\DLBCL\20211222_CR082480A1_Villasboas_processed_computer\processed_2021-12-26\tiles")

# output tiffs into here
path_ashlar_inputs = path_tiles_folder.parent / "ashlar" / "ashlar_inputs"

list_path_tiles = list(path_tiles_folder.rglob("*.tif"))
list_path_tiles = natsorted(list_path_tiles)

# determine unique number of regions 
list_dir_regions = [r.name for r in path_tiles_folder.glob("*") if r.is_dir() and "fit_results" not in str(r)]
    
# get number of regions
list_regions = []
for dir_name in list_dir_regions:
    reg = dir_name.split("_")[0]
    if reg not in list_regions:
        list_regions.append(reg)

# create stack for each regions
for region in list_regions:
    pass
    
    print(f"processing region: {region}")
    
    # get all images for this region
    list_path_images = [t for t in list_path_tiles if region in str(t)]
    
    # get unique markers based on unique file suffix
    list_suffix_markers = set()
    for path_image in list_path_images:
        pass
        _,_,_, marker_suffix = path_image.stem.split("_",3)
        list_suffix_markers.add(marker_suffix)
    
    # get list of timepoints
    set_cycles = {s.split("_")[0] for s in list_suffix_markers}
    list_cycles = natsorted(list(set_cycles))
    
    # figure out which suffixes belong to this cycle
    for cycle in tqdm(list_cycles):
        pass
        
        path_cycle_output = path_ashlar_inputs / region / cycle
        path_cycle_output.mkdir(parents=True, exist_ok=True)
    
        list_path_cycle_images = natsorted([s for s in list_path_images if cycle in str(s)])

        # copy files into ashlar folder for processing
        for p in tqdm(list_path_cycle_images, mininterval=1):
            pass
            shutil.copy2(p, path_cycle_output / f"{p.name}")
        
#######

# "fileseries|/input/cycle1|pattern=reg001_X{row:2}_Y{col:2}_t001_z001_c{channel:3}.tif|width=3|height=21|overlap=0.3|pixel_size=0.377454"
   

# 5 images
# output_width = 6720 / 5
# output_height = 5040 / 5


    
    #%%
    # # iterate through suffixes and do illumination correction
    # for suffix in natsorted(list(list_suffix_markers))[:]:
    #     pass
    #     print(f"Processing:{region}_{suffix}")
    #     # get all images for this marker
    #     list_path_marker_images = [p for p in list_path_images if suffix in str(p)]
    #     list_path_marker_images = natsorted(list_path_marker_images)
        
    #     # create temporary array
    #     rows, cols = tifffile.imread(list_path_marker_images[0]).shape
    #     im_stack = np.zeros((len(list_path_marker_images), rows, cols))
        
    #     # creat stack of images
    #     for idx, im_path in enumerate(list_path_marker_images):
    #         pass
    #         im_stack[idx] = tifffile.imread(im_path)
            
    #     basic = BaSiC(get_darkfield=True, smoothness_flatfield=1)
    #     basic.fit(im_stack)
    #     images_transformed = basic.transform(im_stack)
        
    #     ################## plot fit results
    #     fig, axes = plt.subplots(1, 3, figsize=(9, 3))
    #     fig.suptitle(f"marker suffix: {suffix}")
    #     im = axes[0].imshow(basic.flatfield)
    #     fig.colorbar(im, ax=axes[0])
    #     axes[0].set_title("Flatfield")
    #     im = axes[1].imshow(basic.darkfield)
    #     fig.colorbar(im, ax=axes[1])
    #     axes[1].set_title("Darkfield")
    #     axes[2].plot(basic.baseline)
    #     axes[2].set_xlabel("Frame")
    #     axes[2].set_ylabel("Baseline")
        
    #     fig.tight_layout()
        
    #     path_fit_results = path_output / "fit_results"
    #     path_fit_results.mkdir(exist_ok=True)
    #     plt.savefig(path_fit_results / f"{region}_marker_suffix_{suffix}.tiff")
    #     plt.show()
        
    #     ######### visualize illumination correction for each image
    #     # for idx, (im_original, path_im) in enumerate(zip(im_stack,list_path_marker_images)):
    #     #     pass
            
    #     #     fig, ax = plt.subplots(1,2,figsize=(20,7))
    #     #     fig.suptitle(f"{path_im.stem}")
            
    #     #     vmax=5000
            
    #     #     ax[0].set_title("original")
    #     #     ax[0].imshow(im_original, vmax=vmax)
            
    #     #     ax[1].set_title("illumination_corrected")
    #     #     ax[1].imshow(images_transformed[idx], vmax=vmax)
            
    #     #     plt.show()
        
    #     # # visualize correction
    #     # plt.imshow(im_stack[0]) 
    #     # plt.imshow(images_transformed[0])
    #     # plt.imshow(im_stack[0] - images_transformed[0], vmax=92, vmin=0)
            
    #     ######## save images for this marker
    #     for idx, (im, path_im) in enumerate(zip(images_transformed, list_path_marker_images)):
    #         pass
    #         # create folder
    #         path_im_output = path_output / path_im.parent.stem
    #         path_im_output.mkdir(exist_ok=True)
            
    #         # save image 
    #         tifffile.imwrite(path_im_output / path_im.name, im)
    #         print(path_im_output / path_im.name)

        