import tifffile

import matplotlib.pylab as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300

import numpy as np

channelDesign = {'ch001':'DAPI','ch002':'AF750','ch003':'Atto550','ch004':'Cy5'}

im_width = 300
im_height = 300
n_channels = 1



## generate tiffs 

for idx, (key, value) in enumerate(channelDesign.items()):
    stack = np.zeros((n_channels,im_width, im_height))
    
    stack[0,...] = np.random.random((im_width, im_height))
    tifffile.imwrite(f"./reg_{idx}_{key}_{value}_Barcode_.tif", stack)
    # "Sample","Cycle","Channel","Marker"

# tifffile.imwrite(f"./reg_stack_{im_width}x{im_height}_channels_{n_channels}.tiff", stack)


#%%

from skimage.data import binary_blobs
from skimage.morphology import label

import numpy as np

blobs = binary_blobs(length=512, blob_size_fraction=0.05, volume_fraction=0.2)

mask_blobs = label(blobs)
plt.imshow(mask_blobs)
plt.show()

plt.imshow(blobs)
plt.show()
