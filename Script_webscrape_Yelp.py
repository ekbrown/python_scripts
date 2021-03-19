import time
from selenium import webdriver
import os, re

driver = webdriver.Chrome("/Users/ekb5/chromedriver")

url = 'https://www.yelp.com/biz/brick-oven-provo-provo-2'
driver.get(url)

max_pages = 10
counter = 1
with open('/Users/ekb5/Downloads/' + os.path.basename(url) + '.txt', 'w') as fout:
    while True and counter <= max_pages:
        reviews = driver.find_elements_by_xpath('//div[@class="review-content"]/p')
        # stars = driver.find_element_by_xpath('div[@class="i-stars i-stars--regular-4 rating-large"]')
        stars = driver.find_elements_by_xpath('//div[@class="review-content"]/div/div/div[contains(@class, "stars")]')
        stars = [i.get_attribute("title") for i in stars]
        stars = [re.sub(r"[^\d+\.]", "", i) for i in stars]
        print(stars)
        print(type(stars))

        for i in range(len(reviews)):
            # star = stars[i]
            # review = reviews[i]
            fout.write(stars[i] + ": " + reviews[i].text + '\n-------\n')

        # for review in reviews:
        #     fout.write(review.text + '\n-------\n')

        counter += 1
        if not driver.find_element_by_link_text("Next"):
            break
        driver.find_element_by_link_text("Next").click()
        time.sleep(3)

driver.close()
driver.quit()

