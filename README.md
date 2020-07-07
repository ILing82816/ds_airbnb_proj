# Data Science Airbnb Price Estimator: Project Overview
* Created a tool that estimates data science house rent price (MAE ~$1) to help host realize house rent in the future when they want to participate Airbnb.
* Scraped over 1000 house descriptions from airbnb using python and beautifulsoup
* Engineered features from categorical objects to encode by using CatBoost Encoding, and from the customers review of each house to quantify the value house.
* Optimized Linear Regression, Random Forest, and XGBoost tuning parameters to reach the best model.
* Displyed a variable importance using shap.
* Built a client facing API using flask

## Code and Resources Used
**Python Version:** 3.7  
**Packages:** urllib, bs4, pandas, numpy, category_encoders, vaderSentiment, sklearn, xgboost, shap, matplotlib, seaborn, flask, json, pickle  
**For Web Framework Requirements:** `pip install -r requirements.txt`    
**Flask Productionization:** https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2  

## Web Scraping
built up a web scarper by using beautifulsoup to scrape 1000 house postings from airbnb.com. With each house, we got the following:
* Name
* Location
* Type of room
* Amenities
* Review
* Price

## Data Cleaning
After scraping the data, I needed to clean it up so that it was usable for our model. I made the following changes and created the following variables:
* Parsed location out of house text
* Made columns for host provided how many room, beds, and baths
* Made a new column for the capacity of house 
* Parsed numeric data out of price
* Add column for the review sentiment analysis
* Add column for encoding the categorical objects, Location and Type of room.  

## EDA
I looked at the distributions of the data and the value counts for the various categorical variables. Below are a few highlights from the pivot tables.
![alt text](https://github.com/ILing82816/ds_oil_price_proj/blob/master/Figure/distribution_wti_price.png "distribution")  
Autocorrelation of WTI Price: There are AR(3)
![alt text](https://github.com/ILing82816/ds_oil_price_proj/blob/master/Figure/ACF_PACF.png "ACF")  
Correlation with other features:
![alt text](https://github.com/ILing82816/ds_oil_price_proj/blob/master/Figure/Features_corr.png "correlation")  

## Model Building
First, I normalized the data. I also split the data into train and tests sets with a test size of 20%.  
I tried three different models and evaluated them using Mean Absolute Error. I chose MAE because it is relatively easy to interpret and outliers aren’t particularly bad in for this type of model.  
I tried three different models:  
* **Linear Regression** - Baseline for the model
* **Long Short-term Memory (LSTM)** - Because the history of oil price would affect current oil price, I thought a memorable model like long short-term memory would be effective.
* **Prophet** - Again, with the time series data, I thought that this would be a good fit. Also, prophet can predict not only one period but more.   

## Model performance
Depend on the trend of oil price in the future, investors decide the strategies of investment. Although the Linear Regression model far outperformed the other approaches on the test and validation sets, the Prophet model is more practical.
* **Prophet:** MAE = 14.56   
![alt text](https://github.com/ILing82816/ds_oil_price_proj/blob/master/Figure/prediction_prophet.png "prophet")   
* **Linear Regression:** MAE = 0.82  
![alt text](https://github.com/ILing82816/ds_oil_price_proj/blob/master/Figure/prediction_linear.png "linear")  
* **Long Short-term Memory (LSTM):** MAE = 1.08  
![alt text](https://github.com/ILing82816/ds_oil_price_proj/blob/master/Figure/prediction_LSTM.png "LSTM")

## Productionization
In this step, I built a flask API endpoint that was hosted on a local webserver by following along with the tutorial in the reference section above. The API endpoint takes in a request with the day of prediction and returns a list of estimated WTI Price.
