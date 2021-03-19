"""
Python script to get keywords in a target corpus
Earl K. Brown, ekbrown byu edu (add appropriate characters to create email)
based on code written by Adam Davies
"""

from math import log2
from collections import defaultdict
import os, re, time, pandas as pd

start = time.time()

def get_num_wds_freqs(pathway):
    """Helper function to retrieve the number of words and the frequencies of those words in a directory"""
    os.chdir(pathway)
    files = [file for file in os.listdir() if re.search(r"\.txt", file, flags=re.I)]
    freqs = defaultdict(int)
    num_wds = 0
    for file in files:
        with open(file) as infile:
            whole_file_as_str = infile.read()
            wds = re.split(r"[^-'a-záéíóúüñ]+", whole_file_as_str, flags=re.I)
            wds = [wd.upper() for wd in wds if len(wd) > 0]
            num_wds += len(wds)
            for wd in wds:
                freqs[wd] += 1
    print("There are " + "{:,}".format(num_wds) + f" words in {pathway}")
    return (num_wds, freqs)

def get_keywords(target_dir, ref_dir, num_keywords, min_freq):
    """Get keywords in .txt files within a target directory, comparing them with words in .txt files within a reference directory.
    param: target_dir - the directory with the target corpus in .txt files
    param: ref_dir - the directory with the reference corpus in .txt files
    param: num_keywords - number of keywords desired
    param: min_freq - the minimum frequency of keywords in the target corpus
    return value: a pandas DataFrame with three columns: (1) keyword, (2) frequency in target corpus, (3) keyness score
    """

    # get number of words and freqs in target and reference directories
    target_num_wds, target_freqs = get_num_wds_freqs(target_dir)
    ref_num_wds, ref_freqs = get_num_wds_freqs(ref_dir)

    # calculate frequency ratio between target corpus and reference corpus
    rel_freq = target_num_wds / ref_num_wds

    # calculate keyness
    keywords = {}
    for wd in sorted(target_freqs, key = lambda x:target_freqs[x], reverse = True):
        if target_freqs[wd] >= min_freq:
            if wd in ref_freqs:
                keywords[wd] = log2((target_freqs[wd] * rel_freq) / ref_freqs[wd])

    # sort keywords and limit to number desired by user
    top_keywords = [kw for kw in sorted(keywords, key = lambda x:keywords[x], reverse = True)][:num_keywords]

    # push keywords to pandas DataFrame
    df = pd.DataFrame(columns = ["keyword", "freq", "keyness"])
    for kw in top_keywords:
        df = df.append({'keyword': kw, "freq": target_freqs[kw], "keyness": "{:.4}".format(keywords[kw])}, ignore_index=True)

    return df


### test the function
target_dir = "/Users/ekb5/Documents/LING_580R/gen_conf/"
ref_dir = "/Users/ekb5/Corpora/Brown/"
num_keywords = 10
min_freq = 3

print(get_keywords(target_dir, ref_dir, num_keywords, min_freq))

print(f"{round(time.time() - start, 2)} seconds")
