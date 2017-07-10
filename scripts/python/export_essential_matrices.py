# COLMAP - Structure-from-Motion and Multi-View Stereo.
# Copyright (C) 2017  Johannes L. Schoenberger <jsch at inf.ethz.ch>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This script exports inlier matches from a COLMAP database to a text file.

import os
import argparse
import sqlite3
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--database_path", required=True)
    parser.add_argument("--output_path", required=True)
    parser.add_argument("--min_num_matches", type=int, default=15)
    args = parser.parse_args()
    return args


def pair_id_to_image_ids(pair_id):
    image_id2 = pair_id % 2147483647
    image_id1 = (pair_id - image_id2) / 2147483647
    return image_id1, image_id2


def main():
    args = parse_args()

    connection = sqlite3.connect(args.database_path)
    cursor = connection.cursor()

    images = {}
    cursor.execute("SELECT image_id, camera_id, name FROM images;")
    for row in cursor:
        image_id = row[0]
        image_name = row[2]
        images[image_id] = image_name

    with open(os.path.join(args.output_path), "w") as fid:
        cursor.execute("SELECT pair_id, ematrix FROM inlier_matches WHERE rows>=?;",
                       (args.min_num_matches,))
        for row in cursor:
            pair_id = row[0]
            ematrix = np.fromstring(row[1],
                                           dtype=np.double).reshape(3, 3)
            image_id1, image_id2 = pair_id_to_image_ids(pair_id)
            image_name1 = images[image_id1]
            image_name2 = images[image_id2]
            fid.write("%s %s\n" % (image_name1, image_name2))
            for line in ematrix:
                fid.write("%.6e %.6e %.6e\n" %(line[0], line[1], line[2]))
            fid.write("\n")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()
