# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 15:21:54 2020

@author: USER
"""
import requests

URL = 'http://127.0.0.1:5000/predict'
headers = {"Content-Type": "application/json"}
data = {"input": 1}

r = requests.get(URL,headers=headers, json=data) 

r.json()

