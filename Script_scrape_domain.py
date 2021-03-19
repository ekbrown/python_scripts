"""Python script to scrape a website.
Earl K. Brown, ekbrown byu edu (add appropriate characters to create email)
Note: You'll need to pip install justext and requests_html before running this script.
"""

import justext, os, re
from random import uniform
from requests_html import HTMLSession
from time import sleep

def process_url(domain, url, session, output_dir):
    """Function to scrape text from URL and return links.
    domain: string -- the domain URL of the website;
    url: string -- the URL whose text should be scraped;
    session: an HTMLSession object from requests_html;
    output_dir: string -- the directory on the hard drive to save TXT files to;
    return value: list -- links to other webpages within domain on current webpage.
    """

    # request HTML
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
    r = session.get(url, headers = headers)
    r.encoding = r.apparent_encoding

    # get text out of webpage
    paragraphs = justext.justext(r.text, justext.get_stoplist("English"))
    txt = ""
    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            txt += paragraph.text + "\n"

    # save text to hard drive
    with open(os.path.join(output_dir, re.sub(r"\W+", "_", url)) + ".txt", "w", encoding = "utf8") as outfile:
        outfile.write(url + "\n")
        outfile.write(txt)

    # return links to other webpages
    return [l for l in list(r.html.absolute_links) if l[:len(domain)] == domain]


#########################
### test the function ###
#########################

domain = "https://www.geico.com"  # SPECIFY THE DOMAIN URL
output_dir = "/Users/ekb5/Downloads/delete"  # SPECIFY THE DIRECTORY TO SAVE TXT FILES TO
max_pages = 5  # SPECIFY THE MAX NUMBER OF WEBPAGES TO SCRAPE

# SAVE SCRIPT AND RUN IT!
session = HTMLSession()
need_to_visit = [domain]
already_visited = set()

count = 0
while (len(need_to_visit) > 0) & (count < max_pages):
    cur_file = need_to_visit.pop()
    if cur_file not in already_visited:
        count += 1
        print(f"Working on page {count}: {cur_file}")
        new_links = process_url(domain, cur_file, session, output_dir)
        already_visited.add(cur_file)
        need_to_visit.extend(new_links)
        rand_float = uniform(0.5, 1.5)
        print(f"\tGonna sleep for {round(rand_float, 1)} seconds...")
        sleep(rand_float)

print(f"All done!\nProcessed {count} webpages:\n{sorted(already_visited)}")
