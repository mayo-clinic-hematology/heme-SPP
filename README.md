# To reproduce the Heme DS version of Raymond's pipeline on mFORGE you will need:

- A conda environment containing tifffile, numpy, pandas, xarray. To create this environment:
  - module load conda
  - conda create -n cdx_pipe_env tifffile numpy pandas xarray
  - 

- Build the deepcell singularity container. This can in theory be done by uncommenting line ~65 of build_deepcell_singularity.sh in Raymonds original pipeline and running on a dataset of interest, but it must be built prior to being submitted to the queue as compute nodes do not have internet access and cannot build the container. To build prior to submitting as a job to the queue run:
  - module load apptainer
  - /bin/bash Modules/build_deepcell_singularity.sh
  - 
