# -*- coding: utf-8 -*-
"""
Created on Mon May  6 09:24:42 2024

@author: M304399
"""
# create new conda env with python=3.10
# conda install conda-forge::zeroc-ice
# pip install ezomero[tables]
# https://docs.openmicroscopy.org/omero/5.6.1/developers/PythonBlitzGateway.html

import tomli
from pprint import pprint

import ezomero 
from ezomero.rois import Point, Rectangle
import pandas as pd
from pathlib import Path

from natsort import natsorted

import omero

### Handy object to make annotations appear in native layer
NAMESPACE = omero.constants.metadata.NSCLIENTMAPANNOTATION

from random import sample
from tqdm import tqdm
# if __name__ == "__main__":
#     pass
#%% Load config and create connection object

with open("config.toml", mode="rb") as fp:
    config = tomli.load(fp)
    # pprint(config)

user = config['login']['user']
password = config['login']['password']

host = config['server']['url']
port = config['server']['port']
group = config['server']['group']
secure = config['server']['secure']

conn = ezomero.connect(user=user, 
                        password=password, 
                       host=host, 
                       port=port,
                       group=group,
                       secure=secure)

#%% load csv file and pick dataset



path_csv = Path(r"Y:\003 CODEX\MCMICRO\SMM_project\20230522_BR1010694BR1034362_Gonsalves_3_membrane\df_mcmicro_qupath_merged\df_mcmicro_qupath_roi001.csv") #TODO enter path to excel file

df = pd.read_csv(path_csv)

# different = df[df["CellID"] == df["mask_label"]]

#%% Create points and prepare rois 

# ezomero.get_roi_ids
# ezomero.get_shape
# ezomero.post_roi

#%% Populate points based on class
# https://thejacksonlaboratory.github.io/ezomero/ezomero.html#ezomero.rois.Point

image_id = 13750
    
try:
    for classification in df["Class"].unique():
        pass
        print(f"processing class: {classification}")
        shapes = list()
    
        df_subset = df[df["Class"] == classification]
    
        # generate point objects for each 
        for idx, row_data in tqdm(df_subset.iterrows()):
            pass
            point = Point(x=row_data['centroid_px_x'], 
                          y=row_data['centroid_px_y'],
                          label=f"{classification.lower()}: {row_data.mask_label}")
            shapes.append(point)
        
        ## take susbset of sample, otherwise it will be very slow on the OMERO side
        shapes = sample(shapes, len(shapes)//4)
        # put all points in same ROI
        ezomero.post_roi(conn, 
                          image_id, 
                          shapes, 
                          name=f"{classification}s",
                      # description='Very important'
                      )
finally:
    conn.close()

