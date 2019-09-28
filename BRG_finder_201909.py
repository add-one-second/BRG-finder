'''
Find BRG opportunities with Google Search

'''


# Import packages
import time, os, random, warnings, sqlite3, xlrd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd

# start a chrome browser
cwd = os.getcwd()
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})

driver = webdriver.Chrome(cwd + '\chromedriver_win32\chromedriver.exe', chrome_options=options)

driver.get("https://www.google.com/")

hotel_name_list = ['Andaz Maui at Wailea Resort', 'Hyatt Regency Maui Resort and Spa', 'Courtyard Maui Kahului Airport', 'Residence Inn Maui Wailea', \
    'Wailea Beach Resort - Marriott, Maui', 'The Ritz-Carlton, Kapalua', 'Sheraton Maui Resort & Spa', 'Westin Maui', \
    'Grand Wailea, A Waldorf Astoria Resort']

time.sleep(random.uniform(1, 2))  # add random intervals between actions -- mimic human behavior to prevent site

def date_box_click(checkin_date, checkout_date):
    # inner function for check in and check out date inputs
    print('checkin date:', checkin_date, 'checkout date:', checkout_date)
    driver.find_elements_by_class_name("lxhdrtxt").click()  # click on the check in date gridcell
    time.sleep(random.uniform(1, 2))
    driver.find_elements_by_class_name("hudp-nextMonth")[0].click()  # move to Nov.
    driver.find_elements_by_class_name("hudp-nextMonth")[0].click()
    time.sleep(random.uniform(1, 2))
    driver.find_element_by_xpath("//td[@aria-label='" + checkin_date + "']").click()
    time.sleep(random.uniform(1, 2))
    # elems = driver.find_elements_by_class_name("hudp-nextMonth")
    # elems[0].click()
    # time.sleep(1)
    driver.find_element_by_xpath("//td[@aria-label='" + checkout_date + "']").click()
    time.sleep(random.uniform(2, 5))
    return driver

def hotel_name_input(hotel_name):
    print('working on', hotel_name)
    # elem = driver.find_element_by_id("gbqfbb") # now is feel luck...
    elem = driver.find_element_by_xpath("//input[@class='gLFyf gsfi']") # find the input element
    elem.click()  # click
    time.sleep(random.uniform(1, 2))
    elem.clear()
    elem.send_keys(hotel_name_list[0])
    time.sleep(random.uniform(0, 2))
    elem.send_keys(Keys.RETURN)
    time.sleep(random.uniform(1, 2))

hotel_name = hotel_name_list[0]

checkin_dates = ['13 Jul']
checkout_dates = ['14 Jul']


https://www.tripadvisor.com/Hotel_Review-g60982-d87040-Reviews-Hyatt_Place_Waikiki_Beach-Honolulu_Oahu_Hawaii.html
https://www.tripadvisor.com/Hotel_Review-s1-g609129-d4459053-Reviews-Andaz_Maui_At_Wailea_Resort-Wailea_Maui_Hawaii.html