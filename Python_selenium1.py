from selenium import webdriver
import time

browser = webdriver.Firefox()
browser.get('https://twitter.com/7qSySkOpfvdLDiM/following')
time.sleep(2)

scroll_pixels = 100
for i in range(0,20):
    browser.execute_script("window.scrollBy(0,{})".format(str(scroll_pixels)))
    scroll_pixels += 100
    time.sleep(.1)


