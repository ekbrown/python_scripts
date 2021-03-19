"""
Python script to control Selenium in order to webscrape frequencies from corpusdelespanol.org

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
username.send_keys("YOUR_EMAIL_HERE")
password.send_keys("YOUR_PASSWORD_HERE")
driver.find_element_by_name("B1").click()

###
# search box
driver.get("https://www.corpusdelespanol.org/web-dial/x1.asp")

# create collector DataFrame
freqs = pd.DataFrame(columns=['wd', 'freq'])

# loop over search terms
# SPECIFY SEARCH TERMS FOR WHICH YOU'D LIKE FREQUENCIES
search_terms = ["la mujer", "hombre", "ciudad", "libro"]
counter = 0
for i in search_terms:
    driver.find_element_by_id("p").clear()  # clear previous search term from search box
    driver.find_element_by_id("p").send_keys(i + Keys.ENTER)  # enter current search term and press <Enter>
    driver.switch_to.window(driver.window_handles[-1])  # go to the page that just opened (x2.asp)
    word = driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr[2]/td[3]/a').text
    freq = driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr[2]/td[4]/font').text
    driver.switch_to.window(driver.window_handles[-2])  # switch back to x1.asp
    freqs.loc[counter] = [word, freq]  # add word and freq to collector DataFrame
    counter += 1
    print(word, freq)  # print to console

# write collector DataFrame to .csv file on hard drive
freqs.to_csv(path_or_buf="/Users/ekb5/Downloads/freqs.csv", sep='\t', encoding='utf-8', index=False, header=True, mode='w')

# close web browser
driver.close()
driver.quit()

# stop watch
end = time.time()
print("All done! The script took", end-start, "seconds to run.")

### end script
