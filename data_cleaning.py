# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 09:10:52 2020

@author: USER
"""
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import random
from urllib.error import HTTPError

#load data
print("Load Data")
df = pd.read_csv('airbnb_list.csv')


#fill the nan of amenities and review
A = df[df["Amenities"].isnull()]
print(len(A))
for i in A.index:
    print("Index:", i)
    room_url= "https://www.airbnb.com"+ df["url"].loc[i]
    time.sleep(random.randint(1, 5))
    try:
        room_responds = urlopen(room_url)
    except HTTPError:
        print("Don't have this page")
        continue
    room_html = BeautifulSoup(room_responds)
    amenities_list = room_html.find_all("div", class_="_19xnuo97")
    review_list = room_html.find_all("div", class_="_eeq7h0")

    if amenities_list!= None:
        amenities = ""
        for a in range(len(amenities_list)):
            amenities +=  amenities_list[a].text+", "
    print(amenities if amenities else "N/A")
    df["Amenities"].loc[i] = amenities if amenities else "N/A"
    
    if review_list!= None:
        review = ""
        for r in range(len(review_list)):
            review +=  review_list[r].text+"/ "
    print(review if review else "N/A")
    df["Review"].loc[i] = review if review else "N/A"

  
df.to_csv("airbnb_list.csv", encoding="utf-8", index=False) 