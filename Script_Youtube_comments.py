"""
Python script to control Selenium in order to webscrape comments below a Youtube video
Earl K. Brown, ekbrown byu edu (add appropriate characters to create email)
based on some code by Gary Law
"""

from selenium import webdriver
import time

# SPECIFY PATHWAY TO CHROMEDRIVER
driver = webdriver.Chrome("/Users/ekb5/chromedriver")

# SPECIFY ID OF YOUTUBE VIDEO (I.E., THE LAST PART OF THE URL)
# id = "tnzz-eFmKaw"  # Rhett and Link OCD Song
# id = "jkwp0GkUFrw"  # chess video
id = "5PL0TmQhItY"  # word embeddings

# create url to video and open it
url = "https://www.youtube.com/watch?v=" + id
driver.get(url)
time.sleep(3)  # wait to allow page to load
driver.execute_script("window.scrollBy(0, 200);")
time.sleep(2)

# SPECIFY THE MAXIMUM NUMBER OF PAGES OF COMMENTS TO LOAD
max_pages = 10

# loop over pages (or scroll-downs) of comments
# height = 500

with open('/Users/ekb5/Downloads/jquery-3.4.0.js', 'r') as jquery_js: 
    jquery = jquery_js.read() #read the jquery from a file
    driver.execute_script(jquery) #active the jquery lib

counter = 1
while counter <= max_pages:
    print("Working on page", counter)
    counter += 1
    # driver.execute_script("window.scrollTo(0, " + str(height) + ");")
    driver.execute_script("window.scrollBy(0, 5000);")
    # height += 1000
    # print(driver.execute_script("return document.body.scrollHeight"))
    # print(driver.get_window_size())
    height = driver.execute_script("return $(document).height()")
    print (height)

    time.sleep(3)

# get comments
comments = driver.find_elements_by_xpath('//*[@id="content-text"]')

# SPECIFY THE DIRECTORY IN WHICH YOU'D LIKE THE RESULTS WRITTEN
dir = "/Users/ekb5/Downloads"

# write comments to .txt file in directory specified above
with open(dir + "/comments_" + id + ".txt", "w", encoding="utf-8") as fout:
    for comment in comments:
        fout.write(comment.text + "\n")

print("Comments download completed!")

# Close the browser
driver.close()
driver.quit()
