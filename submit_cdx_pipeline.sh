#! /bin/bash

#SBATCH --partition=cpu-short
#SBATCH -J=heme-spptest1
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

cd /research/labs/hematology/hemedata/m302618/projects/spatial/heme-SPP
echo $PWD

./run_pipeline_codex.sh -i /research/labs/hematology/hemedata/m302618/projects/spatial/cdx_pipeline_mforge/cdx_test_kankeu \
    -o /research/labs/hematology/hemedata/m302618/projects/spatial/cdx_pipeline_mforge/cdx_test_kankeu_out
