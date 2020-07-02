# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 11:48:25 2020

@author: USER
"""
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

#load data
print("Load Data")
df = pd.read_csv('airbnb_list.csv')

A = df[df["Number of review"].isnull()]
df = df.drop(A.index)
B = df[df["Review"].isnull()]
df = df.drop(B.index)



df["Capacity"] =0
df["Bed"] =0
df["Room"] =0
df["Bath"] =0
for i in df.index:
    #parsing of location
    df["Location"][i]=df["Location"][i].split(" in ")[-1]
    #Capacity
    df["Capacity"][i]=df["Type of room"][i].split("·")[0]
    #Bed
    df["Bed"][i]=df["Type of room"][i].split("·")[2]
    #Room
    df["Room"][i]=df["Type of room"][i].split("·")[1]
    #Bath
    if len(df["Type of room"][i].split("·"))==4:
        df["Bath"][i]=df["Type of room"][i].split("·")[3]
    #parsing of number of review
    df["Number of review"][i]=df["Number of review"][i].split("(")[-1]
    df["Number of review"][i]=df["Number of review"][i].split(")")[0]
    #parsing of price
    df["price"][i]=df["price"][i].split("$")[-1]
    #Review
    df["Review"][i] = df["Review"][i].split("/")[:-2]

#add column for the review sentiment analysis
#Analyzer
analyzer = SentimentIntensityAnalyzer()
#get sentiment scores
sentiment = df['Review'].apply(lambda x: analyzer.polarity_scores(x))
#put sentiment into dataframe
df = pd.concat([df, sentiment.apply(pd.Series)],1)
df_nz = df[df['compound'] != 0]

#Result
df_nz['compound'].sample(500).hist()
plt.title('The Sentiment of Review')
plt.show()


df.to_csv("airbnb_list_clean.csv", index=False) 