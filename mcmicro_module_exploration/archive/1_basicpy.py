# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 15:42:19 2023

@author: M304399
"""
from pathlib import Path
from natsort import natsorted

import numpy as np
import re

import matplotlib.pylab as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300

import tifffile

from tqdm import tqdm

from basicpy import BaSiC
#%%
path_tiles_folder = Path(r"M:\Projects\DLBCL\20211222_CR082480A1_Villasboas_processed_computer\processed_2021-12-26\tiles")

path_output = path_tiles_folder.parent / "illumination_correction"
path_output.mkdir(exist_ok=True)

list_path_tiles = list(path_tiles_folder.rglob("*.tif"))
list_path_tiles = natsorted(list_path_tiles)

# determine unique number of regions 
list_dir_regions = [r.name for r in path_tiles_folder.glob("*") if r.is_dir()]

list_regions = []
for dir_name in list_dir_regions:
    reg = dir_name.split("_")[0]
    if reg not in list_regions:
        list_regions.append(reg)

# create stack for each regions
for region in list_regions:
    pass
    print(f"correcting region: {region}")
    
    # get all images for this region
    list_path_images = [t for t in list_path_tiles if region in str(t)]
    
    # get unique markers based on unique file suffix
    list_suffix_markers = set()
    for path_image in list_path_images:
        pass
        _,_,_, marker_suffix = path_image.stem.split("_",3)
        list_suffix_markers.add(marker_suffix)
        
    # iterate through suffixes and do illumination correction
    for suffix in tqdm(natsorted(list(list_suffix_markers))[:]):
        pass
        print(f"Processing:{region}_{suffix}")
        # get all images for this marker
        list_path_marker_images = [p for p in list_path_images if suffix in str(p)]
        list_path_marker_images = natsorted(list_path_marker_images)
 
        # visualize images in this set
        # for p in list_path_marker_images[:]:
        #     pass
        #     im_temp = tifffile.imread(p)
            
        #     plt.title(p.name)
        #     plt.imshow(im_temp)
        #     plt.show()
        
        # create temporary array
        rows, cols = tifffile.imread(list_path_marker_images[0]).shape
        im_stack = np.zeros((len(list_path_marker_images), rows, cols)) # , dtype=np.int16
        
        # creat stack of images
        for idx, im_path in enumerate(list_path_marker_images[:]):
            pass
            im_stack[idx] = tifffile.imread(im_path, dtype=np.int32)
            
        basic = BaSiC(get_darkfield=True, smoothness_flatfield=1)
        basic.fit(im_stack)
        images_transformed = basic.transform(im_stack)
        
        #####
        # idx_plot = 0
        # plt.imshow(im_stack[idx_plot])
        # plt.show()
        
        # plt.imshow(images_transformed[idx_plot])
        # plt.show()
        
        # plt.imshow(im_stack[idx_plot] - images_transformed[idx_plot])
        # plt.show()
        # #####
        
        ################## plot fit results
        fig, axes = plt.subplots(1, 3, figsize=(9, 3))
        fig.suptitle(f"{region} | marker suffix: {suffix}")
        im = axes[0].imshow(basic.flatfield)
        fig.colorbar(im, ax=axes[0])
        axes[0].set_title("Flatfield")
        im = axes[1].imshow(basic.darkfield)
        fig.colorbar(im, ax=axes[1])
        axes[1].set_title("Darkfield")
        axes[2].plot(basic.baseline)
        axes[2].set_xlabel("Frame")
        axes[2].set_ylabel("Baseline")
        
        fig.tight_layout()
        
        path_fit_results = path_output / "fit_results"
        path_fit_results.mkdir(exist_ok=True)
        # plt.savefig(path_fit_results / f"{region}_marker_suffix_{suffix}.tiff")
        plt.show()
        
        ######### visualize illumination correction for each image
        # for idx, (im_original, path_im) in enumerate(zip(im_stack,list_path_marker_images)):
        #     pass
            
        #     fig, ax = plt.subplots(1,2,figsize=(20,7))
        #     fig.suptitle(f"{path_im.stem}")
            
        #     vmax=5000
            
        #     ax[0].set_title("original")
        #     ax[0].imshow(im_original, vmax=vmax)
            
        #     ax[1].set_title("illumination_corrected")
        #     ax[1].imshow(images_transformed[idx], vmax=vmax)
            
        #     plt.show()
        
        # # visualize correction
        # plt.imshow(im_stack[0]) 
        # plt.imshow(images_transformed[0])
        # plt.imshow(im_stack[0] - images_transformed[0], vmax=92, vmin=0)
            
        ######## save images for this marker
        for idx, (im, path_im) in enumerate(zip(images_transformed, list_path_marker_images)):
            pass
            # create folder
            path_im_output = path_output / path_im.parent.stem
            path_im_output.mkdir(exist_ok=True)
            
            # save image
            #TODO BaSicPy outputs negative values which become huge
            # if converted to ints, try taking abs values instead first?
            tifffile.imwrite(path_im_output / path_im.name, abs(im.astype(np.int32)))
            print(path_im_output / path_im.name)

        
#%%%% BaSiCPY example

# from basicpy import BaSiC
# from basicpy import datasets as bdata
# from matplotlib import pyplot as plt

# images = bdata.wsi_brain()

# for im in images[:20]:
#     # plt.imshow(images[12])
#     plt.imshow(im)
#     plt.show()

# basic = BaSiC(get_darkfield=True, smoothness_flatfield=1)
# basic.fit(images)

# images_transformed = basic.transform(images)

# plt.imshow(images_transformed[12])
# plt.show()

#%%




















