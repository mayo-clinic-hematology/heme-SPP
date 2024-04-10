# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 15:03:18 2023

@author: M304399
"""

from pathlib import Path

import tifffile
import numpy as np


def squeeze_and_save_mask(path_input : Path, suffix:str="_squeezed", overwrite:bool=False):
    """
    Helper function to remove empty dimensions in mask arrays coming out of the CODEX pipeline.

    Parameters
    ----------
    path_input : Path
        path to the input image.
    suffix : TYPE, optional
        Name suffix to add to the filename to differentiate from the 
        original mask. The default is "squeezed".

    Returns
    -------
    None.

    """
    mask = tifffile.imread(path_input).squeeze()
    path_output = path_input.parent / f"{path_file.stem}_{suffix}.tiff"
    
    # save mask
    if path_output.exists():
        if overwrite:
            # save image
            tifffile.imwrite(path_output, mask)
        else:
            print(f"Error: File already esists, skipping saving. Optinally use overwrite flag: \n{path_output}")
    else: # no current file, save it
        # save image
        tifffile.imwrite(path_output, mask)

if __name__ == "__main__":
    pass

    path_file = Path(r"C:\Users\m304399\Desktop\reg005_WholeCellMask.tiff")
    squeeze_and_save_mask(path_file, suffix="test", overwrite=True)
