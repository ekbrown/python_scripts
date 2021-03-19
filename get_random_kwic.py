"""Python script to control Selenium to scrape a random sample of 100, 200, or 500 keyword-in-context (KWIC) results in the COCA corpus.
Earl K. Brown, ekbrown byu edu (add appropriate characters to create email)

Before using this script you need to download and install:
- Selenium: http://www.seleniumhq.org/
- ChromeDriver: https://sites.google.com/a/chromium.org/chromedriver/downloads
- the Python module selenium: https://pypi.python.org/pypi/selenium
- the Python module pandas: https://pypi.python.org/pypi/pandas

Note: Use Python 3.6+
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re
import time

### DEFINE THE FUNCTION ###
def get_kwic(search_term, email, password, chrome_driver_path, output_file, num_hits = 100):

    nap_dur = 3

    # start driver
    driver = webdriver.Chrome(executable_path=chrome_driver_path)

    # log in
    driver.get("https://www.english-corpora.org/")
    driver.get("https://www.english-corpora.org/login.asp")
    driver.find_element_by_name("email").send_keys(email)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("B3").click()
    time.sleep(nap_dur)

    # go to COCA
    driver.get("https://www.english-corpora.org/coca/")
    mainpage = driver.get("https://www.english-corpora.org/coca/x.asp")
    time.sleep(nap_dur)

    # enter search term
    search_box = driver.find_element_by_xpath("//frame[@name='x1']")
    driver.switch_to.frame(search_box)
    driver.find_element_by_id("p").send_keys(search_term + Keys.ENTER)
    time.sleep(nap_dur)

    # focus on frequency list and click on random sample link
    driver.switch_to.frame(mainpage)
    freq_list = driver.find_element_by_xpath("//frame[@name='x2']")
    driver.switch_to.frame(freq_list)
    push_regex = f"//a[contains(@target,'x3') and contains(@href, 'x3.asp?n={num_hits}')]"
    driver.find_element_by_xpath(push_regex).click()
    time.sleep(nap_dur)

    # scrape the KWIC results
    driver.switch_to.frame(mainpage)
    kwic_list = driver.find_element_by_xpath("//frame[@name='x3']")
    driver.switch_to.frame(kwic_list)

    # write to output file
    tbl = driver.find_element_by_xpath('//*[@id="zabba"]/table[2]').get_attribute('outerHTML')
    tbl = re.sub(r'<b>\(\d\)</b>', '', tbl)  # put node word in its own column
    tbl = re.sub(r'<b>', '</td><td>', tbl)  # cont.
    tbl = re.sub(r'</b>', '</td><td>', tbl)  # cont.
    df = pd.read_html(tbl)[0]  # convert html table to pandas DataFrame
    df.to_csv(path_or_buf=output_file, sep='\t', encoding='utf-8', index=False, header=False, mode='w')

    # close web browser
    driver.close()
    driver.quit()

    ### END FUNCTION DEFINITION ###


### TEST THE FUNCTION ###
search_term = "*able"
email = "yourUsername@domain.ext"  # the email you use to login to the Davies corpora
password = "yourPassword"  # and the associated password
chrome_driver_path = "/home/earl/Documents/chromedriver"  # pathway to chromedriver executable file
output_file = "/home/earl/Downloads/kwic.csv"  # pathway to CSV file to save KWIC results to
num_hits = 100  # number of results, from among 100, 200, or 500

get_kwic(search_term, email, password, chrome_driver_path, output_file, num_hits)

print(f"All done!\nThe following CSV file should be ready to be imported into spreadsheet software: {output_file}")
