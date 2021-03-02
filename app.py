# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 08:52:44 2021

@author: DATeam
"""

import random
import json as jas
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from flask_cors import CORS, cross_origin
#import json
#import folium 
#import requests



app = Flask(__name__)
CORS(app)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
@cross_origin()
def home():
    return render_template('homepage.html')

@app.route('/predict',methods=['POST'])
@cross_origin()
def predict():
#     url = 'https://drive.google.com/file/d/1Gl5hCaXAusU3arqdYZGZSh98K3hoqQuZ/view?usp=sharing'
# #url = 'https://drive.google.com/file/d/0B6GhBwm5vaB2ekdlZW5WZnppb28/view?usp=sharing'
#     path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    df = pd.read_excel('Routes_Clean_New.xlsx')
    ac=df['Origin'][0]
#     ac=df["Origin"][1]
#     #ac=data['Origin'][1]
#     #https://raw.githubusercontent.com/cozentus-satyabrata/herokueta/main/Routes.csv?token=ASYTOAXEBNWGCIAJH2A6TH3AHX2CA
    
    
    #url = 'https://raw.githubusercontent.com/cozentus-satyabrata/herokueta/main/Routes.csv?token=ASYTOAXEBNWGCIAJH2A6TH3AHX2CA'
    #df = pd.read_csv(url,index_col=0)
    
    
    
    

    return ac



if __name__ == "__main__":
    app.run(debug=False)
