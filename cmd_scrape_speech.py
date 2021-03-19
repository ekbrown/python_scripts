"""Python command-line tool to download a speech from https://factba.se/.
Earl K. Brown, ekbrown byu edu (add appropriate characters to create email)
Note: You need to pip install "requests_html" before running this script.
Usage: python3 cmd_scrape_speech.py [-o /pathway/to/dir] URL
"""

import argparse, json, os, requests_html

### parse command-line arguments
parser = argparse.ArgumentParser(description='Scrape text of a speech from factba.se')
parser.add_argument("-o", "--output", type=str, required = False, help = "Optional pathway to directory where the TXT file with the text of the speech should be saved. If not given, the TXT file is saved to the working directory.")
parser.add_argument("URL", type=str, help="The URL of the webpage on factba.se with the speech whose text is desired.")
args = parser.parse_args()

### request webpage from factba.se
session = requests_html.HTMLSession()
r = session.get(args.URL)

### scrape JSON-encoded data from the source HTML of webpage
spch = r.html.xpath("//script[@type='application/ld+json']")
spch = json.loads(spch[0].text)

### create the filename of the outfile
if args.output:
    filename = args.output + os.path.basename(args.URL) + ".txt"
else:
    filename = os.path.basename(args.URL) + ".txt"

### write speech to outfile
with open(filename, mode = "w", encoding = "utf8") as outfile:
    outfile.write(args.URL + "\n" + spch['articleBody'].strip())

### announce finish
print(f"\nDone!\nYou should now have the following file on your hard drive: {filename}")
