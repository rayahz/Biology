#!/usr/bin/python
# coding=utf-8

##  AUTHOR : Rayhana ZIARA
##  LANGUAGE USED : python

from Bio import SeqIO
import os.path
import glob
import re
import math
import subprocess
from os.path import exists

strand          = ""
translation     = ""
cpt             = 0
filename_input  = "./path/filename.gbk"
filename_output = "./path/filename.faa"

# Does the file exists ?
if not exists(filename_input):
  exit("The file " + filename_input + " does not exists\nPlease check the path and/or the filename")

# Opening file to write 
output_handle = open(filename_output, "w")

print("Conversion from GenBank file to FASTA file")

# Reading the data needed from the GenBank file
for k in range(0, 2):
  for sequence in SeqIO.parse(filename_input, "genbank"):
    for feature in sequence.features:
      if feature.type == "CDS":
        start        = feature.location.start
        end          = feature.location.end
        transl_table = feature.qualifiers["transl_table"][0]

        if feature.location.strand == 1:
          strand      = "direct"
          translation = sequence.seq[start:end].translate(table = transl_table)
        else:
          strand      = "complement"
          translation = sequence.seq[start:end].reverse_complement().translate(table = transl_table)

        string  = ">gi|"
        string += re.sub("GI:", "", feature.qualifiers.get('db_xref')[0]) + "|"
        string += "unknown_cds_" + str(cpt) + "  "
        string += feature.qualifiers["product"][0] + "|"
        string += str(start + 1) + "|"
        string += str(end) + "|" + strand 

        for i in range(0, len(translation)):
          if i%60 == 0 and translation[i] != "*":
            string += "\n" + translation[i]
          elif translation[i] != "*":
            string += translation[i]

        output_handle.write(string + "\n")
        cpt += 1
output_handle.close()

print("The file " + filename_input + " has been converted to " + filename_output) 
