# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 15:11:30 2020

@author: USER
"""


import time
from selenium import webdriver

driver = webdriver.Chrome('D:/USA 2020 summer/Machine Learning/ds_airbnb_proj/chromedriver')  # Optional argument, if not specified will search path.
driver.get('https://www.airbnb.com/s/New-York--NY--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=pagination&query=New%20York%2C%20NY&place_id=ChIJOwg_06VPwokRYv534QaPC8g&federated_search_session_id=585eec54-b658-4b46-9a76-61d0ba4a0851');
time.sleep(5) # Let the user actually see something!
room_href = driver.find_element_by_class_name('_gjfol0').click()
time.sleep(10) # Let the user actually see something!
#element = WebDriverWait(driver, 10).until(
#                EC.presence_of_element_located((By.class, '_1v4ygly5')).click()
#            )
amenities_list = driver.find_element_by_css_selector('a._1v4ygly5').click()

print(element)
driver.close()
