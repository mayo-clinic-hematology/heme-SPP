#! /bin/bash
SECONDS=0


usage()
{
cat << EOF
###########################################################################
##	Generate OME.TIFF, QC Reports, QuPath Project & Quantification Files for Codex MxIF.
##
##	Script Options:
##	-i	<input>	 - (REQUIRED)  Input directory to Raw Codex Processor files.
##	-o	<output> - (REQUIRED)  Working directory, to output files from workflow.
##	-d	<DAPI>	 - (OPTIONAL)  Provide the Channel Index for DAPI [Default = 0]. 
##	-m	<MEMBR>	 - (OPTIONAL)  Provide the Channel Index for Membrane [Default = 11].
##	-t	<title>	 - (OPTIONAL)  Provide an optional name for Report title(s). NO SPACES!
##	-h			- Display Help 
##
###########################################################################
## Authors:             Raymond Moore
##For questions, comments, or concerns, contact 
##       Raymond (moore.raymond@mayo.edu)
EOF
}

### Pre determined Variables: Edit Once ###
TITLE="Codex_MxIF_Analysis"
WKFL=Modules/
QPATHFULL=/research/bsi/tools/biotools/qupath/0.4.3/bin/
DAPIIDX=0
MEMBRIDX=7



while getopts "i:o:d:m:t:h" OPTION; do
  case $OPTION in
	h) usage
		exit ;;
	i) INPUT=$OPTARG ;;
	o) OUTPUT=$OPTARG ;;
	d) DAPIIDX=$OPTARG ;;
	m) MEMBRIDX=$OPTARG ;;
	t) TITLE=$OPTARG ;;
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
	echo -e "\e[1;31mMust provide a input directory.\e[0m"
	usage
	exit 1;

else
	echo -e "\n Input directory:  ${INPUT}\n"
	echo -e "\n Output directory: ${OUTPUT}\n"
	echo -e "\n DAPI index:       ${DAPIIDX}\n"
	echo -e "\n Membrane index:   ${MEMBRIDX}\n"
	echo -e "\n#---------------------------------------------------"
    echo -e "\n#---------   Contents of input directory   ---------"
    echo -e "\n#---------------------------------------------------\n"

    reg_total=$(find "${INPUT}/stitched/" -mindepth 1 -type d | wc -l)
    reg_filesize=$(du -sh "${INPUT}/stitched" | cut -f1)

    echo -e "\t-> Number of regions: $reg_total"
    echo -e "\t-> Size of regions:   $reg_filesize"
    echo -e "\n#---------------------------------------------------\n"
fi

echo -e "\n"


echo -e "\n#---------------------------------------------------"
echo -e "\n#--------------   PIPELINE START:    ---------------"
echo -e "\n#---------------------------------------------------\n"



mkdir -p $OUTPUT/{OMETIFF,SEGMASKS,QUPATH,REPORTS}


echo "----------Step 1: Generating OME.TIFF's $(($SECONDS / 3600))h $(($SECONDS / 60))m $(($SECONDS % 60))s----------"

## Generating OME.TIFF files from stitched directory

python $WKFL/convertCodexDir2Ometiff.py -i $INPUT -o $OUTPUT/OMETIFF

## Segementation Setup: need to run just once.
# /bin/bash $WKFL/build_deepcell_singularity.sh

echo "----------Step 2: Segmenting OME.TIFF's $(($SECONDS / 3600))h $(($SECONDS / 60))m $(($SECONDS % 60))s----------"

## Segmenting each OME.TIFF file using mesmer

for ROIFH in $OUTPUT/OMETIFF/*.ome.tiff; do 
	echo $ROIFH;
 	$WKFL/run_deepcell_singularity.sh $OUTPUT $ROIFH $DAPIIDX $MEMBRIDX
done

echo "----------Step 3: Quantifying Marker Expression $(($SECONDS / 3600))h $(($SECONDS / 60))m $(($SECONDS % 60))s----------"

## Make QuPath project
$QPATHFULL/QuPath script $WKFL/createNewProject_Codex.groovy -a $OUTPUT 
## Generate quantification
PRGT=$(ls $OUTPUT/QUPATH/*.qpproj)
$QPATHFULL/QuPath script $WKFL/export_individual_qupath_rois.groovy -a $OUTPUT -p $PRGT

echo "----------End of Heme-Spatial Processing Pipeline $(($SECONDS / 3600))h $(($SECONDS / 60))m $(($SECONDS % 60))s----------"

## end Heme-Spatial Processing Pipeline