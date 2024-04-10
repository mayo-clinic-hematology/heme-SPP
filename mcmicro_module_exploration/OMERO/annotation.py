# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 10:20:18 2024

@author: M304399
"""
# create new conda env with python=3.10
# conda install conda-forge::zeroc-ice
# pip install ezomero[tables]
# https://docs.openmicroscopy.org/omero/5.6.1/developers/PythonBlitzGateway.html

import tomli
from pprint import pprint

import ezomero 
import pandas as pd
from pathlib import Path

from natsort import natsorted

import omero

### Handy object to make annotations appear in native layer
NAMESPACE = omero.constants.metadata.NSCLIENTMAPANNOTATION

# if __name__ == "__main__":
#     pass

#%% LOAD EXCEL file and pick dataset

path_excel = Path(r"Metadata for FL Transformation project - TMA LYM534A.xlsx") #TODO enter path to excel file

df = pd.read_excel(path_excel)
df = df.sort_values(by="OMERO Image name")

# Follicular Transformation 
# 20231208_LYM534A_Villasboas
id_dataset = 1441 # TODO enter id of dataset 

#%%

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

try:
       
    ### Image ID's 
    list_image_ids = natsorted(ezomero.get_image_ids(conn, dataset=id_dataset))

    list_image_names = df["OMERO Image name"].values
    
    # Error checking for matching ID's and spreadsheet
    # assert len(list_image_ids) == len(list_image_names), "Error: number of ID's in OMERO does not match number of rows in excel sheet."
    
    # iterate through each image
    for name_image in list_image_names[:3]:
        pass
    
        print("="*50)
        # name_image = df.iloc[0,:]["OMERO Image name"]
        id_image = ezomero.filter_by_filename(conn, im_ids=list_image_ids, imported_filename=name_image)[0]
        
        # store image ID in df
        df.loc[df["OMERO Image name"] == name_image, ['OMERO Image ID']] = int(id_image)
        print(f"{name_image} : ID: {id_image}")
        
        ## GET CURRENT MAP ANNOTATIONS 
        map_ann_ids = ezomero.get_map_annotation_ids(conn, 'Image', int(id_image))
        print(f"Number of map annotations: {len(map_ann_ids)}")
        
        
        # remove hard coded map annotations added during testing
        list_ann_ids_to_remove = [4327, 4329, 4325]
        map_ann_ids = [v for v in map_ann_ids if v not in list_ann_ids_to_remove]

            
        assert len(map_ann_ids) < 2, "Error more than 1 Map Annotation for this image."
        
        # grab row with data based on filename
        dict_row = df.loc[df["OMERO Image name"] == name_image].to_dict(orient='records')
        assert len(dict_row) != 0, "Error no image entry found in excel sheet."
        assert len(dict_row) == 1, "Error multiple entries for this image found in excel sheet ."
        
        dict_row = dict_row[0]
        
        ## convert all entries to strings for comparing with omero dictionary
        dict_row = {str(k): str(v) for k,v in dict_row.items()}
        
        # No map annotations, post one to image
        if len(map_ann_ids) == 0: 
            print("No annotations found, posting new annotations object.")
            
            # post initial dict
            dict_omero = dict_row
            
            # PUT MAP ANNOTATIONS
            ezomero.post_map_annotation(conn, 
                                        object_type="Image",
                                        object_id= id_image, 
                                        kv_dict=dict_omero,
                                        ns=NAMESPACE)
        ## Image has map annotations, update it
        elif len(map_ann_ids) == 1:
            print("Annotations found, updating annotations dictionary.")
            # get first ID
            map_ann_id = map_ann_ids[0]
            dict_omero = ezomero.get_map_annotation(conn, map_ann_id)
            
            if "Clinic #" in list(dict_omero.keys()):
                del dict_omero['Clinic #']
            
            if "Clinic #" in list(dict_row.keys()):
                del dict_omero['Clinic #']
            
            # update dict annotation only if it's different
            if dict_row != dict_omero:
                dict_omero.update(dict_row)
                
                if "Clinic #" in list(dict_omero.keys()):
                    del dict_omero['Clinic #']
                
                # put map annotations
                ezomero.put_map_annotation(conn, 
                                            map_ann_id= map_ann_id, 
                                            kv_dict=dict_omero,
                                            ns=NAMESPACE)
            else:
                print("Skip updating: map annotations object the same as excel sheet.")

finally:
    
    conn.close()


