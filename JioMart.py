
import os
import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import re
from selenium.webdriver.common.keys import Keys


# from selenium import webdriver

# options = webdriver.ChromeOptions()
# options.add_argument("--incognito")

# driver = webdriver.Chrome(options=options)
# driver.get('https://google.com')


driver = webdriver.Chrome("C:\webdrivers\chromedriver.exe")

driver.get('https://www.jiomart.com/c/groceries/2') #opens up google

def scroll():
    SCROLL_PAUSE_TIME = 3

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height




pin_codes = ["110001","380009", "400001"]
products = [ "sunflower oil","khichdi"]

def scrape(pin_codes, products):
    product_id_list = []
    product_name_list = []
    mrp_list = []
    price_list = []
    availbility = []
    pincode_list = []
    for pincode in pin_codes:
        driver.get('https://www.jiomart.com/c/groceries/2') #opens up google
        driver.find_element_by_id('delivery_details').click()
        driver.find_element_by_id('rel_pincode').send_keys(pincode)
        driver.find_element_by_class_name('apply_btn').click()
        time.sleep(2)
        for product in products:
            print(product)
            driver.find_element_by_id('search').send_keys(product)
            time.sleep(2)
            driver.find_element_by_id('search').send_keys(Keys.ENTER)
            search(product)
            
    #         scroll()
            src = driver.page_source
            soup = BeautifulSoup(src, 'lxml')
            details = soup.find('div', attrs={'id': 'hits'})
    #         print(details)
            links = details.findAll('a',{'class':"category_name prod-name"})
            link_list = []
            for link in links:
                link_list.append(link.get('href'))
            
            for link in link_list:
                try:
                    product_id_list.append(link.split('/')[-1])
                    driver.get('https://www.jiomart.com/'+str(link)) #opens up google
                    src = driver.page_source
                    soup = BeautifulSoup(src, 'lxml')
                    product_name_list.append(soup.find('div', attrs={'class':'title-section'}).text)
                    mrp_list.append(soup.find('span', attrs={'class':'price'}).text)
                    price_list.append(soup.find('span', attrs={'class':'final-price'}).text)
                    availbility.append(soup.find('div', attrs={'class':'stock_details'}).text)
                    pincode_list.append(pincode)
                except AttributeError as e:
                    print(e)
        continue
    df = pd.DataFrame({"Product Id":product_id_list, "Product":product_name_list, "MRP":mrp_list,"Price":price_list,"Availability":availbility, "Pincode":pincode_list})
    df.to_csv("Data.csv")





