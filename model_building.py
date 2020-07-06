# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 10:47:16 2020

@author: USER
"""
import pandas as pd
import os
#path
path_prefix = 'D:/USA 2020 summer/Machine Learning/ds_airbnb_proj'
#Depend on the data eda to take some features.
df = pd.read_csv(os.path.join(path_prefix, 'airbnb_list_EDA.csv'))


# choose relevant columns ["Location", "Rating","Number of review", 'price', 'Capacity',"Bed","Room","Bath","compound"]
df_model = df[["Location", "Rating","Number of review", 'price', 'Capacity',"Bed","Room","Bath","compound"]]
'''
#Label Encoder
from sklearn.preprocessing import LabelEncoder
cat_features = ['Location', 'Room', 'Bath']
encoder = LabelEncoder()
# Apply the label encoder to each column
encoded = df_model[cat_features].apply(encoder.fit_transform)
df_dum = df_model[["Rating","Number of review", 'price', 'Capacity',"Bed","compound"]].join(encoded)
'''

'''
#Count Encoder
import category_encoders as ce
cat_features =  ['Location', 'Room', 'Bath']
# Create the encoder
count_enc = ce.CountEncoder()
# Transform the features, rename the columns with the _count suffix, and join to dataframe
count_encoded = count_enc.fit_transform(df_model[cat_features])
df_model = df_model.join(count_encoded.add_suffix("_count"))
df_dum = df_model.drop(['Location', 'Room', 'Bath'], axis =1)
'''

'''
X = df_dum.drop('price', axis =1)
y = df_dum.price.values

#Normalization
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_vars = scaler.fit_transform(X)

# train test split 
from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(X_vars, y, test_size=0.2)
'''
#Interactions
df_model["Type_of_room"] = df_model['Room'] + "_" + df_model['Bath']
df_model = df_model.drop(['Room', 'Bath'], axis =1)

'''
#CatBoost Encoding
X = df_model.drop('price', axis =1)
y = df_model.price.values
# train test split 
from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

import category_encoders as ce
cat_features =  ['Location', 'Room', 'Bath']
# Create the encoder
target_enc = ce.CatBoostEncoder(cols=cat_features)
target_enc.fit(X_train[cat_features], y_train)

# Transform the features, rename columns with _cb suffix, and join to dataframe
X_train = X_train.join(target_enc.transform(X_train[cat_features]).add_suffix('_cb'))
X_train = X_train.drop(['Location', 'Room', 'Bath'], axis =1)
X_val = X_val.join(target_enc.transform(X_val[cat_features]).add_suffix('_cb'))
X_val = X_val.drop(['Location', 'Room', 'Bath'], axis =1)
'''
#CatBoost Encoding
X = df_model.drop('price', axis =1)
y = df_model.price.values
# train test split 
from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

import category_encoders as ce
cat_features =  ['Location', 'Type_of_room']
# Create the encoder
target_enc = ce.CatBoostEncoder(cols=cat_features)
target_enc.fit(X_train[cat_features], y_train)

# Transform the features, rename columns with _cb suffix, and join to dataframe
X_train = X_train.join(target_enc.transform(X_train[cat_features]).add_suffix('_cb'))
X_train = X_train.drop(['Location', 'Type_of_room'], axis =1)
X_val = X_val.join(target_enc.transform(X_val[cat_features]).add_suffix('_cb'))
X_val = X_val.drop(['Location', 'Type_of_room'], axis =1)



#Multiple linear regression (use mean absolute error to evaluation)
## sklearn Linear Regression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

linear = LinearRegression()
model_linear = linear.fit(X_train, y_train)
print("Linear regression")

y_train_pred = model_linear.predict(X_train)
print(mean_absolute_error(y_train, y_train_pred))

y_val_pred = model_linear.predict(X_val)
print(mean_absolute_error(y_val, y_val_pred))

train_preds = X_train.copy()
train_preds['PRICE'] = y_train
train_preds['price_pred_linear'] = model_linear.predict(X_train)

val_preds = X_val.copy()
val_preds['PRICE'] = y_val
val_preds['price_pred_linear'] = model_linear.predict(X_val)
val_preds['ERROR_linear'] = val_preds['PRICE'] - val_preds['price_pred_linear']

# random forest regressor
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()
model_rf = rf.fit(X_train, y_train)
print("Random Forest")

y_train_pred = model_rf.predict(X_train)
print(mean_absolute_error(y_train, y_train_pred))
y_val_pred = model_rf.predict(X_val)
print(mean_absolute_error(y_val, y_val_pred))

train_preds['price_pred_Rf'] = model_rf.predict(X_train)
val_preds['price_pred_Rf'] = model_rf.predict(X_val)
val_preds['ERROR_Rf'] = val_preds['PRICE'] - val_preds['price_pred_Rf']


#XGBoost 
import xgboost as xgb
xgb_train = xgb.DMatrix(data = X_train, label = y_train)
xgb_val = xgb.DMatrix(data = X_val, label = y_val)

param_xgb = {'booster' : 'gbtree'
           #,'lambda' = ???
           #,'alpha' = ???
           ,'feature_selector' : 'cyclic' #also have 'shuffle', 'random', 'greedy', 'thrifty'
           #, 'top_k' : ??? # only available for greedy and thrifty selector
           , 'objective' : 'reg:squarederror' #also have 'squaredlogerror'
           , 'eval_metric' : 'mae' # also have 'rmsle',
           , 'maximize' : 'FALSE'
        }

watchlist = [(xgb_train, 'train'), (xgb_val, 'eval')]
num_round = 50 #This is another hyperparameter of sorts
xgb_model = xgb.train(param_xgb, xgb_train, num_round, watchlist, early_stopping_rounds = 10)


train_preds['price_pred_xgb'] = xgb_model.predict(xgb_train)
val_preds['price_pred_xgb'] = xgb_model.predict(xgb_val)
val_preds['ERROR_xgb'] = val_preds['PRICE'] - val_preds['price_pred_xgb']

print("XGBoost")
print("Train MAE =", mean_absolute_error(train_preds['PRICE'], train_preds['price_pred_xgb'])
    ,"Val MAE =", mean_absolute_error(val_preds['PRICE'], val_preds['price_pred_xgb']))



#LightGBM
import lightgbm as lgb
lgb_train = lgb.Dataset(X_train, y_train)
lgb_val = lgb.Dataset(X_val, y_val)

lgb_params = {
    'boosting_type': 'gbdt', # also have goss, and dart
    'objective': 'regression',
    'metric': 'mae', # also 'mean_absolute_error', 'mae', 'root_mean_squared_error'
    #'max_depth' : 3,
    #'num_leaves' : ???
    #'learning_rate': 0.1,
    #'num_threads' : -1,
    #'scale_pos_weight' : ???
    'early_stopping_round' : 10,
}

lgb_model = lgb.train(params = lgb_params, train_set = lgb_train,
                num_boost_round = 50, valid_sets = [lgb_val, lgb_train],
               valid_names = ['Evaluation', 'Train'])

train_preds['price_pred_lgb'] = lgb_model.predict(X_train)

val_preds['price_pred_lgb'] = lgb_model.predict(X_val)
print("LightGBM")
print("Train MAE =", mean_absolute_error(train_preds['PRICE'], train_preds['price_pred_lgb'])
    ,"Val MAE =", mean_absolute_error(val_preds['PRICE'], val_preds['price_pred_lgb']))


#model explanation
import shap
model_explainer = shap.TreeExplainer(xgb_model)
shap_vals_train=model_explainer.shap_values(X_train)
shap.summary_plot(shap_vals_train, X_train)
shap_vals_test=model_explainer.shap_values(X_val)
shap.summary_plot(shap_vals_test, X_val)


# flask_API--store the best model
import pickle
with open(os.path.join(path_prefix, 'FlaskApI/airbnb_price_model.pckl'), 'wb') as fout:
    pickle.dump(xgb_model, fout)

X_val.to_csv("airbnb_list_val.csv", index=False)
val_preds.to_csv("airbnb_list_pred.csv", index=False)










