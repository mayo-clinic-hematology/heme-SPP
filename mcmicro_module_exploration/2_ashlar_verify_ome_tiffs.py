# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 08:12:37 2024

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
#%% script to compare akoya and ashlar outputs to make sure they are identical

# path_akoya_tiffs = Path(r"Z:\CODEX Processed files\20230522_BR1010694BR1034362_Gonsalves\processed_2023-06-12\stitched")
# path_ashlar = Path(r"M:\Projects\SMM\20230522_BR1010694BR1034362_Gonsalves\ashlar\ashlar_outputs")

path_akoya_tiffs = Path(r"Z:\CODEX Processed files\20230817_BR093223_Gonsalves\processed_2023-08-27\stitched")
path_ashlar = Path(r"M:\Projects\SMM\20230817_BR093223_Gonsalves") / "ashlar/ashlar_outputs"

# load akoya tiff stack
id_sample = path_akoya_tiffs.parent.parent.name
list_akoya_tiffs = natsorted(list(path_akoya_tiffs.rglob(f"*{id_sample}_reg*")))

# load ashlar tiff stack
list_ashlar_tiffs = natsorted(list(path_ashlar.glob("*.tiff")))

for path_im_akoya, path_im_ashlar in list(zip(list_akoya_tiffs, list_ashlar_tiffs))[:]:
    pass

    # make sure same regions are compared
    handle = path_im_ashlar.stem.split(".")[0]
    assert handle in str(path_im_akoya), "Error: mismatchd regions being compared."
    
    # load and rearrange akoya tiffs 
    print(f"Reading akoya tiff: {path_im_akoya.name}")
    im_akoya = tifffile.imread(path_im_akoya)
    print("Finished reading akoya tiff")    
    cycle, channel, x , y = im_akoya.shape

    # load ashlar tiff
    print(f"Reading ashlar tiff: {path_im_ashlar.name}")
    im_ashlar = tifffile.imread(path_im_ashlar)
    print("Finished reading ashlar tiff")
    
    for ch in range(len(im_ashlar)):
        pass
        
        # compute channel and cycle indices in array to match
        # ashlars
        akoya_cycle = ch // 4
        akoya_channel = ch % 4 
        
        im_akoya_channel = im_akoya[akoya_cycle, akoya_channel,...]
        im_difference =  im_akoya_channel - im_ashlar[ch,...]
        sum_pixels = np.sum(abs(im_difference), axis=(0,1))
        
        if sum_pixels == 0:
            print(f"{handle} : channel {ch} | akoya and ashlar images are identical.")
        
        else:
            
            fig, ax = plt.subplots(1,3,figsize=(10,5))
            
            vmax = 5000
            
            fig.suptitle(f"{handle} : channel {ch} | sum difference pixels= {sum_pixels}")
            ax[0].set_title("akoya")
            ax[0].imshow(im_akoya_channel, vmax=vmax)
            ax[0].set_axis_off()
            
            ax[1].set_title("ashlar")
            ax[1].imshow(im_ashlar[ch,...], vmax=vmax)
            ax[1].set_axis_off()
            
            ax[2].set_title("difference")
            ax[2].imshow(im_difference, vmax=vmax)
            ax[2].set_axis_off()
            plt.show()
            
            
        