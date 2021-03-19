"""Command-line tool to scrape text from a webpage and save it to a TXT file in the working directory.
Earl K. Brown, ekbrown byu edu (add appropriate characters to create email)
Usage: python3 cmd_html2txt.py URL [-o filename.txt]
"""

import argparse, justext, re, requests

parser = argparse.ArgumentParser(description='Webscrape text from a static webpage and save it to a TXT file in the current working directory.')
parser.add_argument('URL', type=str, help='The URL of the webpage whose text you want to scrape.')
parser.add_argument("-o", "--output", type=str, required=False, help="Optional filename to save text to; if not given, the filename is a modified version of the URL.")
parser.add_argument("-l", "--lang", type=str, required=False, help="Optional language that the webpage is written in.")
args = parser.parse_args()

r = requests.get(args.URL)
r.encoding = r.apparent_encoding


if args.lang:
    lang = args.lang
else:
    lang = "English"

paragraphs = justext.justext(r.text, justext.get_stoplist(lang))

txt = ""
for paragraph in paragraphs:
  if not paragraph.is_boilerplate:
    txt += paragraph.text + "\n"

if args.output:
  filename = args.output
else:
  filename = re.sub(r"\W+", "_", args.URL) + ".txt"

with open(filename, mode = "w", encoding = "utf8") as outfile:
  outfile.write(txt)
