# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 15:11:30 2020

@author: USER
"""


import time
from selenium import webdriver

driver = webdriver.Chrome('D:/USA 2020 summer/Machine Learning/ds_airbnb_proj/chromedriver')  # Optional argument, if not specified will search path.
driver.get('http://www.google.com/');
time.sleep(5) # Let the user actually see something!
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5) # Let the user actually see something!
driver.quit()
