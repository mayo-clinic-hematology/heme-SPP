#!/bin/bash

# this script should be run inside the ashlar folder which contains two folders
# ashlar_input and ashlar_output
# the ashlar input has the regions in folders as reg001/t001
# the struture of the ashlar_input folder is generated by the python script  that 
# copies and renames the files so that they appear to come from the same cycle


for folder in $(ls -d */) #| head -n 1
do
	working_dir="${folder}ashlar/"
	echo "Processing: ${working_dir}"
	for reg in $(ls "${working_dir}/ashlar_inputs")
	do
		file_path="${working_dir}ashlar_outputs/${reg}.ome.tiff"
		echo ${file_path}

		if ! [ -f ${file_path} ]; then

		    echo ${reg}
		    docker run \
		    -v "./${working_dir}ashlar_inputs":/input \
		    -v "./${working_dir}ashlar_outputs":/output \
		    -it labsyspharm/ashlar:1.18.0b3 ashlar \
		    --maximum-shift 0 \
		    "filepattern|/input/${reg}/t001|pattern=${reg}_X{col:02}_Y{row:02}_t001_z001_c{channel}.tif|overlap=0.0|pixel_size=0.377454" \
		    -o /output/${reg}.ome.tiff
		else
			echo "${reg}.ome.tiff already exists"
		fi
	done
done
