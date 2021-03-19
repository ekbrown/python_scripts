"""
A Python script to webscrape the frequency of search terms in the Corpus of Contemporary American English
Earl Kjar Brown, ekbrown byu edu (add appropriate characters to create email)
"""

# import the workhorses
import random, requests
from lxml import html
from time import sleep

# read in search terms from TXT file
with open("/Users/ekb5/Downloads/wds_generciding.txt") as infile:
    wds = [f.strip() for f in infile.readlines()]

# create session object in order to hold onto cookies
s = requests.Session()

# SPECIFY YOUR EMAIL AND PASSWORD THAT YOU USE TO ACCESS THE MARK DAVIES CORPORA
email = "HERE"
password = "HERE"

# get initial cookies and login to the corpus
s.get("https://www.english-corpora.org/")
s.get("https://www.english-corpora.org/coca/")
s.get("https://www.english-corpora.org/coca/login.asp?email=" + requests.utils.quote(email) + "&password=" + requests.utils.quote(password) + "&B1=Log+in&e=")

# create outfile
with open("/Users/ekb5/Downloads/freqs_COCA.csv", mode = "w", encoding = "utf8") as outfile:
    outfile.write("wd,freq\n")
    for w in wds:

        print("working on " + w)

        # create dictionary to hold the parameters and their corresponding values that will be passed in with the POST request
        payload = {
            'chartx4': 'n',
            'chooser': 'seq',
            'clickType': 'w',
            'allcoll': 'n',
            'ignoreHighFreq': 'n',
            'fromC': '',
            'sessionID': '',
            'bigNgrams': 'n',
            'isVC': 'n',
            'whatdo': '',
            'whatdo1': '',
            'showHelp': '',
            'wl': '4',
            'wr': '4',
            'w1a': '',
            'p': w,  # here's where the current word gets passed in
            'posDropdown': '',
            'posDropdown1': '',
            'w1b': '',
            'posWord2Dropdown': 'Insert+PoS',
            'w2': '',
            'posColDropdown': 'Insert+PoS',
            'submit1': 'Find+matching+strings',
            'sec1': '0',
            'sec2': '0',
            'sortBy': 'freq',
            'sortByDo2': 'freq',
            'minfreq1': 'freq',
            'freq1': '20',
            'freq2': '0',
            'numhits': '100',
            'kh': '200',
            'groupBy': 'words',
            'whatshow': 'raw',
            'saveList': 'no',
            'ownsearch': 'y',
            'changed': '',
            'word': '',
            'sbs': '',
            'sbs1': '',
            'sbsreg1': '',
            'sbsr': '',
            'sbsgroup': '',
            'redidID': '',
            'compared': '',
            'holder': '',
            'waited': 'y',
            'user': '',
            's1': '0',
            's2': '0',
            's3': '0',
            'perc': 'mi',
            'r1': '',
            'r2': '',
            'didRandom': 'y'
        }

        # make POST request
        freq = s.post("https://www.english-corpora.org/coca/x2.asp", data=payload, headers={'referer': "https://www.english-corpora.org/coca/x1.asp?showit=2"}, allow_redirects=True)

        # create tree in order to use the DOM to find the frequency
        tree = html.fromstring(freq.content)

        result = tree.xpath('//font[@color="#003399"]/text()')[0].strip()

        # print result to screen
        print("\t", result)
        outfile.write(w + "," + result + "\n")
        sleep(random.uniform(0.5, 1.5))
