#!/usr/local/bin/python3

# Python script to create a frequency list of single words from a directory of .txt files

# CHANGE THE SHEBANG LINE ABOVE AS NEEDED

# SPECIFY THE DIRECTORY WITH THE .TXT FILES
input_directory = "/pathway/to/directory"
input_directory = "/Users/ekb5/Corpora/USA/California/Salinas/transcripts"

# SPECIFY A REGEX WITH NON-WORD CHARACTERS TO BREAK UP WORDS
non_wd_char = "[^A-ZÁÉÍÓÚÜÑ]+"

# SPECIFY A .CSV FILE THAT THE FREQUENCY LIST SHOULD BE SAVED TO
output_csv_file = "/Users/ekb5/Downloads/deleteme.csv"

# NOW, SAVE THE FILE AND MAKE IT EXECUTABLE (in a terminal window: "chmod +x freq_list.py") AND RUN IT (in a terminal window: "./freq_list.py")

import os
import re
import csv
import collections

os.chdir(input_directory)
file_names = [f for f in os.listdir(input_directory) if re.search("\.txt$", f, re.IGNORECASE)]

d = collections.defaultdict(int)
for i in file_names:
    with open(i) as f:
        cur_lines = f.read().upper().splitlines()
        f.close()
        cur_words = [re.split(non_wd_char, x) for x in cur_lines]
        cur_words = [item for sublist in cur_words for item in sublist]
        for j in cur_words:
            if j == '':
                continue
            d[j] += 1

od = collections.OrderedDict(sorted(d.items()))

writer = csv.writer(open(output_csv_file, 'w+'))
for key, value in od.items():
    writer.writerow([key, value])
