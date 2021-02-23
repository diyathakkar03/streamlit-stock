import pandas as pd 
import numpy as np 
import requests 
import json
import re
import datetime
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from PIL import Image
import time 
import random 
from plotly.subplots import make_subplots
all_links = {"balance sheet": "https://financialmodelingprep.com/api/v3/balance-sheet-statement/{}?period=quarter&limit=400&apikey=da58bd9052194c551bbe95498876fda0",
            "income statement":"https://financialmodelingprep.com/api/v3/income-statement/{}?period=quarter&limit=400&apikey=da58bd9052194c551bbe95498876fda0",
            "financial ratios":"https://financialmodelingprep.com/api/v3/ratios/{}?period=quarter&limit=140&apikey=da58bd9052194c551bbe95498876fda0", 
            "stock symbol":'https://financialmodelingprep.com/api/v3/stock/list?apikey=da58bd9052194c551bbe95498876fda0',
            "live price": 'https://financialmodelingprep.com/api/v3/quote-short/{}?apikey=da58bd9052194c551bbe95498876fda0',
            "min stock": "https://financialmodelingprep.com/api/v3/historical-chart/1min/{}?apikey=da58bd9052194c551bbe95498876fda0"}


# Streamlit app 

placeholder = st.empty()
start_button = st.empty()
  

ticker = 'AAPL'
def live_data(ticker):
    df = pd.json_normalize(requests.get(all_links['min stock'].format(ticker)).json())
    df = df.iloc[:520].iloc[::-1]
    df['M_20'] = df.close.rolling(20).mean()
    df['M_50'] = df.close.rolling(50).mean()
    #df = df.loc[:500,['date', 'open', 'volume']]
    return df.iloc[::-1]

def graph(df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Candlestick(x = df.date, open = df['open'], 
                                  high = df['high'], low = df['low'],
                                  close = df['close'], name = '%s'%ticker), row = 1, col = 1, secondary_y = False)
    fig.add_trace(go.Scatter(x=df.date, y=df.M_20, line=dict(color='blue', width=1), name = 'MA 20m'), row = 1, col = 1)
    fig.add_trace(go.Scatter(x=df.date, y=df.M_50, line=dict(color='red', width=1), name = 'MA 50m'), row = 1, col = 1)
    fig.add_trace(go.Bar(x=df.date, y=df.volume, name = 'Volume'), row = 1, col = 1, secondary_y = True)


    fig.update_layout(title = 'Live Data %s'%ticker, yaxis_title = 'Price in USD $')
    #fig.update_xaxes(matches = 'x')

    fig.update_xaxes(rangeslider_visible = True,rangeselector = dict(
        buttons = list([
            dict(count = 15, label = '15m', step = 'minute', stepmode = 'backward'),
            dict(count = 45, label = '45m', step = 'minute', stepmode = 'backward'),
            dict(count = 1, label = 'HTD', step = 'hour', stepmode = 'backward'),
            dict(count = 3, label = '3h', step = 'minute', stepmode = 'backward'),
            dict(step = 'all')])))
    fig.update_yaxes(title_text="In US $", secondary_y=False)
    fig.update_yaxes(title_text="Volume", secondary_y=True)

    return placeholder.write(fig)


  
if start_button.button('Start',key='start'):
    start_button.empty()
    if st.button('Stop',key='stop'):
        pass
    while True:
        graph(live_data(ticker))
        time.sleep(5)
        


# You can try to add the volume graph as well but in a different subplot 
#fig.add_trace(go.Bar(x=df.date, y=df.volume, name = 'Volume'), row = 2, col = 1)
