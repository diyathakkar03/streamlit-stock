#import icecream as ic 
import yfinance as yf
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import requests 
import json
import re
import datetime
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
# My imports
from api_py_fy import api_data
from income_statement import income_statement as inc
from bs_py_fy import balance_sheet as bs
from bs_py_fy import ratios 


# STREAMLIT 
st.title('Finance Application')


all_links = {"Balance Sheet": "https://financialmodelingprep.com/api/v3/balance-sheet-statement/{}?period=quarter&limit=400&apikey=da58bd9052194c551bbe95498876fda0",
            "Income Statement":"https://financialmodelingprep.com/api/v3/income-statement/{}?period=quarter&limit=400&apikey=da58bd9052194c551bbe95498876fda0",
            "Financial Ratios":"https://financialmodelingprep.com/api/v3/ratios/{}?period=quarter&limit=140&apikey=da58bd9052194c551bbe95498876fda0"}



path = st.text_input('Eneter the ticker symbol here','W', key = '1234')




add_selectbox = st.sidebar.selectbox(
    "Select the financial statement",
    ("Income Statement", "Balance Sheet", "Financial Ratios"))

col_name = api_data('AAPL', all_links,add_selectbox ).get_data('col')


# Block for Error Handling 
try:
    df_1 = api_data(path, all_links, add_selectbox).get_data(col_name = col_name)
except IndexError:
    st.error('The ticker Symbol is invalid or sufficent data not available')
    st.stop()
except ValueError:
    st.error('Sufficent Data Not Available')
    st.stop()


if add_selectbox == 'Income Statement':
    df_1 = api_data.bs_is(df_1)
    df_2 = inc(df_1)

    inc.is_df_1(df_2)

    inc.rev_plot(df_2)
    #rev_plot(df_2)
    #st.write(df_2.df)

    option = st.selectbox('Select the Quarterly Result',list(df_2.df['Date']))

    df_3, index_no = inc.waterfall_df(df_2,date = option)


    inc.is_waterfall_plot(df_3,index_no = index_no)
    #st.write(df_3)
    df_4 = inc.pct_df(df_2.df)
    #st.write(df_4)
    inc.rev_income(df_4, path)

elif add_selectbox == 'Balance Sheet':
    df_1 = api_data.bs_is(df_1)

    #path_1 = st.text_input('Eneter the ticker symbol here','Cash And Cash Equivalents', key = '5')
    df_2 = bs(df_1)
    df_2, df_3 = df_2.bs_df_1()
    
    path_1 = st.selectbox( 'Choose the Portiion of statement to analyze', list(df_2.columns))

    df_3 = bs.con_func(df_2,per_df = df_3)
    bs.bs_plot_1(df_3,row_name = path_1 )
    #st.write('Write the balnce sheet code here 2/16')

elif add_selectbox == 'Financial Ratios':
    df_3,df_4 = ratios(df_1).ratio_df()
    
    #df_3, df_4 = df_2.ratio_df()

    path_3= st.selectbox( 'Choose the Portiion of statement to analyze', list(df_3.columns))

    ratios.ratio_graph(df_3,df_4,col_name=path_3)


