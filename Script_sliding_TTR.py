"""Python function to calculate a sliding type-to-token ratio.
Earl Kjar Brown, ekbrown byu edu (add appropriate characters to create email)
Note: Assumes the word_tokenize() function in NLTK is available.
"""

import re
from nltk import word_tokenize
from statistics import mean
from time import time

def get_ttr(wds):
    """Helper function to get type-to-token ratio of list of words.
    """
    return len(set(wds)) / len(wds)

def get_sliding_ttr(pathway, span):
    """Given a string with the pathway to TXT file, returns a sliding TTR score.
    param pathway: str, pathway to TXT file (assumes UTF-8 character encoding);
    param span: int, the width of the window in words;
    return value: float, the sliding TTR score; if 'span' is larger than the number of words in the TXT file, returns -1.
    """

    with open(pathway, encoding = "utf8") as infile:
        wds = word_tokenize(infile.read())
    wds = [w for w in wds if re.search(r"[-'\w]", w)]

    if len(wds) < span:
        return -1
    else:
        start, end = 0, span - 1
        ttrs = []
        while end <= len(wds):
            ttrs.append(get_ttr(wds[start:end]))
            start += 1
            end += 1
        return mean(ttrs)

### TEST THE FUNCTION ###
start = time()
print(get_sliding_ttr("/Users/ekb5/Downloads/War_Peace.txt", 1000))
print(time() - start)
