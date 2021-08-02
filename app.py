
import random
import json as jas
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from flask_cors import CORS, cross_origin
import ast
import requests

import json
import folium 
import requests
import pandas as pd
from branca.element import Figure
from folium.features import DivIcon




app = Flask(__name__)
CORS(app)
model_s = pickle.load(open('regression_model.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))


@app.route('/')
@cross_origin()
def home():
    return render_template('homepage.html')

@app.route('/predict',methods=['POST'])
@cross_origin()
def predict():
    a=request.json
    b=list(a.values())
    print(b)
    
    final_features = [b]
    org=final_features[0][0]
    des=final_features[0][1]
    date=final_features[0][2]
    global o
    o=org
    global d
    d=des
    #w=weight
    da=date
    
    
    global oo
    oo=org
    global dd
    dd=des
    
    date=pd.to_datetime(date)
    year=date.year
    month=date.month
    week=date.week
    day=date.day
    dateweek=date.dayofweek

    
    if o=="Guangzhou":
      delay=0
    elif o=="Qingdao":
      delay=1
    elif o=="LongBeach":
      delay=2
    elif o=="LosAngeles":
      delay=3
    elif o=="NewYork":
      delay=4
    elif o=="Seattle":
      delay=5
    else:
      delay=6
    
    org_dict={'Guangzhou':10,'Ningbo':11,'Qingdao':12,'Shanghai':13,'Shenzhen':14,'Long Beach':15,'Los Angeles':16,'New York':17,'Savannah':18,'Seattle':19,'Busan':20,'Wilmington':21,'Wenzhou':22,'Yokohama':23}
    dest_dict={'Guangzhou':10,'Ningbo':11,'Qingdao':12,'Shanghai':13,'Shenzhen':14,'Long Beach':15,'Los Angeles':16,'New York':17,'Savannah':18,'Seattle':19,'Busan':20,'Wilmington':21,'Wenzhou':22,'Yokohama':23}
    
    distance_dict={'Qingdao|Shanghai': 335, 'Shanghai|Ningbo': 134, 'Ningbo|Wenzhou': 234, 'Wenzhou|Busan': 624, 'Busan|Long Beach': 5254, 'Ningbo|Busan': 506, 'Busan|Los Angeles': 5254, 'Busan|Wilmington': 10098, 'Wilmington|Savannah': 628, 'Savannah|New York': 688, 'Busan|Yokohama': 644, 'Yokohama|Seattle': 4247, 'Guangzhou|Shenzhen': 46, 'Shenzhen|Ningbo': 746, 'Ningbo|Shanghai': 134, 'Shanghai|Busan': 481, 'Shenzhen|Shanghai': 872, 'Seattle|Yokohama': 4247, 'Yokohama|Busan': 644, 'Busan|Shanghai': 481, 'Shanghai|Shenzhen': 872, 'Ningbo|Shenzhen': 746, 'New York|Savannah': 688, 'Savannah|Wilmington': 628, 'Wilmington|Busan': 10098, 'Los Angeles|Busan': 5254, 'Long Beach|Busan': 5254, 'Shenzhen|Guangzhou': 46, 'Busan|Ningbo': 506, 'Busan|Wenzhou': 624, 'Wenzhou|Ningbo': 234, 'Shanghai|Qingdao': 335}
    
    org_dest=str(o)+"|"+str(d)

    result_predicted_Route_One=[]
    result_predicted_Route_Two=[]
    

    df_route=pd.read_csv("https://raw.githubusercontent.com/cozentus-satyabrata/files/main/SplittedRoutes_model_prediction.csv")
    for i in range(len(list(df_route["Routes"]))):
        
        c=str(df_route["Routes"][i])
        res = ast.literal_eval(c)
    
        if (o==res[0] and d==res[-1]):
              routee=res
              xpos=i
    
    print(xpos)
    c_new=(df_route["Routes"][xpos-1])
    res_new= ast.literal_eval(c_new)
    
    
    # predicted output for route 1
    for i in range(len(res_new)-1):
  
        o_num=org_dict[res_new[i]]
        d_num=dest_dict[res_new[i+1]]
        dis_n=distance_dict[str(res_new[i]+"|"+res_new[i+1])]
        route1_res=model_s.predict([[int(o_num),int(d_num),dis_n,year,month,week,day,dateweek,delay]])
        result_predicted_Route_One.append( int(route1_res[0]))

    a=0
    for i in result_predicted_Route_One:
      a=a+i
    print("NO OF PORT CALLS:",len(result_predicted_Route_One))
    portcall_one=len(result_predicted_Route_One)
    print("PREDICTED ETA FOR ROUTE ONE:",a)
    eta_split_one=a
    print(res_new)
    print(routee)
    
    #predicted output for route 2
    for i in range(len(routee)-1):
        # print(res_new[i]+"|"+res_new[i+1],distance_dict[str(res_new[i]+"|"+res_new[i+1])])       
        o_num=org_dict[routee[i]]
        d_num=dest_dict[routee[i+1]]
        dis_n=distance_dict[str(routee[i]+"|"+routee[i+1])]
        print(o_num)
        print(d_num)
        route2_res=model_s.predict([[int(o_num),int(d_num),dis_n,year,month,week,day,dateweek,delay]])
        print(route2_res)
        # result_predicted_Route_Two.append(res_new[i]+"|"+res_new[i+1])
        
        result_predicted_Route_Two.append( int(route2_res[0]))
    az=0
    for g in result_predicted_Route_Two:
        az=az+g
    print("NO OF PORT CALLS ",len(result_predicted_Route_Two))
    portcall_two=len(result_predicted_Route_Two)
    print("PREDICTED ETA FOR ROUTE TWO",az)
    eta_split_two=az

    
    Origin = org
    Destination = des
    Canal_P = 'Panama'
    Canal_C = 'Cape of Good Hope'
    Canal_S = 'Suez'
    p=Canal_P
    q=Canal_C
    t=Canal_S

    #maps old
    df = pd.read_csv("https://raw.githubusercontent.com/cozentus-satyabrata/files/main/Routes_Clean.csv")
    df_new=df.loc[(df['Origin']==o) & (df['Destination']==d) & (df['TradeRoute']==Canal_C)]


    str_P = Origin+"|"+Destination+"|"+Canal_P
    str_C = Origin+"|"+Destination+"|"+Canal_C
    str_S = Origin+"|"+Destination+"|"+Canal_S
    #map_dict={'Guangzhou|Long Beach|Panama': 53, 'Guangzhou|Long Beach|Cape of Good Hope': 53, 'Guangzhou|Long Beach|Suez': 53, 'Guangzhou|Los Angeles|Panama': 53, 'Guangzhou|Los Angeles|Cape of Good Hope': 53, 'Guangzhou|Los Angeles|Suez': 53, 'Guangzhou|New York|Panama': 53, 'Guangzhou|New York|Cape of Good Hope': 53, 'Guangzhou|New York|Suez': 53, 'Guangzhou|Savannah|Panama': 53, 'Guangzhou|Savannah|Cape of Good Hope': 53, 'Guangzhou|Savannah|Suez': 53, 'Guangzhou|Seattle|Panama': 53, 'Guangzhou|Seattle|Cape of Good Hope': 53, 'Guangzhou|Seattle|Suez': 53, 'Ningbo|Long Beach|Panama': 53, 'Ningbo|Long Beach|Cape of Good Hope': 53, 'Ningbo|Long Beach|Suez': 53, 'Ningbo|Los Angeles|Panama': 53, 'Ningbo|Los Angeles|Cape of Good Hope': 53, 'Ningbo|Los Angeles|Suez': 53, 'Ningbo|New York|Panama': 53, 'Ningbo|New York|Cape of Good Hope': 53, 'Ningbo|New York|Suez': 53, 'Ningbo|Savannah|Panama': 53, 'Ningbo|Savannah|Cape of Good Hope': 53, 'Ningbo|Savannah|Suez': 53, 'Ningbo|Seattle|Panama': 53, 'Ningbo|Seattle|Cape of Good Hope': 53, 'Ningbo|Seattle|Suez': 53, 'Qingdao|Long Beach|Panama': 53, 'Qingdao|Long Beach|Cape of Good Hope': 53, 'Qingdao|Long Beach|Suez': 53, 'Qingdao|Los Angeles|Panama': 53, 'Qingdao|Los Angeles|Cape of Good Hope': 53, 'Qingdao|Los Angeles|Suez': 53, 'Qingdao|New York|Panama': 53, 'Qingdao|New York|Cape of Good Hope': 53, 'Qingdao|New York|Suez': 53, 'Qingdao|Savannah|Panama': 53, 'Qingdao|Savannah|Cape of Good Hope': 53, 'Qingdao|Savannah|Suez': 53, 'Qingdao|Seattle|Panama': 53, 'Qingdao|Seattle|Cape of Good Hope': 53, 'Qingdao|Seattle|Suez': 53, 'Shanghai|Long Beach|Panama': 53, 'Shanghai|Long Beach|Cape of Good Hope': 53, 'Shanghai|Long Beach|Suez': 53, 'Shanghai|Los Angeles|Panama': 53, 'Shanghai|Los Angeles|Cape of Good Hope': 53, 'Shanghai|Los Angeles|Suez': 53, 'Shanghai|New York|Panama': 53, 'Shanghai|New York|Cape of Good Hope': 53, 'Shanghai|New York|Suez': 53, 'Shanghai|Savannah|Panama': 53, 'Shanghai|Savannah|Cape of Good Hope': 53, 'Shanghai|Savannah|Suez': 53, 'Shanghai|Seattle|Panama': 53, 'Shanghai|Seattle|Cape of Good Hope': 53, 'Shanghai|Seattle|Suez': 53, 'Shenzhen|Long Beach|Panama': 53, 'Shenzhen|Long Beach|Cape of Good Hope': 53, 'Shenzhen|Long Beach|Suez': 53, 'Shenzhen|Los Angeles|Panama': 53, 'Shenzhen|Los Angeles|Cape of Good Hope': 53, 'Shenzhen|Los Angeles|Suez': 53, 'Shenzhen|New York|Panama': 53, 'Shenzhen|New York|Cape of Good Hope': 53, 'Shenzhen|New York|Suez': 53, 'Shenzhen|Savannah|Panama': 53, 'Shenzhen|Savannah|Cape of Good Hope': 53, 'Shenzhen|Savannah|Suez': 53, 'Shenzhen|Seattle|Panama': 53, 'Shenzhen|Seattle|Cape of Good Hope': 53, 'Shenzhen|Seattle|Suez': 53, 'Long Beach|Guangzhou|Panama': 53, 'Long Beach|Guangzhou|Cape of Good Hope': 53, 'Long Beach|Guangzhou|Suez': 53, 'Long Beach|Ningbo|Panama': 53, 'Long Beach|Ningbo|Cape of Good Hope': 53, 'Long Beach|Ningbo|Suez': 53, 'Long Beach|Qingdao|Panama': 53, 'Long Beach|Qingdao|Cape of Good Hope': 53, 'Long Beach|Qingdao|Suez': 53, 'Long Beach|Shanghai|Panama': 53, 'Long Beach|Shanghai|Cape of Good Hope': 53, 'Long Beach|Shanghai|Suez': 53, 'Long Beach|Shenzhen|Panama': 53, 'Long Beach|Shenzhen|Cape of Good Hope': 53, 'Long Beach|Shenzhen|Suez': 53, 'Los Angeles|Guangzhou|Panama': 53, 'Los Angeles|Guangzhou|Cape of Good Hope': 53, 'Los Angeles|Guangzhou|Suez': 53, 'Los Angeles|Ningbo|Panama': 53, 'Los Angeles|Ningbo|Cape of Good Hope': 53, 'Los Angeles|Ningbo|Suez': 53, 'Los Angeles|Qingdao|Panama': 53, 'Los Angeles|Qingdao|Cape of Good Hope': 53, 'Los Angeles|Qingdao|Suez': 53, 'Los Angeles|Shanghai|Panama': 53, 'Los Angeles|Shanghai|Cape of Good Hope': 53, 'Los Angeles|Shanghai|Suez': 53, 'Los Angeles|Shenzhen|Panama': 53, 'Los Angeles|Shenzhen|Cape of Good Hope': 53, 'Los Angeles|Shenzhen|Suez': 53, 'New York|Guangzhou|Panama': 53, 'New York|Guangzhou|Cape of Good Hope': 53, 'New York|Guangzhou|Suez': 53, 'New York|Ningbo|Panama': 53, 'New York|Ningbo|Cape of Good Hope': 53, 'New York|Ningbo|Suez': 53, 'New York|Qingdao|Panama': 53, 'New York|Qingdao|Cape of Good Hope': 53, 'New York|Qingdao|Suez': 53, 'New York|Shanghai|Panama': 53, 'New York|Shanghai|Cape of Good Hope': 53, 'New York|Shanghai|Suez': 53, 'New York|Shenzhen|Panama': 53, 'New York|Shenzhen|Cape of Good Hope': 53, 'New York|Shenzhen|Suez': 53, 'Savannah|Guangzhou|Panama': 53, 'Savannah|Guangzhou|Cape of Good Hope': 53, 'Savannah|Guangzhou|Suez': 53, 'Savannah|Ningbo|Panama': 53, 'Savannah|Ningbo|Cape of Good Hope': 53, 'Savannah|Ningbo|Suez': 53, 'Savannah|Qingdao|Panama': 53, 'Savannah|Qingdao|Cape of Good Hope': 53, 'Savannah|Qingdao|Suez': 53, 'Savannah|Shanghai|Panama': 53, 'Savannah|Shanghai|Cape of Good Hope': 53, 'Savannah|Shanghai|Suez': 53, 'Savannah|Shenzhen|Panama': 53, 'Savannah|Shenzhen|Cape of Good Hope': 53, 'Savannah|Shenzhen|Suez': 53, 'Seattle|Guangzhou|Panama': 53, 'Seattle|Guangzhou|Cape of Good Hope': 53, 'Seattle|Guangzhou|Suez': 53, 'Seattle|Ningbo|Panama': 53, 'Seattle|Ningbo|Cape of Good Hope': 53, 'Seattle|Ningbo|Suez': 53, 'Seattle|Qingdao|Panama': 53, 'Seattle|Qingdao|Cape of Good Hope': 53, 'Seattle|Qingdao|Suez': 53, 'Seattle|Shanghai|Panama': 53, 'Seattle|Shanghai|Cape of Good Hope': 53, 'Seattle|Shanghai|Suez': 53, 'Seattle|Shenzhen|Panama': 53, 'Seattle|Shenzhen|Cape of Good Hope': 53, 'Seattle|Shenzhen|Suez': 53}
    map_dict={'Guangzhou|Long Beach|Panama': 20, 'Guangzhou|Long Beach|Cape of Good Hope': 52, 'Guangzhou|Long Beach|Suez': 50, 'Guangzhou|Los Angeles|Panama': 20, 'Guangzhou|Los Angeles|Cape of Good Hope': 52, 'Guangzhou|Los Angeles|Suez': 50, 'Guangzhou|New York|Panama': 36, 'Guangzhou|New York|Cape of Good Hope': 43, 'Guangzhou|New York|Suez': 37, 'Guangzhou|Savannah|Panama': 34, 'Guangzhou|Savannah|Cape of Good Hope': 44, 'Guangzhou|Savannah|Suez': 39, 'Guangzhou|Seattle|Panama': 18, 'Guangzhou|Seattle|Cape of Good Hope': 56, 'Guangzhou|Seattle|Suez': 54, 'Ningbo|Long Beach|Panama': 18, 'Ningbo|Long Beach|Cape of Good Hope': 54, 'Ningbo|Long Beach|Suez': 51, 'Ningbo|Los Angeles|Panama': 18, 'Ningbo|Los Angeles|Cape of Good Hope': 54, 'Ningbo|Los Angeles|Suez': 51, 'Ningbo|New York|Panama': 34, 'Ningbo|New York|Cape of Good Hope': 45, 'Ningbo|New York|Suez': 38, 'Ningbo|Savannah|Panama': 32, 'Ningbo|Savannah|Cape of Good Hope': 46, 'Ningbo|Savannah|Suez': 40, 'Ningbo|Seattle|Panama': 16, 'Ningbo|Seattle|Cape of Good Hope': 58, 'Ningbo|Seattle|Suez': 55, 'Qingdao|Long Beach|Panama': 18, 'Qingdao|Long Beach|Cape of Good Hope': 56, 'Qingdao|Long Beach|Suez': 53, 'Qingdao|Los Angeles|Panama': 18, 'Qingdao|Los Angeles|Cape of Good Hope': 56, 'Qingdao|Los Angeles|Suez': 53, 'Qingdao|New York|Panama': 34, 'Qingdao|New York|Cape of Good Hope': 47, 'Qingdao|New York|Suez': 40, 'Qingdao|Savannah|Panama': 32, 'Qingdao|Savannah|Cape of Good Hope': 48, 'Qingdao|Savannah|Suez': 42, 'Qingdao|Seattle|Panama': 16, 'Qingdao|Seattle|Cape of Good Hope': 60, 'Qingdao|Seattle|Suez': 57, 'Shanghai|Long Beach|Panama': 18, 'Shanghai|Long Beach|Cape of Good Hope': 55, 'Shanghai|Long Beach|Suez': 52, 'Shanghai|Los Angeles|Panama': 18, 'Shanghai|Los Angeles|Cape of Good Hope': 55, 'Shanghai|Los Angeles|Suez': 52, 'Shanghai|New York|Panama': 33, 'Shanghai|New York|Cape of Good Hope': 46, 'Shanghai|New York|Suez': 39, 'Shanghai|Savannah|Panama': 32, 'Shanghai|Savannah|Cape of Good Hope': 47, 'Shanghai|Savannah|Suez': 41, 'Shanghai|Seattle|Panama': 16, 'Shanghai|Seattle|Cape of Good Hope': 59, 'Shanghai|Seattle|Suez': 56, 'Shenzhen|Long Beach|Panama': 20, 'Shenzhen|Long Beach|Cape of Good Hope': 52, 'Shenzhen|Long Beach|Suez': 49, 'Shenzhen|Los Angeles|Panama': 20, 'Shenzhen|Los Angeles|Cape of Good Hope': 52, 'Shenzhen|Los Angeles|Suez': 49, 'Shenzhen|New York|Panama': 36, 'Shenzhen|New York|Cape of Good Hope': 43, 'Shenzhen|New York|Suez': 36, 'Shenzhen|Savannah|Panama': 34, 'Shenzhen|Savannah|Cape of Good Hope': 44, 'Shenzhen|Savannah|Suez': 38, 'Shenzhen|Seattle|Panama': 18, 'Shenzhen|Seattle|Cape of Good Hope': 56, 'Shenzhen|Seattle|Suez': 53, 'Long Beach|Guangzhou|Panama': 20, 'Long Beach|Guangzhou|Cape of Good Hope': 52, 'Long Beach|Guangzhou|Suez': 50, 'Long Beach|Ningbo|Panama': 18, 'Long Beach|Ningbo|Cape of Good Hope': 54, 'Long Beach|Ningbo|Suez': 51, 'Long Beach|Qingdao|Panama': 18, 'Long Beach|Qingdao|Cape of Good Hope': 56, 'Long Beach|Qingdao|Suez': 53, 'Long Beach|Shanghai|Panama': 18, 'Long Beach|Shanghai|Cape of Good Hope': 55, 'Long Beach|Shanghai|Suez': 52, 'Long Beach|Shenzhen|Panama': 20, 'Long Beach|Shenzhen|Cape of Good Hope': 52, 'Long Beach|Shenzhen|Suez': 49, 'Los Angeles|Guangzhou|Panama': 20, 'Los Angeles|Guangzhou|Cape of Good Hope': 52, 'Los Angeles|Guangzhou|Suez': 50, 'Los Angeles|Ningbo|Panama': 18, 'Los Angeles|Ningbo|Cape of Good Hope': 54, 'Los Angeles|Ningbo|Suez': 51, 'Los Angeles|Qingdao|Panama': 18, 'Los Angeles|Qingdao|Cape of Good Hope': 56, 'Los Angeles|Qingdao|Suez': 53, 'Los Angeles|Shanghai|Panama': 18, 'Los Angeles|Shanghai|Cape of Good Hope': 55, 'Los Angeles|Shanghai|Suez': 52, 'Los Angeles|Shenzhen|Panama': 20, 'Los Angeles|Shenzhen|Cape of Good Hope': 52, 'Los Angeles|Shenzhen|Suez': 49, 'New York|Guangzhou|Panama': 36, 'New York|Guangzhou|Cape of Good Hope': 43, 'New York|Guangzhou|Suez': 37, 'New York|Ningbo|Panama': 34, 'New York|Ningbo|Cape of Good Hope': 45, 'New York|Ningbo|Suez': 38, 'New York|Qingdao|Panama': 34, 'New York|Qingdao|Cape of Good Hope': 47, 'New York|Qingdao|Suez': 40, 'New York|Shanghai|Panama': 33, 'New York|Shanghai|Cape of Good Hope': 46, 'New York|Shanghai|Suez': 39, 'New York|Shenzhen|Panama': 36, 'New York|Shenzhen|Cape of Good Hope': 43, 'New York|Shenzhen|Suez': 36, 'Savannah|Guangzhou|Panama': 34, 'Savannah|Guangzhou|Cape of Good Hope': 44, 'Savannah|Guangzhou|Suez': 39, 'Savannah|Ningbo|Panama': 32, 'Savannah|Ningbo|Cape of Good Hope': 46, 'Savannah|Ningbo|Suez': 40, 'Savannah|Qingdao|Panama': 32, 'Savannah|Qingdao|Cape of Good Hope': 48, 'Savannah|Qingdao|Suez': 42, 'Savannah|Shanghai|Panama': 32, 'Savannah|Shanghai|Cape of Good Hope': 47, 'Savannah|Shanghai|Suez': 41, 'Savannah|Shenzhen|Panama': 34, 'Savannah|Shenzhen|Cape of Good Hope': 44, 'Savannah|Shenzhen|Suez': 38, 'Seattle|Guangzhou|Panama': 18, 'Seattle|Guangzhou|Cape of Good Hope': 56, 'Seattle|Guangzhou|Suez': 54, 'Seattle|Ningbo|Panama': 16, 'Seattle|Ningbo|Cape of Good Hope': 58, 'Seattle|Ningbo|Suez': 55, 'Seattle|Qingdao|Panama': 16, 'Seattle|Qingdao|Cape of Good Hope': 60, 'Seattle|Qingdao|Suez': 57, 'Seattle|Shanghai|Panama': 16, 'Seattle|Shanghai|Cape of Good Hope': 59, 'Seattle|Shanghai|Suez': 56, 'Seattle|Shenzhen|Panama': 18, 'Seattle|Shenzhen|Cape of Good Hope': 56, 'Seattle|Shenzhen|Suez': 53}
    this_dict = {('Shenzhen|New York|Cape of Good Hope'):(13771.24929),
    ('Guangzhou|New York|Cape of Good Hope'):(13801.1163),
    ('New York|Shenzhen|Cape of Good Hope'):(13771.24929),
    ('New York|Guangzhou|Cape of Good Hope'):(13801.1163),
    ('Savannah|Guangzhou|Cape of Good Hope'):(13843.77501),
    ('Shenzhen|Savannah|Cape of Good Hope'):(13813.908),
    ('Guangzhou|Savannah|Cape of Good Hope'):(13843.77501),
    ('Savannah|Shenzhen|Cape of Good Hope'):(13813.908),
    ('New York|Ningbo|Cape of Good Hope'):(14426.54367),
    ('Ningbo|New York|Cape of Good Hope'):(14426.54367),
    ('New York|Shanghai|Cape of Good Hope'):(14493.10262),
    ('Shanghai|New York|Cape of Good Hope'):(14493.10262),
    ('Ningbo|Savannah|Cape of Good Hope'):(14469.20238),
    ('Savannah|Ningbo|Cape of Good Hope'):(14469.20238),
    ('Savannah|Shanghai|Cape of Good Hope'):(14535.76134),
    ('Qingdao|New York|Cape of Good Hope'):(14765.90819),
    ('New York|Qingdao|Cape of Good Hope'):(14765.90819),
    ('Shanghai|Savannah|Cape of Good Hope'):(14535.76134),
    ('Qingdao|Savannah|Cape of Good Hope'):(14808.5669),
    ('Savannah|Qingdao|Cape of Good Hope'):(14808.5669),
    ('Guangzhou|Long Beach|Cape of Good Hope'):(16393.3512),
    ('Long Beach|Shenzhen|Cape of Good Hope'):(16363.4842),
    ('Los Angeles|Guangzhou|Cape of Good Hope'):(16400.04171),
    ('Shenzhen|Long Beach|Cape of Good Hope'):(16363.4842),
    ('Guangzhou|Los Angeles|Cape of Good Hope'):(16400.04171),
    ('Shenzhen|Los Angeles|Cape of Good Hope'):(16370.1747),
    ('Long Beach|Guangzhou|Cape of Good Hope'):(16393.3512),
    ('Los Angeles|Shenzhen|Cape of Good Hope'):(16370.1747),
    ('Ningbo|Long Beach|Cape of Good Hope'):(17018.77858),
    ('Long Beach|Ningbo|Cape of Good Hope'):(17018.77858),
    ('Ningbo|Los Angeles|Cape of Good Hope'):(17025.46908),
    ('Los Angeles|Ningbo|Cape of Good Hope'):(17025.46908),
    ('Long Beach|Shanghai|Cape of Good Hope'):(17085.33753),
    ('Los Angeles|Shanghai|Cape of Good Hope'):(17092.02804),
    ('Shanghai|Long Beach|Cape of Good Hope'):(17085.33753),
    ('Shanghai|Los Angeles|Cape of Good Hope'):(17092.02804),
    ('Seattle|Shenzhen|Cape of Good Hope'):(17488.85128),
    ('Los Angeles|Qingdao|Cape of Good Hope'):(17364.8336),
    ('Qingdao|Long Beach|Cape of Good Hope'):(17358.1431),
    ('Seattle|Guangzhou|Cape of Good Hope'):(17518.71829),
    ('Long Beach|Qingdao|Cape of Good Hope'):(17358.1431),
    ('Guangzhou|Seattle|Cape of Good Hope'):(17518.71829),
    ('Qingdao|Los Angeles|Cape of Good Hope'):(17364.8336),
    ('Shenzhen|Seattle|Cape of Good Hope'):(17488.85128),
    ('Ningbo|Seattle|Cape of Good Hope'):(18144.14566),
    ('Seattle|Ningbo|Cape of Good Hope'):(18144.14566),
    ('Seattle|Shanghai|Cape of Good Hope'):(18210.70462),
    ('Shanghai|Seattle|Cape of Good Hope'):(18210.70462),
    ('Seattle|Qingdao|Cape of Good Hope'):(18483.51018),
    ('Qingdao|Seattle|Cape of Good Hope'):(18483.51018),
    ('Ningbo|Seattle|Panama'):(5089.262209),
    ('Seattle|Ningbo|Panama'):(5089.262209),
    ('Seattle|Qingdao|Panama'):(5090.144791),
    ('Shanghai|Seattle|Panama'):(5065.038384),
    ('Seattle|Shanghai|Panama'):(5065.038384),
    ('Qingdao|Seattle|Panama'):(5090.144791),
    ('Los Angeles|Shanghai|Panama'):(5710.011498),
    ('Qingdao|Los Angeles|Panama'):(5735.117905),
    ('Shanghai|Long Beach|Panama'):(5710.073692),
    ('Guangzhou|Seattle|Panama'):(5800.010721),
    ('Seattle|Guangzhou|Panama'):(5800.010721),
    ('Seattle|Shenzhen|Panama'):(5755.901055),
    ('Los Angeles|Qingdao|Panama'):(5735.117905),
    ('Long Beach|Shanghai|Panama'):(5710.073692),
    ('Long Beach|Ningbo|Panama'):(5734.297517),
    ('Shenzhen|Seattle|Panama'):(5755.901055),
    ('Long Beach|Qingdao|Panama'):(5735.180099),
    ('Qingdao|Long Beach|Panama'):(5735.180099),
    ('Los Angeles|Ningbo|Panama'):(5734.235323),
    ('Ningbo|Long Beach|Panama'):(5734.297517),
    ('Ningbo|Los Angeles|Panama'):(5734.235323),
    ('Shanghai|Los Angeles|Panama'):(5710.011498),
    ('Shenzhen|Los Angeles|Panama'):(6400.874169),
    ('Guangzhou|Long Beach|Panama'):(6445.04603),
    ('Long Beach|Guangzhou|Panama'):(6445.04603),
    ('Los Angeles|Guangzhou|Panama'):(6444.983836),
    ('Shenzhen|Long Beach|Panama'):(6400.936363),
    ('Long Beach|Shenzhen|Panama'):(6400.936363),
    ('Guangzhou|Los Angeles|Panama'):(6444.983836),
    ('Los Angeles|Shenzhen|Panama'):(6400.874169),
    ('Ningbo|Savannah|Panama'):(10204.87953),
    ('Savannah|Qingdao|Panama'):(10205.76212),
    ('Savannah|Ningbo|Panama'):(10204.87953),
    ('Qingdao|Savannah|Panama'):(10205.76212),
    ('Savannah|Shanghai|Panama'):(10180.65571),
    ('Shanghai|Savannah|Panama'):(10180.65571),
    ('New York|Shanghai|Panama'):(10602.20874),
    ('Shanghai|New York|Panama'):(10602.20874),
    ('Savannah|Guangzhou|Panama'):(10899.65958),
    ('Ningbo|New York|Panama'):(10626.43256),
    ('Qingdao|New York|Panama'):(10627.31514),
    ('New York|Ningbo|Panama'):(10626.43256),
    ('Guangzhou|Savannah|Panama'):(10899.65958),
    ('Savannah|Shenzhen|Panama'):(10855.54991),
    ('New York|Qingdao|Panama'):(10627.31514),
    ('Shenzhen|Savannah|Panama'):(10855.54991),
    ('Guangzhou|New York|Panama'):(11321.2126),
    ('New York|Guangzhou|Panama'):(11321.2126),
    ('New York|Shenzhen|Panama'):(11277.10294),
    ('Shenzhen|New York|Panama'):(11277.10294),
    ('New York|Shenzhen|Suez'):(11570.97291),
    ('Shenzhen|New York|Suez'):(11570.97291),
    ('Guangzhou|New York|Suez'):(11600.83992),
    ('New York|Guangzhou|Suez'):(11600.83992),
    ('Savannah|Shenzhen|Suez'):(12053.96275),
    ('New York|Ningbo|Suez'):(12250.28227),
    ('Ningbo|New York|Suez'):(12250.28227),
    ('Shenzhen|Savannah|Suez'):(12053.96275),
    ('Shanghai|New York|Suez'):(12316.84122),
    ('New York|Shanghai|Suez'):(12316.84122),
    ('Savannah|Guangzhou|Suez'):(12083.82976),
    ('Guangzhou|Savannah|Suez'):(12083.82976),
    ('Qingdao|New York|Suez'):(12589.46032),
    ('New York|Qingdao|Suez'):(12589.46032),
    ('Ningbo|Savannah|Suez'):(12733.27211),
    ('Savannah|Ningbo|Suez'):(12733.27211),
    ('Savannah|Shanghai|Suez'):(12799.83106),
    ('Shanghai|Savannah|Suez'):(12799.83106),
    ('Savannah|Qingdao|Suez'):(13072.45016),
    ('Qingdao|Savannah|Suez'):(13072.45016),
    ('Shenzhen|Long Beach|Suez'):(15683.8866),
    ('Los Angeles|Shenzhen|Suez'):(15690.57711),
    ('Long Beach|Shenzhen|Suez'):(15683.8866),
    ('Guangzhou|Los Angeles|Suez'):(15720.44412),
    ('Long Beach|Guangzhou|Suez'):(15713.75361),
    ('Guangzhou|Long Beach|Suez'):(15713.75361),
    ('Shenzhen|Los Angeles|Suez'):(15690.57711),
    ('Los Angeles|Guangzhou|Suez'):(15720.44412),
    ('Long Beach|Ningbo|Suez'):(16363.19596),
    ('Ningbo|Los Angeles|Suez'):(16369.88647),
    ('Los Angeles|Ningbo|Suez'):(16369.88647),
    ('Ningbo|Long Beach|Suez'):(16363.19596),
    ('Long Beach|Shanghai|Suez'):(16429.75492),
    ('Shanghai|Los Angeles|Suez'):(16436.44542),
    ('Shanghai|Long Beach|Suez'):(16429.75492),
    ('Los Angeles|Shanghai|Suez'):(16436.44542),
    ('Shenzhen|Seattle|Suez'):(16809.25369),
    ('Los Angeles|Qingdao|Suez'):(16709.06452),
    ('Seattle|Shenzhen|Suez'):(16809.25369),
    ('Qingdao|Los Angeles|Suez'):(16709.06452),
    ('Long Beach|Qingdao|Suez'):(16702.37402),
    ('Qingdao|Long Beach|Suez'):(16702.37402),
    ('Seattle|Guangzhou|Suez'):(16839.1207),
    ('Guangzhou|Seattle|Suez'):(16839.1207),
    ('Ningbo|Seattle|Suez'):(17488.56305),
    ('Seattle|Ningbo|Suez'):(17488.56305),
    ('Shanghai|Seattle|Suez'):(17555.122),
    ('Seattle|Shanghai|Suez'):(17555.122),
    ('Qingdao|Seattle|Suez'):(17827.74111),
    ('Seattle|Qingdao|Suez'):(17827.74111)
    }
    

    
    a_P=this_dict[str_P]  
    a_C=this_dict[str_C]
    a_S=this_dict[str_S]
    
    
    CE_P=3*int(a_P)
    CE_C=3*int(a_C)
    CE_S=3*int(a_S)
    f_P=map_dict[str_P]
    f_C=map_dict[str_C]
    f_S=map_dict[str_S]
    
    CS_P=random.randrange(2000,3000)
    CS_C=random.randrange(2045,2956)
    CS_S=random.randrange(2090,2999)
    
    
    PR_P=98
    PR_C=98
    PR_S=98

    
    if org=='Guangzhou':
    	org=10
    elif org=='Ningbo':
    	org=11
    elif org=='Qingdao':
    	org=12
    elif org=='Shanghai':
    	org=13
    elif org=='Shenzhen':
    	org=14
    elif org=='Long Beach':
    	org=15
    elif org=='Los Angeles':
    	org=16
    elif org=='New York':
    	org=17
    elif org=='Savannah':
    	org=18
    elif org=='Seattle':
    	org=19
        
        
    if des=='Guangzhou':
    	des=10
    elif des=='Ningbo':
    	des=11
    elif des=='Qingdao':
    	des=12
    elif des=='Shanghai':
    	des=13
    elif des=='Shenzhen':
    	des=14
    elif des=='Long Beach':
    	des=15
    elif des=='Los Angeles':
    	des=16
    elif des=='New York':
    	des=17
    elif des=='Savannah':
    	des=18
    elif des=='Seattle':
    	des=19
        
    
    sh=random.randrange(1,18)
    if (sh==1 or sh==3 or sh==5 or sh==7 or sh==9 or sh==11) :
        SH_F='Maersk'
    elif (sh==2 or sh==4 or sh==6 or sh==8 or sh==10 or sh==12):
        SH_F='XPO'
    else:
        SH_F='HPL'
        
    sh=random.randrange(1,18)
    if (sh==1 or sh==3 or sh==5 or sh==7 or sh==9 or sh==11) :
        SH_S='Maersk'
    elif (sh==2 or sh==4 or sh==6 or sh==8 or sh==10 or sh==12):
        SH_S='XPO'
    else:
        SH_S='HPL'
        
        
    sh=random.randrange(1,18)
    if (sh==1 or sh==3 or sh==5 or sh==7 or sh==9 or sh==11) :
        SH_T='Maersk'
    elif (sh==2 or sh==4 or sh==6 or sh==8 or sh==10 or sh==12):
        SH_T='XPO'
    else:
        SH_T='HPL'
        
        
        
    OR=int(org)
    DS=int(des)
    DI_P=float(a_P)
    DI_C=float(a_C)
    DI_S=float(a_S)
    #TR=int(trade)
    YR=int(year)
    MN=int(month)
    WE=int(week)
    DA=int(day)
    DW=int(dateweek)
    #WE=float(weight)
    
    
    
    TR_P=int(4)
    list_P=[OR,DS,DI_P,TR_P,YR,MN,WE,DA,DW]
    TR_C=int(5)
    list_C=[OR,DS,DI_C,TR_C,YR,MN,WE,DA,DW]
    TR_S=int(6)
    list_S=[OR,DS,DI_S,TR_S,YR,MN,WE,DA,DW]


    final_features_P = [np.array(list_P)]
    final_features_C = [np.array(list_C)]
    final_features_S = [np.array(list_S)]
    
    prediction_P = model.predict(final_features_P)
    prediction_C = model.predict(final_features_C)
    prediction_S = model.predict(final_features_S)
    output_P = int(prediction_P[0])
    output_C = int(prediction_C[0])
    output_S = int(prediction_S[0])

    # url = 'https://raw.githubusercontent.com/cozentus-satyabrata/coz/master/data.csv'
    df = pd.read_csv("https://raw.githubusercontent.com/cozentus-satyabrata/files/main/data.csv")
    df["StDate"]=pd.to_datetime(df["StDate"])
    df["ETA"]=pd.to_datetime(df["ETA"])
    df["ATA"]=pd.to_datetime(df["ATA"])
    
    df['ETA_DI'] = abs(df['StDate'] - df['ETA'])
    df['ATA_DI'] = abs(df['StDate'] - df['ATA'])
    df['ETA_T']=df['ETA_DI']/np.timedelta64(1,'h')
    df['ATA_T']=df['ATA_DI']/np.timedelta64(1,'h')
    df["ETA_D"]=df["ETA_T"]/24
    df["ATA_D"]=df["ATA_T"]/24
    df=df.drop(['ETA_DI', 'ATA_DI' ,'ETA_T','ATA_T'], axis = 1)
    df["ETA_D"]=df["ETA_D"].round(2)
    df["ATA_D"]=df["ATA_D"].round(2)
    df["ETA_D_INT"]=df["ETA_D"].astype(int)
    df["ATA_D_INT"]=df["ATA_D"].astype(int)
    # print(df)
 
    df_new_P=df[(df['Origin']==o) & (df["Destination"]==d) & (df['TradeRoute'] == Canal_P)  & ((df['ATA_D_INT'] == output_P+1) | (df['ATA_D_INT'] == output_P-1) | (df['ATA_D_INT'] == output_P)) ]
    df_new_C=df[(df['Origin']==o) & (df["Destination"]==d) & (df['TradeRoute'] == Canal_C)  & ((df['ATA_D_INT'] == output_C+1) | (df['ATA_D_INT'] == output_C-1) | (df['ATA_D_INT'] == output_C)) ]
    df_new_S=df[(df['Origin']==o) & (df["Destination"]==d) & (df['TradeRoute'] == Canal_S)  & ((df['ATA_D_INT'] == output_S+1) | (df['ATA_D_INT'] == output_S-1) | (df['ATA_D_INT'] == output_S)) ]
    a_PC=df_new_P.shape[0]
    a_CC=df_new_C.shape[0]
    a_SC=df_new_S.shape[0]
    p_PC=round(100*round(1/a_PC, 3),2)
    p_CC=round(100*round(1/a_CC, 3),2)
    p_SC=round(100*round(1/a_SC, 3),2)
    
    #map generation of individual for route1
    df = pd.read_csv(r"https://raw.githubusercontent.com/cozentus-satyabrata/files/main/ROUTE_LAT_LON_COMBINED_ULTIMATE.csv")
    lat_new=[]
    lon_new=[]
    lon_new_=[]
    
    df_i=pd.read_csv("https://raw.githubusercontent.com/cozentus-satyabrata/files/main/experiment_Data_new_new.csv")
    points=[]
    data = pd.DataFrame( columns = ['Origin','Destination','lat','lon'])
       
    
    
    
    for i in range(len(list(df["Routes"]))):
        c=str(df["Routes"][i])
        res = ast.literal_eval(c) 
        if (o==res[0] and d==res[-1]):
            routee=res
            xpos=i
    
    
    c_new=(df["Routes"][xpos-1])
    res_new= ast.literal_eval(c_new)       
    
   
    
    


    
    
    
    
    Canal_P = 'Panama'
    Canal_C = 'Cape of Good Hope'
    Canal_S = 'Suez'
    p=Canal_P
    q=Canal_C
    t=Canal_S

    
    dataRow ={'originPort':[oo,oo,oo],'destinationPort':[d,d,d],'startDate':[da,da,da],'predictedEta':[eta_split_one,eta_split_two,output_S],'tradeLaneURl': ["" , "",""],'tradeLaneName':['Panama','Panama','Suez'],'portCalls':[5,6,0],'Probablity':[int(PR_P),int(PR_C),int(PR_S)],'ETA':[50,int(f_C),int(f_S)],'Diff':[abs(eta_split_one-50),abs(eta_split_two-45),abs(output_S-int(f_S))],'carbonEmission':[CE_P,CE_C,CE_S],'shippingCost':[CS_P,CS_C,CS_S],'shippingLine':[SH_F,SH_S,SH_T]}
    respone=jsonify(result=dataRow)
    respone.status_code=200
    #print(f_P)
    return respone

    
    

if __name__ == "__main__":
    app.run(debug=False)
    
