# CODEX Pipeline

---

Pipeline order: 
1. BaSiC --> illumination correction (found to be optional with CODEX images)
2. Ashlar --> stitching
3. Segmentation(mesmer/cellpose)
4. RedseaPy - (spillover compensation and quantification)
5. MCQuant - quantification
6. CyLinter - quality control
7. SCIMAP --> phenotyping and neighborhood analysis

---

### How To Run

1. BaSicPy - Windows side python interpreter
    Script points to the shared drive where the original tiles are located, it then creates and saves the corrected tiles in a folder called _illumination_corrected_ images
	run on shared drive
    Copy this output into the local folder (not WSL) ashlar_input folder as _reg005_
    
    > Note: The output of BaSicPy is float32 and has negative numbers this will make your image size much larger and ashlar will not like negative numbers. You can take the absolute value and convert to int16 before feeding into ashlar

---

2. ashlar - WSL2/Docker 

    Use the ashlar script that renames all tiles into a single cycle then run ashlar through docker as if it was all run on a single cycle. It works better this way because otherwise ashlar introduces a 1px blank tile separation on some cycles. 
    
    Once the tile filenames have the correct cycle (t001) and channel (ch###) run the command in WSL at the root of the _ashlar_ working directory. Ashlar outputs a pyramidal ome.tiff 

   There is an accompanying shell script that can be used to stitch up each of the regions in a folder after the ashlar.py script has been run. 


``` bash
docker run \
-v './ashlar_inputs':/input \
-v "./ashlar_outputs":/output \
-it labsyspharm/ashlar:1.18.0b3 ashlar \
--maximum-shift 0 \
"filepattern|/input/reg005/t001|pattern=reg005_X{col:02}_Y{row:02}_t001_z001_c{channel}.tif|overlap=0.0|pixel_size=0.377454" \
-o /output/reg005_one_cycle.ome.tiff

```

Other optional arguments

```
--output-channels 0
--pyramid
--filter-sigma 0 \
--align-channel 0
-v '/ashlar':/illumination \
--ffp '/illumination/GB38_OT-ffp.tif' \
--dfp '/illumination/GB38_OT-dfp.tif'
```




---

1. Segmentation -- Cellpose 

---

2. MCQuant --> Run on WSL2 

    * Grab the channel_names.txt file from the CODEX output folder
    * Grab the paths to the mask(s), image and point to the output folders
    * Add in your additional features 

    ```bash
    python \CommandSingleCellExtraction.py --masks "../../ashlar/mask/dapi_cp_masks.tif" \
    --image "../../ashlar/ashlar_outputs/reg005.ome.tiff" \
    --output "../output" --channel_names "../channelNames.txt" \
    --intensity_props gini_index intensity_median intensity_sum
    ```

--- 

3.5. redseapy --> Run locally on windows side, can also be run on docker

* This package does spillover compensation given a mask and an ome.tiff stack. It then returns a before and after CSV files quantifying intensity counts per roi  

Inputs
  * ome.tiff
  * mask
  * channelNames.txt <-- CODEX name of channels

Run through docker
``` bash 
docker run -v "$PWD":/data --rm labsyspharm/redsea:0.1 redsea  \
data/ashlar/ashlar_outputs/reg005.ome.tiff \
data/segmentation/mask/dapi_cp_masks.tif \
data/mcquant/channelNames.txt \
data/redseapy/output
```
Local --> change directory into CODEX root folder
``` bash
redsea ".\ashlar\ashlar_outputs\reg005.ome.tiff" \
  ".\segmentation\mask\dapi_cp_masks.tif" \
  ".\mcquant\channelNames.txt" \
  ".\redseapy\output"
```

---

5. CyLinter (Optional) - Run on windows anaconda prompt environment
   * GUI based, so install it on the windows side not WSL side
   * Optional --> SCIMAP has a lot of the same features for quality control, skipping exploring for now

---

6. SCIMAP --> Run on windows side through anaconda prompt
   *  Phenotyping of cells and neighborhood analysis. Also does some quality control
   * Run through python script. 
