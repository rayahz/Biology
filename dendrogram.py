#!/usr/bin/python
# coding=utf-8

##  AUTHOR : Rayhana ZIARA
##  LANGUAGE USED : python

import json
from os.path import exists
import subprocess

filename_name     = "./path/files_names.json"
filename_distance = "./path/distances_matrix.json"
filename_tree     = "./path/tree.phb"

# Is njplot installed ?
if cache['njplot'].is_installed == False:
	print "Please install njplot to continue"
	sys.exit(0)

# Does the file exists ?
if not exists(filename_distance):
  exit("The file " + filename_distance + " does not exists\nPlease check the path and/or the filename")

# Does the file exists ?
if not exists(filename_name):
  exit("The file " + filename_name + " does not exists\nPlease check the path and/or the filename")

# Load of the matrix distance
file_json = open(filename_distance, "r")
distances = json.load(file_json)
file_json.close()

# Load of the files names
file_json = open(filename_name, "r")
files = json.load(file_json)
file_json.close()

print("Dendrogram")
# Array of leaves. Array size is the number of files
leaves = [[files[i][1], 0.] for i in range(len(files))]

tmp_size = len(distances)

while tmp_size > 1:
  # Looking for the minimum value in the array
  dist_min = [distances[0][1], 0, 1]
  for i in range(tmp_size - 1):
    for j in range(i + 1, tmp_size):
      if distances[i][j] < dist_min[0]:
        dist_min = [distances[i][j], i, j]
  # Partial tree
  leaves[dist_min[1]][0] = "(" + leaves[dist_min[1]][0] + ":" + str(dist_min[0] - leaves[dist_min[1]][1]) + "," + leaves[dist_min[2]][0] + ":" + str(dist_min[0] - leaves[dist_min[2]][1]) + ")"
  leaves[dist_min[1]][1] = dist_min[0]

  # Fusion of 2 columns / rows. Only the colum / row with the minimal value is kept
  for i in range(tmp_size):
    distances[i][dist_min[1]] = min(distances[i][dist_min[1]], distances[i][dist_min[2]])
    distances[dist_min[1]][i] = distances[i][dist_min[1]]

  # Updating the size array
  tmp_size -= 1

  # Removing the other row / column
  del distances[dist_min[2]]
  for i in range(tmp_size):
    del distances[i][dist_min[2]]
  del leaves[dist_min[2]]

# Final tree
leaves[0][0] += ";"
print(leaves[0][0])

# Writing final tree in file
file_phb = open(filename_tree, "w")
file_phb.write(leaves[0][0])
file_phb.close()

# Calling njplot (output format is ps)
subprocess.call(["njplot", "-psonly", "-boot", "-lengths", "-pc", "1", "-us", "-notitle", filename_tree])
