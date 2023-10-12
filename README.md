# Heme-Spatial Processing Pipeline
- A modified pipeline from Raymond Moore: https://github.com/VillasboasLab/MACodexPipeline
  
## Preparation:

- A conda environment containing the necessary packages. To create this environment: 
  - `module load conda`
  - `conda create -n cdx_pipe_env tifffile numpy pandas xarray`

- Build the deepcell singularity container that runs mesmer for segmentation. This should be done inside your pipeline directory `/path/to/heme-spp`. The container must be built prior to being submitted to the queue as compute nodes do not have internet access to pull the container:
  - module load apptainer
  - `/bin/bash Modules/build_deepcell_singularity.sh` (NOTE:DEPRECATED USAGE: Singularity is deprecated and has been replaced with Apptainer within the scripts)

- Next, the pipeline will need to be to run on a head node with a reduced dataset to pull and cache the MultiplexSegmentation model. We recommend using one small reg001 directory from a previous experiment and running until the model is downloaded. Set up the environment modules with `module load`:
```
module purge
module load apptainer
module load conda
eval "$(conda shell.bash hook)"
conda activate cdx_pipe_env

./run_pipeline_codex.sh -i [/path/to/smallinputfolder] -o [/path/to/outputfolder]
```
- End the run when downloaded and resubmit as a job to the queue using `submit_cdx_pipeline.sh`. It is ill-advised to run jobs on the head node, but is necessary for the reasons outlined above regarding compute node internet access.
- Pull processed codex data from Villaboas processing drive (CODEX Processed files) into your input directory folder using your preferred file transfer method. The file structure of the necessary data from a codex run should look as such:
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
- You will need all filles from the stitched folder and only the .log file from the diagnostics folder
## Usage
### Running the pipeline
To run the pipeline successfully there are two options.
1. Edit `submit_cdx_pipeline.sh` and submit to mFORGE queue
      - Line 11 and 12 must be edited with your email and path to pipeline directory
        - 11: `#SBATCH --mail-user=YOUREMAILHERE`
        - 12: `#SBATCH --chdir=/path/to/pipeline/heme-spp`
      - Line 27 must be changed to include paths to input and output directories (nuclearchannel and membranechannel are optional arguments and their defaults can be found in `run_pipeline_codex.sh`):
      ```
      ./run_pipeline_codex.sh -i [/path/to/inputfolder] -o [/path/to/outputfolder]> -d [nuclearchannel] -m [membrane channel(s)]
      ```
      
      - Submit to queue:
      ```
      sbatch submit_cdx_pipeline.sh
      ```
2. Allocate and enter an interactive environment on mFORGE using `srun` with sufficient compute resources:
      - `cd /path/to/pipeline/heme-spp`
      - Run the pipeline from the command line:
      ```
      ./run_pipeline_codex.sh -i [/path/to/inputfolder] -o [/path/to/outputfolder]> -d [nuclearchannel] -m [membrane channel(s)]
      ```
## Dependencies

- conda/4.7.12
  - cdx_pipe_env
- qupath/0.4.3
- apptainer/1.1.4
