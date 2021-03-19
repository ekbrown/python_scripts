"""Python function to get concordance lines of a regex in TXT files in a directory
Earl K. Brown, ekbrown byu edu (add appropriate characters to create email)
"""

import os, re, pandas as pd


def get_conc(search_regex, pathway, case_sens = False, num_token_span = 10, sort_by = "original"):
    """Retrieve concordance lines of a regex in TXT files in a directory
    param - search_regex: a regular expression to search for
    param - pathway: the pathway to the directory with .txt files; other file types are ignored
    param - case_sens: case sensitive search (default = False)
    param - num_token_span: number of words/punctuation of context around match (default = 10)
    param - sort_by: which column to sort by, among "original" (as found; no sorting), "L1" (by the word/punctuation to the left of the match), "R1" (by the word/punctuation to the right of the match) (default is "original")
    return value: a pandas DataFrame
    """

    # get filenames
    os.chdir(pathway)
    filenames = [f for f in os.listdir() if re.search("\.txt$", f, re.I)]

    # create collector data frame
    df = pd.DataFrame(columns = ["file", "char_offset", "pre", "match", "post", "L1", "R1"])

    # loop over files
    for filename in filenames:
        with open(filename, mode = "r", encoding = "utf8") as infile:  # assume "UTF-8" character encoding
            whole_file = infile.read()  # read in whole file as a single string

        # search for regex, taking into account the case sensitivity specified by the user
        if case_sens:
            matches = re.finditer(search_regex, whole_file)
        else:
            matches = re.finditer(search_regex, whole_file, flags = re.I)

        # loop over matches in current file, if any
        for match in matches:
            if match is None:
                continue
            else:

                # get preceding words
                pre_wds = whole_file[:match.start()]
                pre_wds = [wd.strip() for wd in re.split(r"(?=[^-'a-záéíóúüñ]+)", pre_wds, flags=re.I)]
                pre_wds = [wd for wd in pre_wds if len(wd) > 0]
                try:
                    pre_wds = pre_wds[-num_token_span:]
                except IndexError:
                    pass
                L1 = pre_wds[-1]  # get one word to the left
                pre_wds = " ".join(pre_wds)

                # get following words
                post_wds = whole_file[match.end():]
                post_wds = [wd.strip() for wd in re.split(r"(?=[^-'a-záéíóúüñ]+)", post_wds, flags=re.I)]
                post_wds = [wd for wd in post_wds if len(wd) > 0]
                try:
                    post_wds = post_wds[:num_token_span]
                except IndexError:
                    pass
                R1 = post_wds[0]  # get one word to the right
                post_wds = " ".join(post_wds)

                # append to collector data frame
                to_append = {"file": os.path.basename(filename), "char_offset": match.start(), "pre": pre_wds, "match": match.group(), "post": post_wds, "L1": L1, "R1": R1}
                df = df.append(to_append, ignore_index=True)

    # sort data frame, if needed
    if sort_by == "L1":
        df['L1_lower'] = df['L1'].str.lower()
        df = df.sort_values(by=['L1_lower', 'match', 'file', 'char_offset'])
        df = df.drop(['L1_lower'], axis=1)
    elif sort_by == "R1":
        df['R1_lower'] = df['R1'].str.lower()
        df = df.sort_values(by = ['R1_lower', 'match', 'file', 'char_offset'])
        df = df.drop(['R1_lower'], axis = 1)

    return df


### test the function
results = get_conc(r"\bescuela\b", "/Users/ekb5/Corpora/USA/California/Salinas/transcripts/", sort_by = "R1")
results.to_csv("/Users/ekb5/Downloads/results.csv", index = False)
