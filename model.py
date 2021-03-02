# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 20:19:42 2021

@author: HP
"""

# Importing the libraries
import numpy as np
import pandas as pd
import pickle

df=pd.read_excel("US_CHN_Transaction_Company_Data_Time_V1.3.1.xlsx")
df["StDate"]=pd.to_datetime(df["StDate"])
df['ETA_DI'] = abs(df['StDate'] - df['ETA'])
df['ATA_DI'] = abs(df['StDate'] - df['ATA'])
df['ETA_T']=df['ETA_DI']/np.timedelta64(1,'h')
df['ATA_T']=df['ATA_DI']/np.timedelta64(1,'h')
df["ETA_D"]=df["ETA_T"]/24
df["ATA_D"]=df["ATA_T"]/24
df=df.drop(['ETA_DI', 'ATA_DI' ,'ETA_T','ATA_T'], axis = 1)
df["ETA_D"]=df["ETA_D"].round(2)
df["ATA_D"]=df["ATA_D"].round(2)
df["ADDN_TIME_TAKEN"]=abs(df["ETA_D"]-df["ATA_D"])
df["ADDN_TIME_TAKEN"]=df["ADDN_TIME_TAKEN"].round(2)

df['StDateyear'] = df['StDate'].dt.year
df['StDatemonth'] = df['StDate'].dt.month
df['StDateweek'] = df['StDate'].dt.week
df['StDateday'] = df['StDate'].dt.day
df['StDatehour'] = df['StDate'].dt.hour
df['StDateminute'] = df['StDate'].dt.minute
df['StDatedayofweek'] = df['StDate'].dt.dayofweek


df['ATA_year'] = df['ATA'].dt.year
df['ATA_month'] = df['ATA'].dt.month
df['ATA_week'] = df['ATA'].dt.week
df['ATA_day'] = df['ATA'].dt.day
df['ATA_hour'] = df['ATA'].dt.hour
df['ATA_minute'] = df['ATA'].dt.minute
df['ATA_dayofweek'] = df['ATA'].dt.dayofweek


# =============================================================================
# 'ADDN_TIME_TAKEN'
# =============================================================================

X = df[[ 'Origin', 'Destination', 'Distance', 'TradeRoute'  , 'StDateyear','StDatemonth',
      'StDateweek', 'StDateday','StDatedayofweek']]
y = df['ATA_D']

#Converting words to integer values
# =============================================================================
# def convert_to_int_Company(word):
#     word_dict = {'Maersk':1, 'XPO Logistics':2, 'HPL':3}
#     return word_dict[word]
# =============================================================================

def convert_to_int_Destination_Origin(word):
    word_dict = {'Guangzhou':10, 'Ningbo':11, 'Qingdao':12, 'Shanghai':13, 'Shenzhen':14,
                'Long Beach':15, 'Los Angeles':.16, 'New York':17, 'Savannah':18, 'Seattle':19}
    return word_dict[word]

def convert_to_int_TradeRoute(word):
    word_dict = {'Panama':4, 'Cape of Good Hope':5, 'Suez':6}
    return word_dict[word]



X['Origin'] = X['Origin'].apply(lambda x : convert_to_int_Destination_Origin(x))
X['Destination'] = X['Destination'].apply(lambda x : convert_to_int_Destination_Origin(x))
X['TradeRoute'] = X['TradeRoute'].apply(lambda x : convert_to_int_TradeRoute(x))
# =============================================================================
# X['Company'] = X['Company'].apply(lambda x : convert_to_int_Company(x))
# 
# =============================================================================

#Splitting Training and Test Set
#Since we have a very small dataset, we will train our model with all availabe data.


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33,shuffle=False)

from sklearn.linear_model import LinearRegression 
from sklearn.metrics import r2_score

clf = LinearRegression(normalize=True)


#Fitting model with trainig data
clf.fit(X_train,y_train)

print("R2 SCORE OF TRAIN DATASET:{}".format(clf.score(X_train,y_train)))
# Saving model to disk
# =============================================================================
pickle.dump(clf, open('model.pkl','wb'))
# 
# # Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))
print(model.predict([[10,17,11600.84,6,2015,1,4,23,4]]))
# =============================================================================
