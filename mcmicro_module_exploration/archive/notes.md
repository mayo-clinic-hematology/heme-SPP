# To reproduce Raymond's pipeline locally (or otherwise) you will need:

- Install python packages in convertCodexDir2Ometiff.py
  - tifffile, numpy, pandas, xarray



- Install singularity (tested on 3.5.3)
  - The singularity container must be built the first time from build_deepcell_singularity.sh which is currently commented out in the main pipeline file (run_pipeline_codex.sh). Make sure to uncomment it.
  - The most recent version of the container (latest) will not build in singularity version 3.5.3 so manually specify in the build file.
  
  ```
  singularity build initialdeepcell.sif docker://vanvalenlab/deepcell-applications:0.4.0
  ```
- Install Java (tested on openjdk 17.0.6 2023-01-17)
- Install QuPath (tested on 0.4.4)
    
    The groovy scripts are executed through QuPath and are therefore called with:
    ```
    QuPath script yourscript.groovy
    ```
  This means the path to calling QuPath on your local computer must be specificied in the main run_pipeline_codex.sh script


    We tested the current pipeline with dummy data, which did not play well with QuPath so running with real data would be ideal. all of these packages are likely available on mForge, but there could be unknown parameters we may need to troubleshoot. Otherwise the pipeline is currently reproducible in our hands.

