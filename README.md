# Heme-Spatial Processing Pipeline
- A modified pipeline from Raymond Moore: https://github.com/VillasboasLab/MyCodexPipeline
  
## Preparation:

- A conda environment containing the necessary packages. To create this environment: 
  - `module load conda`
  - `conda create -n cdx_pipe_env tifffile numpy pandas xarray`

- Build the deepcell singularity container that runs mesmer for segmentation. This should be done inside your pipeline directory `/path/to/heme-spp`. The container must be built prior to being submitted to the queue as compute nodes do not have internet access to pull the container:
  - `module load apptainer`
  - `/bin/bash Modules/build_deepcell_singularity.sh` (NOTE:DEPRECATED USAGE: Singularity is deprecated and has been replaced with Apptainer within the scripts)


- Next, the pipeline will need to be to run on a head node with a reduced dataset to pull and cache the MultiplexSegmentation model. Pull a reduced processed codex experiment from the Villaboas processing drive (CODEX Processed files) into your input directory folder using your preferred file transfer method. We recommend using one small reg001 directory from a previous experiment and running until the model is downloaded. You will need all filles from the stitched folder and only the .log file from the diagnostics folder. The file structure of the necessary data from a codex run should look as such (This file structure and data should be the same for full runs as well):
```bash
├── inputfolder
│   ├── stitched
│   │    ├── reg***
│   │        ├──reg_cyc_ch_marker.tif
│   │        ├──**_**_experiment_reg
│   │
│   ├── diagnostics
│   │    ├──*.log
```
- Set up the environment modules with `module load` and run the pipeline on the reduced dataset:

```
module purge
module load apptainer
module load conda
eval "$(conda shell.bash hook)"
conda activate cdx_pipe_env

./run_pipeline_codex.sh -i [/path/to/smallinputfolder] -o [/path/to/outputfolder]
```
- End the run when the model is downloaded and resubmit as a job to the queue using `submit_cdx_pipeline.sh`. It is ill-advised to run jobs on the head node, but is necessary for the reasons outlined above regarding compute node internet access.

## Usage
### Running the pipeline
To run the pipeline successfully there are two options.
1. Edit `submit_cdx_pipeline.sh` and submit to mFORGE queue
      - Line 10 and 11 must be edited with your email and path to pipeline directory
        - 10: `#SBATCH --mail-user=YOUREMAILHERE`
        - 11: `#SBATCH --chdir=/path/to/pipeline/heme-spp`
      - Line 23 must be changed to include paths to input and output directories (nuclearchannel and membranechannel are optional arguments and their defaults can be found in `run_pipeline_codex.sh`):
      ```
      ./run_pipeline_codex.sh -i [/path/to/inputfolder] -o [/path/to/outputfolder]> -d [nuclearchannel] -m [membrane channel(s)]
      ```
      
      - Submit to queue:
      ```
      sbatch submit_cdx_pipeline.sh
      ```
2. Allocate and enter an interactive environment on mFORGE using `srun` with sufficient compute resources:
      - `cd /path/to/pipeline/heme-spp`
      - Setup environment modules as done previously
      - Run the pipeline from the command line:
      ```
      ./run_pipeline_codex.sh -i [/path/to/inputfolder] -o [/path/to/outputfolder] -d [nuclearchannel] -m [membrane channel(s)]
      ```
## Dependencies

- conda/4.7.12
  - cdx_pipe_env
- qupath/0.4.3
- apptainer/1.1.4






