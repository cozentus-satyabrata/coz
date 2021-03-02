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
    url = 'https://raw.githubusercontent.com/cozentus-satyabrata/coz/master/data.csv'
    df = pd.read_csv(url)
    print(df)
    ac=df['Origin'][149]
    
    
    

    return ac


if __name__ == "__main__":
    app.run(debug=False)
