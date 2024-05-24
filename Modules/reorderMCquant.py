import pandas as pd
import os, glob, argparse
from pathlib import Path

def reindex_csv(csv_paths):
    for data in csv_paths:
        # Exclude median files already generated
        fn = os.path.split(data)[1]
        if fn.find('median_') != -1:
            continue
 
        # Read in data
        df = pd.read_csv(data, float_precision="round_trip")

        # Collect column names 
        column_name_list = df.columns.values.tolist()

        # Create list of median and mean markers and leftover feature columns to reindex
        median_list = [i for i in column_name_list if "_intensity_median" in i]    
        mean_list =  [marker.split("_intensity_median")[0] for marker in median_list]
        props_list = [i for i in column_name_list if i not in mean_list and i not in median_list and i != column_name_list[0]]

        # Create list for reindexing
        swap_list = median_list + mean_list + props_list
        swap_list.insert(0, column_name_list[0])

        # Reindex csv file and export
        reindexed_df = df.reindex(columns=swap_list)
        path, filename = os.path.split(data)
        newfilename = 'median_' + filename
        reindexed_df.to_csv(os.path.join(path, newfilename), index=False, float_format='%.6f')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reorder MCQUANT output quantification csv files so that the median intensity is compatible with GATER')
    parser.add_argument('-i', '--indir', help='Directory containing MCMICRO output directories', nargs='?', type=str, dest="expDir", metavar="DIR",required=True)
    args = parser.parse_args()
    print(args)
    dir_path = Path(args.expDir)
    print(dir_path)
    # Get list of MCMICRO directories
    dir_to_convert = [folder for folder in dir_path.iterdir() if folder.is_dir()]

    for exp in dir_to_convert:
        # Grab paths to each CSV file
        quant = exp.joinpath('quantification')
        csv_paths = sorted(glob.glob(os.path.join(quant, "*.csv")))
        reindex_csv(csv_paths)



