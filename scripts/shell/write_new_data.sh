#!/bin/sh

dbfile=$(find *.db -print)

python export_raw_matches.py --image_path=./images --output_path=./images --database_path=$dbfile
python export_inlier_matches.py --image_path=./images --output_path=./images --database_path=$dbfile
python export_essential_matrices.py --output_path=./essential_matrices.txt --database_path=$dbfile


