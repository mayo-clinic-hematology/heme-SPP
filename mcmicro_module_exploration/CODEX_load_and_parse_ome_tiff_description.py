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
import numpy as np

# XYResolution 377.4671052631579
# np.sqrt(377.4671052631579)

#%%
path_image = Path(r"C:\Users\m304399\Desktop\CODEX\common project\reg005.ome.tiff")
im = tifffile.imread(path_image)

#%% Access channel metadata stored in image description attribute
# https://github.com/cgohlke/tifffile/tree/v2020.6.3/#examples

tif = TiffFile(path_image)
page = tif.pages[0]
tags = list(page.tags)

list_description = [d for d in page.description.split("<") if "Channel ID" in d]

dict_channels = defaultdict(dict) 
for item in list_description:
    pass
    list_attributes = item.split(" ")
    # print(list_attributes)
    dict_key = list_attributes[2].replace("\"", "").replace("Name=","")
    
    # channel
    channel = list_attributes[1].replace("\"", "").replace("ID=Channel:","")
    channel = int(channel)
    dict_channels[dict_key]['channel'] = channel
    
    # fluor
    fluor = list_attributes[3].replace("\"", "").replace("Fluor=","")
    dict_channels[dict_key]["fluor"] = fluor

#%% PLOT SPECIFIC CHANNELS

list_channels_to_plot = ['CD45', 'CD3e', 'CD20']

for ch in list_channels_to_plot:
    plt.imshow(im[dict_channels[ch]['channel']], vmax=1000) 
    plt.show()




