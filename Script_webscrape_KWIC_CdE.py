"""
Python script to control Selenium in order to webscrape keyword-in-context (KWIC) results from corpusdelespanol.org

Before using this script you need to download and install:
- Selenium: http://www.seleniumhq.org/
- ChromeDriver: https://sites.google.com/a/chromium.org/chromedriver/downloads
- the Python module selenium: https://pypi.python.org/pypi/selenium
- the Python module pandas: https://pypi.python.org/pypi/pandas

Earl K. Brown, ekbrown byu edu (add appropriate characters to create email)
with help from Tanner Eastmond
"""

# make available two functions in the selenium Python module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import pandas as pd  # module with a DataFrame object to work with tabular data
import re  # regular expressions module
import time  # to time the execution speed of this script

### start script
start = time.time()

# create driver object to control Google Chrome
# SPECIFY THE PATHWAY ON YOUR MACHINE TO CHROMEDRIVER
driver = webdriver.Chrome(executable_path='/Users/ekb5/chromedriver')
# other browsers can be used too: http://www.seleniumhq.org/download/

# visit initial page to get cookie
driver.get("https://www.corpusdelespanol.org/web-dial/")

# log in
driver.get("https://www.corpusdelespanol.org/web-dial/login1.asp")
username = driver.find_element_by_name("email")
password = driver.find_element_by_name("password")

# SPECIFY YOUR EMAIL AND PASSWORD THAT YOU USE TO ACCESS THE BYU CORPORA
username.send_keys("yourEmail@here.domain")
password.send_keys("yourPasswordHere")
driver.find_element_by_name("B1").click()

# SPECIFY SEARCH TERM FOR WHICH YOU'D LIKE KWIC RESULTS
search_term = "mesa"

driver.get("https://www.corpusdelespanol.org/web-dial/x1.asp")
driver.find_element_by_id("p").send_keys(search_term + Keys.ENTER)  # enter search term and press <Enter>
driver.switch_to.window(driver.window_handles[-1])  # go to the page that just opened (x2.asp)
driver.find_element_by_xpath('//a[@target="x3"]').click()  # click link to context (KWIC) page
driver.switch_to.window(driver.window_handles[-1])  # go to the page that just opened (x3.asp)

# SPECIFY OUTPUT FILE TO WHICH KWIC RESULTS WILL BE WRITTEN
output_file = "/Users/ekb5/Downloads/kwic.csv"

# create empty file
with open(output_file, 'w') as fin:
    pass

# SPECIFY THE MAXIMUM NUMBER OF PAGES OF KWIC RESULTS TO RETRIEVE (THERE ARE 100 RESULTS PER PAGE).
max_pages = 5
# Note: the corpus seems to only offer 1,000 pages, or 100,000 results, even if it says that there are more.

time.sleep(1)

# loop over pages of KWIC results
counter = 1
while driver.find_element_by_xpath('//b[contains(., ">")]') and counter != 1000 and counter <= max_pages:
    time.sleep(1)

    tbl = driver.find_element_by_xpath('//*[@id="zabba"]/table[2]').get_attribute('outerHTML')
    tbl = re.sub(r'<b>\(\d\)</b>', '', tbl)
    tbl = re.sub(r'<b>', '</td><td>', tbl)
    tbl = re.sub(r'</b>', '</td><td>', tbl)
    df = pd.read_html(tbl)[0]  # convert html table to pandas DataFrame
    df.to_csv(path_or_buf=output_file, sep='\t', encoding='utf-8', index=False, header=False, mode='a')  # append KWIC results from current page to .csv on hard drive
    driver.find_element_by_xpath('//b[contains(., ">")]').click()  # click to next KWIC page
    counter += 1

# close web browser
driver.close()
driver.quit()

# stop watch
end = time.time()
print("All done! The script took", end-start, "seconds to run.")

### end script
