"""Python script to control Selenium to webscrape tweets from Twitter's advanced search page.
Earl Kjar Brown, ekbrown byu edu (add appropriate characters to create email)
Note: Before running script, you must pip install selenium and
install chromedriver (https://chromedriver.chromium.org).
Note: You must use Python 3.6+.
"""

import datetime, re, time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lxml import html

def get_exact_phrase_twitter(exact_phrase, path_webdriver, path_file, lang = "en", max_scrolls = 10, sleep_duration = 3):

    print(f'Working on getting tweets with "{exact_phrase}"...')

    ### open Chrome web browser and visit Twitter's advanced search
    driver = webdriver.Chrome(path_webdriver)
    driver.get('https://twitter.com/search-advanced')
    time.sleep(sleep_duration)
    driver.find_element_by_xpath("//input[@name='thisExactPhrase']").send_keys(exact_phrase)
    time.sleep(1)
    driver.find_element_by_xpath("//input[@name='thisExactPhrase']").send_keys(Keys.RETURN)
    # driver.find_element_by_xpath(f"//select[@id='Language']/option[@value='{lang}']").click()
    # driver.find_element_by_xpath("//div[@role='button']").click()

    time.sleep(sleep_duration)

    ### scroll up to max_scrolls times
    counter = 0
    last_height = driver.execute_script("return document.body.scrollHeight")
    while counter < max_scrolls:
        counter += 1
        print("\ton scroll", counter)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_duration)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("No more screen to scroll down.")
            break
        last_height = new_height

    ### now that the scrolling has finished, get the tweets
    tweets = driver.find_elements_by_xpath("//div[@data-testid='tweet']")

    ### create collector data frame
    to_push = pd.DataFrame(columns=['username', 'date', 'text'])

    ### loop over tweets
    counter = 0
    for t in tweets:

        ### get HTML of current tweet
        raw_html = t.get_attribute("outerHTML")
        tree = html.fromstring(raw_html)

        ### get the user
        user = tree.xpath("//div[@dir='ltr']/span/text()")

        ### get timestamp
        date = tree.xpath("//time[@datetime]")
        date = [d.get('datetime') for d in date]
        date = date[0]

        ### get the text of the tweet
        txt = t.text
        txt = re.sub(r"[\n\t]", " ", txt)

        ### push to collector data frame
        to_push.loc[counter] = [user, date, txt]
        counter += 1

    ### write collector data frame to hard drive
    to_push.sort_values(by=['date'], axis=0, ascending=False, inplace=True)
    to_push.to_csv(path_or_buf=path_file, sep='\t', encoding='utf-8', index=False, header=True, mode='w')

    ### close web browser
    driver.close()
    driver.quit()

#########################
### test the function ###
#########################

### SPECIFY THIS INFO
exact_phrase = "kleenex"  # the exact phrase to search for
path_webdriver = "/Users/ekb5/chromedriver"  # pathway to chromedriver
path_file = "/Users/ekb5/Downloads/tweets.csv"  # CSV file
lang = "en"  # two-character language code, e.g., "en"glish, "es"pañol, "ko"rean, etc.
max_scrolls = 10  # the maximum number of scroll-downs to perform
sleep_duration = 2  # the number of seconds to allow the AJAX call to return new results after each scroll-down

### SAVE THE SCRIPT AND RUN IT!
get_exact_phrase_twitter(exact_phrase, path_webdriver, path_file, lang, max_scrolls, sleep_duration)
print(f"All done!\nYou should now have a file named {path_file} with tweets, ready to import into spreadsheet software.")
