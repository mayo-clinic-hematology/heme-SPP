# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 10:35:20 2024

@author: M304399
"""


#%% load pyramidal ome.tiffs with Napari
# https://forum.image.sc/t/wholeslide-ome-tiff-in-napari-from-ipython/52872/5

# import tifffile
# import zarr
# import napari

# # filename = 'HSM0170-20x20.ome.tiff'  # 163 GB compressed

# filename= path_ashlar

# store = tifffile.imread(filename, aszarr=True)
# zgroup = zarr.open(store, mode='r')
# print(zgroup.info)
# print(zgroup[0].info)
# data = [ 
#     zgroup[int(dataset['path'])]
#     for dataset in zgroup.attrs['multiscales'][0]['datasets']
# ]
# viewer = napari.view_image(data, rgb=False) # contrast_limits=[0, 255]
# napari.run()
# store.close()



#%% calling docker through python  to launch ashlar 

#!/usr/bin/python
# import subprocess

# with open("/tmp/output.log", "a") as output:
#     subprocess.call("docker run --rm wappalyzer/cli https://wappalyzer.com", shell=True, stdout=output, stderr=output)



#%%



import numpy as np








