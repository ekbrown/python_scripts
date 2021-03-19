"""
A Python script to webscrape the frequency of a search term in the Corpus del Español corpusdelespanol.org
Earl K. Brown, ekbrown byu edu (add appropriate characters to create email)
"""

import requests
from lxml import html

# create session object in order to hold onto cookies
s = requests.Session()

# SPECIFY YOUR EMAIL AND PASSWORD THAT YOU USE TO ACCESS THE BYU CORPORA
email = "email_here"
password = "password_here"

# get initial cookies and login to the corpus
s.get("https://www.corpusdelespanol.org/")
s.get("https://www.corpusdelespanol.org/web-dial/")
s.get("https://www.corpusdelespanol.org/web-dial/login.asp?email=" + requests.utils.quote(email) + "&password=" + requests.utils.quote(password) + "&B1=Log+in&e=")

# SPECIFY SEARCH TERM
search_term = 'ciudad'

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
    'p':search_term,
    'posDropdown':'Insert PoS',
    'w1b':'',
    'posWord2Dropdown':'Insert PoS',
    'w2':'',
    'posColDropdown':'Insert PoS',
    'submit1':'Find matching strings',
    'sec1':'0',
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
freq = s.post("https://www.corpusdelespanol.org/web-dial/x2.asp", data=payload, headers={'referer': "https://www.corpusdelespanol.org/web-dial/x1.asp?showit=2"}, allow_redirects=True)

# create tree in order to use the DOM to find the frequency
tree = html.fromstring(freq.content)
result = tree.xpath('//font[@color="#003399"]/text()')[0].strip()

# print result to screen
print(result)
