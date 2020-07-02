# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 16:40:06 2020

@author: USER
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from urllib.error import HTTPError
import time
import random

df = pd.DataFrame(columns=["Name","Location","Type of room","Rating","Number of review","price","Amenities","Review","url"])
#https://www.airbnb.com/s/New-York--NY--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=pagination&query=New%20York%2C%20NY&place_id=ChIJOwg_06VPwokRYv534QaPC8g&federated_search_session_id=585eec54-b658-4b46-9a76-61d0ba4a0851&section_offset=1&items_offset=20
for page in range(0,15):
    url = "https://www.airbnb.com/s/New-York--NY--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=pagination&query=New%20York%2C%20NY&place_id=ChIJOwg_06VPwokRYv534QaPC8g&federated_search_session_id=585eec54-b658-4b46-9a76-61d0ba4a0851"
    if page!=0:
        url=url+"&section_offset=3&items_offset="+str(page*20)
    # 解決 400 Error
    try:
        responds = urlopen(url)
    except HTTPError:
        print("finish!!")
        break
    print("page:", page+1)
    # 分析盒子
    html = BeautifulSoup(responds)
    # 找盒子
    rlist = html.find_all("div", class_="_8ssblpx")
    for r in rlist:
        location = r.find("div", class_="_167qordg")
        name = r.find("div", class_="_1c2n35az")
        type_of_room = r.find("div", class_="_kqh46o")
        rating = r.find("span", class_="_10fy1f8")
        num_of_review = r.find("span", class_="_a7a5sx")
        price = r.find("span", class_="_1p7iugi")
        room_href = r.find("a", class_="_gjfol0")["href"]
        room_url= "https://www.airbnb.com"+room_href
        time.sleep(random.randint(1, 5))
        room_responds = urlopen(room_url)
        room_html = BeautifulSoup(room_responds)
        amenities_list = room_html.find_all("div", class_="_19xnuo97")
        review_list = room_html.find_all("div", class_="_eeq7h0")
    
        if amenities_list!= None:
            amenities = ""
            for a in range(len(amenities_list)):
                amenities +=  amenities_list[a].text+", " 
        
        if review_list!= None:
            review = ""
            for r in range(len(review_list)):
                review +=  review_list[r].text+"/ "
            
        print(name.text if name else "N/A", location.text if location else "N/A", type_of_room.text if type_of_room else "N/A", rating.text if rating else "N/A", num_of_review.text if num_of_review else "N/A", price.text if price else "N/A", amenities if amenities else "N/A", review if review else "N/A", room_href)
        
        
        # 建立資料序列
        s = pd.Series([name.text if name else "N/A", location.text if location else "N/A", type_of_room.text if type_of_room else "N/A", rating.text if rating else "N/A", num_of_review.text if num_of_review else "N/A", price.text if price else "N/A", amenities if amenities else "N/A", review if review else "N/A", room_href],
                  index=["Name","Location","Type of room","Rating","Number of review","price","Amenities","Review","url"])
        df = df.append(s, ignore_index=True) # ignore_index= True 重新標號 不保留原本的標號

            
df.to_csv("airbnb_list.csv", encoding="utf-8", index=False) # index=False 不儲存標號之列表

