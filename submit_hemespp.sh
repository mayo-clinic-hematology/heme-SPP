#!/bin/sh

#SBATCH --partition=cpu-short
#SBATCH -J=mcmicro_SMM_multisample
#SBATCH -o=mcmicro-%J.log
#SBATCH --time=2:00:00
#SBATCH --mem=4G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=howe.michael@mayo.edu
#SBATCH --chdir /research/labs/hematology/hemedata/m302618/projects/spatial/cdx_pipeline_mforge/MCMICRO/

module purge
module load nextflow
module load apptainer

export NXF_APPTAINER_CACHEDIR="/research/labs/hematology/hemedata/m302618/apptainer/containers"

nextflow -C mforge_settings.config run labsyspharm/mcmicro --in 20240112_BR062124_Gonsalves_CD45 -with-report