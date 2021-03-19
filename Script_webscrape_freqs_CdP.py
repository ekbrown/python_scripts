"""
A Python script to webscrape the frequency of a search term in the Corpus do Português corpusdoportugues.org
Earl K. Brown, ekbrown byu edu (add appropriate characters to create email)
"""

import requests
from lxml import html
from time import sleep

# create session object in order to hold onto cookies
s = requests.Session()

# SPECIFY YOUR EMAIL AND PASSWORD THAT YOU USE TO ACCESS THE BYU CORPORA
email = "YOUR EMAIL HERE"
password = "YOUR PASSWORD HERE"

# get initial cookies and login to the corpus
s.get("https://www.corpusdoportugues.org/")
s.get("https://www.corpusdoportugues.org/web-dial/")
s.get("https://www.corpusdoportugues.org/web-dial/login.asp?email=" + requests.utils.quote(email) + "&password=" + requests.utils.quote(password) + "&B1=Log+in&e=")

# SPECIFY SEARCH TERM
#search_term = 'cidade'

with open("/Users/ekb5/Documents/Port_sibilants/test_items.txt") as infile:
    wds = [f.strip() for f in infile.readlines()]
wds = wds[39:]

with open("/Users/ekb5/Documents/Port_sibilants/freqs3.csv", mode = "w", encoding = "utf8") as outfile:
    outfile.write("wd,freq\n")
    for w in wds:

        print("working on " + w)

        # create dictionary to hold the parameters and their corresponding values that will be passed in with the POST request
        payload = {
            'chooser':'seq',
            'isVC':'n',
            'whatdo':'',
            'whatdo1':'',
            'showHelp':'',
            'wl':'4',
            'wr':'4',
            'w1a':'',
            'p':w,
            'posDropdown':'Insert PoS',
            'w1b':'',
            'posWord2Dropdown':'Insert PoS',
            'w2':'',
            'posColDropdown':'Insert PoS',
            'submit1':'Find matching strings',
            'sec1':'1',
            'sec2':'0',
            'sortBy':'freq',
            'sortByDo2':'freq',
            'minfreq1':'freq',
            'freq1':'20',
            'freq2':'0',
            'numhits':'100',
            'kh':'200',
            'groupBy':'words',
            'whatshow':'raw',
            'saveList':'no',
            'ownsearch':'y',
            'changed':'',
            'word':'',
            'sbs':'',
            'sbs1':'',
            'sbsreg1':'',
            'sbsr':'',
            'sbsgroup':'',
            'redidID':'',
            'compared':'',
            'holder':'',
            'waited':'',
            'user':'',
            's1':'',
            's2':'',
            's3':'',
            'perc':'mi',
            'r1':'',
            'r2':'',
            'didRandom':'y'
        }

        # make POST request
        freq = s.post("https://www.corpusdoportugues.org/web-dial/x2.asp", data=payload, headers={'referer': "https://www.corpusdelespanol.org/web-dial/x1.asp?showit=2"}, allow_redirects=True)

        # create tree in order to use the DOM to find the frequency
        tree = html.fromstring(freq.content)
        result = tree.xpath('//font[@color="#003399"]/text()')[0].strip()

        # print result to screen
        print(w, result)
        outfile.write(w + "," + result + "\n")
        sleep(1)
