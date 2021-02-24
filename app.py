import pandas as pd 
import numpy as np 
import requests 
import json
import re
import datetime
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
from PIL import Image
import time

# # My module imports
from pyfiles.api_py_fy import api_data
from pyfiles.income_statement import income_statement as inc
from pyfiles.income_statement import min_data as md
from pyfiles.bs_py_fy import balance_sheet as bs
from pyfiles.bs_py_fy import ratios 


# STREAMLIT 
# sidebar image
image = Image.open('sidebarimage.jpg')

st.sidebar.image(image, caption='', use_column_width=True)




st.title('Stocks Analytical Chart App')

## Adding an expandable column for about app
my_expander = st.beta_expander('About App', expanded= False)
with my_expander:
    text = open('text/content.txt', 'r')
    st.write(text.read())



# API links
all_links = {"Balance Sheet": "https://financialmodelingprep.com/api/v3/balance-sheet-statement/{}?period=quarter&limit=400&apikey=da58bd9052194c551bbe95498876fda0",
            "Income Statement":"https://financialmodelingprep.com/api/v3/income-statement/{}?period=quarter&limit=400&apikey=da58bd9052194c551bbe95498876fda0",
            "Financial Ratios":"https://financialmodelingprep.com/api/v3/ratios/{}?period=quarter&limit=140&apikey=da58bd9052194c551bbe95498876fda0", 
            "Stock Symbol":'https://financialmodelingprep.com/api/v3/stock/list?apikey=da58bd9052194c551bbe95498876fda0',
            "Live Price": 'https://financialmodelingprep.com/api/v3/quote-short/{}?apikey=da58bd9052194c551bbe95498876fda0',
            "Live Data": "https://financialmodelingprep.com/api/v3/historical-chart/1min/{}?apikey=da58bd9052194c551bbe95498876fda0"}



st.subheader('Enter the ticker symbol below')
# User input streamlit for any symbol
ticker = st.text_input('','W', key = '1234')

# File contaning ticker symbol and company name
ticker_df = pd.read_csv('tickers.csv')

# Getting the ticker symbol and company name on basis of user input
try:
    ticker_acro = list(ticker_df[ticker_df.symbol == ticker.upper()].name)
    ticker_acro[0]
    st.text('You selected data for %s'%ticker_acro[0])
except IndexError:
    ticker_acro = ticker
    st.text('You selected data for %s'%ticker_acro.upper())


st.sidebar.header('Select the type of financial statement')
add_selectbox = st.sidebar.selectbox('',
    ("Income Statement", "Balance Sheet", "Financial Ratios", 'Live Data'))



# Block for Error Handling user input when sufficent data is not available 
try:
    if add_selectbox == 'Live Data':
        df_1 = api_data(ticker.upper(), all_links, add_selectbox).live_data()
    else:
        col_name = api_data('AAPL', all_links,add_selectbox ).batch_data(data_or_col = 'col')

        st.header('Previous five quarterly financial results')

        df_1 = api_data(ticker.upper(), all_links, add_selectbox).batch_data(col_name = col_name)
except Exception:
    st.error('The ticker symbol is invalid or sufficent data not available')
    st.stop()


if add_selectbox == 'Income Statement':
    df_1 = api_data.bs_is(df_1)
    df_2 = inc(df_1)
    
    # For revenue Plot
    inc.is_df_1(df_2)
    inc.rev_plot(df_2)

    st.subheader('Waterfall Chart')
    option = st.selectbox('Select the Quarterly Result',list(df_2.df['Date']))

    # Waterfall chart
    df_3, index_no = inc.waterfall_df(df_2,date = option)    

    inc.is_waterfall_plot(df_3,index_no = index_no)
    # Rev and Net Income % change plot
    df_4 = inc.pct_df(df_2.df)
    st.subheader('Revenue & Net Income percentage change over previous five quarters')
    inc.rev_income(df_4, ticker_acro[0])

elif add_selectbox == 'Balance Sheet':
    df_1 = api_data.bs_is(df_1)

    df_2 = bs(df_1)
    df_2, df_3 = df_2.bs_df_1()
    
    path_1 = st.selectbox( 'Choose the Portiion of statement to analyze', list(df_2.columns))

    df_3 = bs.con_func(df_2,per_df = df_3)
    bs.bs_plot_1(df_3,row_name = path_1 )

elif add_selectbox == 'Financial Ratios':
    df_3,df_4 = ratios(df_1).ratio_df()
    

    path_3= st.selectbox( 'Choose the Ratio to analyze', list(df_3.columns))

    ratios.ratio_graph(df_3,df_4,col_name=path_3)

elif add_selectbox == 'Live Data':
    st.write("This graphs is for live data. Due to the limited number of API request per day it will stop every 5 seconds. Press Start to see the graph.")
    start_button = st.empty()
    placeholder = st.empty()

    # Block for live data refresh 
    
    if start_button.button('Start',key='start'):
        start_button.empty()
        if st.button('Stop',key='stop'):
            pass
        i = 0
        while True:
            md.plot_1(md(df_1).plot_df_1(),ticker_acro[0], placeholder = placeholder) 
            i +=1 
            # Limiting it to 10 requests to ensure API limit is not crossed 
            if i > 10:
                break
            time.sleep(1)
            
                



st.sidebar.write(' ')

text = open('text/disclaimer.txt', 'r')
st.sidebar.write(text.read())
st.sidebar.text('Version 1.3')
st.sidebar.text('Updated on 2/23/2021')