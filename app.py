#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 13:25:30 2019

@author: yixizhou
"""

from flask import Flask, render_template, request, redirect
import pandas as pd
import pandas_datareader as pdr 
from pandas import DataFrame
import numpy as np
import bokeh
from bokeh.layouts import gridplot
from bokeh.embed import components 
from bokeh.plotting import figure
from bokeh.io import show
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

def datetime(x):
    return np.array(x, dtype=np.datetime64)

def Tickerlook(Ticker,year,month):
    if month != '12':
        starttime = year+'-'+month+'-01'
        endtime = year+'-'+str(int(month)+1)+'-01'
    else:
        starttime = year+'-'+month+'-01'
        endtime = str(int(year)+1)+'-01-01' 
    df = pdr.DataReader(Ticker,data_source='yahoo',start=starttime,end=endtime)
    p1 = figure(x_axis_type="datetime", title="Stock Closing Prices For"+" "+year+"-"+month)
    p1.grid.grid_line_alpha=0.3
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Price'
    p1.line(datetime(df.index), df['Adj Close'], color='#A6CEE3', legend=Ticker)
    script,div = components(p1)
    return p1

@app.route('/')
def index():
    return render_template('index.html')
 
@app.route("/",methods=['GET','POST'])
def Tickerplot():
    if request.method == 'POST':
        Ticker = request.form['Ticker']
        year = request.form['year']
        month = request.form['month']
        p = Tickerlook(Ticker,year,month)
        script, div = components(p)
        return render_template("index.html", script=script, div=div)

if __name__ == '__main__':
	app.run(debug=True)
