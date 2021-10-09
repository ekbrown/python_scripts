"""
Python script to control Selenium in order to webscrape frequencies from COCA

Earl Kjar Brown, ekbrown byu edu (add characters to create email)

Before using this script you need to download and install:
- Google Chrome web browser
- the Python module selenium: https://pypi.org/project/selenium/
- ChromeDriver (version must match version of Chrome): https://chromedriver.chromium.org/downloads
"""

# make available two functions in the selenium Python module
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time  # to time the execution speed of this script

### UPDATE THESE LINES ###
email = "YOUR_EMAIL_HERE"
password = "YOUR_PASSWORD_HERE"
path_to_chromedriver = '/PATH/TO/chromedriver'
search_terms = ["dude", "computer", "asdfasdf", "walk_N*", "walk_V*"]
nap_len = 2

### start script
start = time.time()

# create driver object to control Google Chrome
driver = webdriver.Chrome(executable_path = path_to_chromedriver)
# other browsers can be used too: http://www.seleniumhq.org/download/

# visit initial page to get cookie
driver.get("https://www.english-corpora.org/coca/")

### log in ###
driver.switch_to.frame(driver.find_element_by_xpath("//frameset[@id='topper']/frame"))
driver.find_element_by_css_selector("#myLink1").click()
time.sleep(nap_len)
driver.switch_to.default_content()
driver.switch_to.frame(driver.find_element_by_css_selector("frame[name='x4']"))
driver.find_element_by_name("email").send_keys(email)
driver.find_element_by_name("password").send_keys(password)
driver.find_element_by_name("B1").click()
time.sleep(nap_len)

### loop over search terms ###
counter = 0

# open connection to outfile
with open("/Users/ekb5/Downloads/freqs.csv", mode="w", encoding="utf8") as outfile:
    outfile.write("term,wd,freq\n")

    # loop over search terms
    for s in search_terms:
        counter += 1
        print("Working on term " + str(counter) + " of " + str(len(search_terms)) + ": " + s)

        # go to search tab
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_xpath("//frameset[@id='topper']/frame"))
        search_tab = driver.find_element_by_css_selector("a#link1").click()
        time.sleep(nap_len)

        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_css_selector("frame[name='x1']"))

        # put current search term into search box and click submit button
        driver.find_element_by_css_selector("input#p").clear()
        driver.find_element_by_css_selector("input#p").send_keys(s)
        driver.find_element_by_css_selector("input#submit1").click()
        time.sleep(nap_len)

        # get frequency of current search term
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_css_selector("frame[name='x2']"))
        try:
            term = driver.find_element_by_css_selector("#url1").text
            freq = driver.find_element_by_css_selector("#zabba > table.auto-style1 > tbody > tr:nth-child(2) > td:nth-child(4) > font").text
        except selenium.common.exceptions.NoSuchElementException:
            term = "NA"
            freq = 0
        # write out to CSV file
        print("\t", s, term, freq)  # print to console
        outfile.write(f"{s},{term},{freq}\n")

# close web browser
driver.close()
driver.quit()

# stop watch
end = time.time()
print("All done! The script took", round(end-start, 1), "seconds to run.")

### end script
