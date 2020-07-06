# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 13:33:04 2020

@author: USER
"""
import flask
from flask import Flask, jsonify, request
import json
import pickle
import pandas as pd
import xgboost as xgb

app = Flask(__name__)

def load_data(i):
    df = pd.read_csv('airbnb_list_val.csv')
    test = xgb.DMatrix(df.iloc[:i])
    return test

def load_models():
    file_name = "airbnb_price_model.pckl"
    with open(file_name, 'rb') as pickled:
        model = pickle.load(pickled)
        #model = data['model']
    return model

@app.route('/predict', methods=['GET'])
def predict():
    # stub input features
    request_json = request.get_json()
    i = int(request_json['input'])
    x = load_data(i)
    # load model
    model = load_models()
    prediction = model.predict(x)[0].item()
    response = json.dumps({'response': prediction})
    return response, 200

if __name__ == "__main__":
    app.run(debug=False)