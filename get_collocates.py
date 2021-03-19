"""Python script to get collocates of a node word in a directory of TXT files.
Earl K. Brown, ekbrown byu edu (add appropriate characters to create email)
"""

import os, re, time, pandas as pd

start = time.time()

def find_collocates(dir_with_txt, node_wd, stopwords = [], span = 4, side = "both", min_freq = 2):
    """Get the collocates (neighboring words) of a node word.
    dir_with_txt: Pathway to directory with TXT files; other file types are ignored.
    node_wd: Node word whose collocates will be found.
    stopwords: A Python list of stopwords to exclude as possible collocates (default is empty list).
    span: The span in number of words around the node word to look for collocates (default is 4).
    side: Which side, or both, of the node word to look for collocates,
        from among "both", "left", "right" (default is "both").
    min_freq: Minimum frequency that a word must have to be considered a collocate (default is 2).
    return value: A Pandas DataFrame.
    """

    ### verify arguments given by user
    if span <= 0 or not isinstance(span, int):
        raise Exception("In the call to find_collocates(), you need to supply a positive integer to the argument 'span'.")

    if side.lower() == "both":
        span_to_search = range(-span,span + 1)
    elif side.lower() == "left":
        span_to_search = range(-span, 0)
    elif side.lower() == "right":
        span_to_search = range(0, span + 1)
    else:
        raise Exception("In the call to find_collocates(), you need to specify 'side' as either 'left', 'right', or 'both'.")

    # make stopwords uppercase
    stopwords = [i.upper() for i in stopwords]

    ### end data verification

    # creates collector dictionary
    freqs_dict = {}

    # gets .txt filenames
    original_working_dir = os.getcwd()
    os.chdir(dir_with_txt)
    filenames = [i for i in os.listdir() if re.search(r"\.txt$", i, flags=re.I)]

    # count = 0
    for i in filenames:
        with open(i) as fin:
            for ln in fin:

                # checks whether the node word is in the current line
                if re.search(node_wd, ln, flags=re.I):
                # if occursin(node_wd, ln)

                    # split up current line into words
                    wds = re.split(r"[^-'a-z]+", ln, flags=re.I)
                    wds = [i for i in wds if len(i) > 0]

                    # loop over the words in the current line
                    for j in range(len(wds)):

                        # if the current word matches the node word
                        if re.search(node_wd, wds[j], flags=re.I):

                            # loop over the collocates within the span
                            for k in span_to_search:

                                # if the current span word is the node word
                                if k == 0:
                                    continue

                                # try to get the next collocate word, if it doesn't fall outside the range of the words in the current line
                                try:
                                    collocate_wd = wds[j + k].upper()

                                    # don't add collocate if stopword
                                    if collocate_wd not in stopwords:
                                        freqs_dict[collocate_wd] = freqs_dict.get(collocate_wd, 0) + 1
                                except:
                                    continue

    freqs_df = pd.DataFrame(list(freqs_dict.items()), columns = ["collocate", "freq"])

    # limit results to minimum frequency
    freqs_df = freqs_df[(freqs_df.freq >= min_freq)]


    # sort in descending order by frequency, then in ascending order by collocate
    freqs_df = freqs_df.sort_values(["freq", "collocate"], ascending=[False, True])

    # change to original working directory
    os.chdir(original_working_dir)

    return freqs_df


### test the function
dir_with_txt = "/Users/ekb5/Corpora/gen_conf_trunc/"
node_wd = r"\bprophet\b"  # as regex
span = 4
side = "both"
min_freq = 3

from stop_words import get_stop_words  # mind the underscores
stopwords = get_stop_words('en')

results = find_collocates(dir_with_txt, node_wd, stopwords, span, side, min_freq)
print(results.iloc[:10])

print(time.time() - start, "seconds")
