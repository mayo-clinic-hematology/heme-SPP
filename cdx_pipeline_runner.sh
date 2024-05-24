#!/bin/bash

SECONDS=0


usage()
{
cat << EOF
################################################################################################
##	Generate OME.TIFF QuPath Project & Quantification Files for Codex MxIF.                   ##
##                                                                                            ##
##	Script Options:                                                                           ##
##	-i	<input>	 - (REQUIRED)  Input directory to Raw CODEXprocessor files in MCMICRO format. ##
##                                                                                            ##
################################################################################################
## Authors: Michael Howe and Emmanuel Contreras

EOF
}

while getopts "i:" OPTION; do
  case $OPTION in
	h) usage
		exit ;;
	i) INPUT=$OPTARG ;;

   \?) echo -e "\e[1;31mInvalid option: -$OPTARG.\e[0m"
       usage
       exit ;;
    :) echo -e "\e[1;31mOption -$OPTARG requires an argument.\e[0m"
       usage
       exit ;;
  esac
done


if [ ! -s "$INPUT" ]
then
	echo -e "\e[1;31mInput directory not provided, Aborting.\e[0m"
	usage
	exit 1;
fi

echo -e "\n"


echo -e "\n#---------------------------------------------------"
echo -e "\n#--------------   PIPELINE START:    ---------------"
echo -e "\n#---------------------------------------------------\n"


echo "----------Step 1: Prep tiles for running ASHLAR $(($SECONDS / 3600))h $(($SECONDS / 60))m $(($SECONDS % 60))s----------"

python Modules/prep_tiles_for_ashlar.py -i $INPUT

echo "----------Step 2: Run MCMICRO $(($SECONDS / 3600))h $(($SECONDS / 60))m $(($SECONDS % 60))s----------"

sbatch submit_hemespp.sh