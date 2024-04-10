#! /bin/bash

#SBATCH --partition=cpu-short
#SBATCH -J=logfilesname
#SBATCH -o hemespp-%J.log
#SBATCH --time=1:00:00
#SBATCH --mem=32G
#SBATCH --ntasks=8
#SBATCH --mail-type=ALL
#SBATCH --mail-user=howe.michael@mayo.edu
#SBATCH --chdir=/path/to/pipeline/heme-spp

module purge
module load apptainer

module load conda
eval "$(conda shell.bash hook)"
conda activate cdx_pipe_env


echo "Current working directory: ${PWD}"

./run_pipeline_codex.sh -i /path/to/input/directory \
    -o /path/to/output/directory
