# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 16:40:06 2020

@author: USER
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

df = pd.DataFrame(columns=["url"])
#https://zh-t.airbnb.com/s/Taipei-City/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=pagination&place_id=ChIJi73bYWusQjQRgqQGXK260bw&federated_search_session_id=ae03436b-1c5d-417b-9a38-ee6ec4f21131&query=%E5%8F%B0%E5%8C%97%2C%20%E5%8F%B0%E7%81%A3%E5%9C%B0%E5%8D%80
#https://zh-t.airbnb.com/s/Taipei-City/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=pagination&place_id=ChIJi73bYWusQjQRgqQGXK260bw&federated_search_session_id=ae03436b-1c5d-417b-9a38-ee6ec4f21131&query=%E5%8F%B0%E5%8C%97%2C%20%E5%8F%B0%E7%81%A3%E5%9C%B0%E5%8D%80&section_offset=3&items_offset=20
#https://zh-t.airbnb.com/s/Taipei-City/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=pagination&place_id=ChIJi73bYWusQjQRgqQGXK260bw&federated_search_session_id=ae03436b-1c5d-417b-9a38-ee6ec4f21131&query=%E5%8F%B0%E5%8C%97%2C%20%E5%8F%B0%E7%81%A3%E5%9C%B0%E5%8D%80&section_offset=3&items_offset=40
#https://www.airbnb.com/s/%E5%8F%B0%E5%8C%97%E5%B8%82/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=pagination&place_id=ChIJi73bYWusQjQRgqQGXK260bw&federated_search_session_id=2ea7cf76-4445-45fa-8b69-007eb6d46a66&query=Taipei%2C%20Taiwan
#https://www.airbnb.com/s/%E5%8F%B0%E5%8C%97%E5%B8%82/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=pagination&place_id=ChIJi73bYWusQjQRgqQGXK260bw&federated_search_session_id=2ea7cf76-4445-45fa-8b69-007eb6d46a66&query=Taipei%2C%20Taiwan&section_offset=3&items_offset=20
for page in range(0,5):
    url = "https://www.airbnb.com/s/%E5%8F%B0%E5%8C%97%E5%B8%82/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=pagination&place_id=ChIJi73bYWusQjQRgqQGXK260bw&federated_search_session_id=2ea7cf76-4445-45fa-8b69-007eb6d46a66&query=Taipei%2C%20Taiwan"
    if page!=0:
        url=url+"&section_offset=3&items_offset="+str(page*20)
    # 解決 400 Error
    try:
        responds = urlopen(url)
    except HTTPError:
        print("已完成，此為最後一頁!!")
        break
    print("頁數:", page+1)
    # 分析盒子
    html = BeautifulSoup(responds)
    # 找盒子
    rlist = html.find_all("div", class_="_8ssblpx")
    for r in rlist:
        list_url = r.find("a", class_="_gjfol0")
        # 取紙條以及特徵
        print(list_url["href"])
        # 建立資料序列
        s = pd.Series([list_url["href"]],
                  index=["url"])
        df = df.append(s, ignore_index=True) # ignore_index= True 重新標號 不保留原本的標號

df.to_csv("list_url.csv", encoding="utf-8", index=False) # index=False 不儲存標號之列表

