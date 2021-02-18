from api_py_fy import api_data
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

class income_statement():
    def __init__(self,df):
        self.df = df

    # Changes to be made in DF for Graph in income statement
    def is_df_1(self):
        self.df = self.df.rename(columns= {'Reported Currency':'Currency', 'Research And Development Expenses':'R&D', 
                'General And Administrative Expenses':'G&A'})
        self.df['Date'] = self.df['Period'] + '_' + self.df['Accepted Date'].astype(str) 
        self.df = self.df.drop(['Accepted Date', 'Period'], axis = 1)
        return self.df

    # For plotting the revenue graph 

    def rev_plot(self):
        fig = px.bar(self.df, x = 'Date', y = 'Revenue',title='Revenue across previous five quarters' ,
        labels={'Date':'Previous five quarters','Revenue':'Amount in $'})
        return st.plotly_chart(fig) 
    # Function for waterfall dataframe for income statement 




    def waterfall_df(self, date):
        #self.df = self.df[(self.df['Date'] == '2021_Q1') | (self.df['Date'] == '2020_Q2')] 
        df = self.df[self.df['Date'] == date]
        df = df.drop(['Date','Symbol', 'Currency','Filling Date'], axis = 1)
        
        df = df.T 
        df = df.rename(columns={df.columns[0]: 'Amount'})
        negative_values = ['Cost Of Revenue','Operating Expenses', 'Cost And Expenses', 
        'Interest Expense','Income Tax Expense']

        df.T.loc[:,set(negative_values) & set(df.index)] *=(-1)
        
        df = df.loc[['Revenue', 'Cost Of Revenue', 'Gross Profit','Operating Expenses','Operating Income',
            'Interest Expense', 'Total Other Income Expenses Net','Income Before Tax','Income Tax Expense', 'Net Income']]

        df_1 = df.reset_index(drop = True)#[(df_3==0).any(axis = 1)]
        index_no = list(df_1[(df_1==0).any(axis = 1)].index)
        
        df = df.reset_index(drop= False).drop(index_no, axis= 'index')
        
        return df, index_no

    def is_waterfall_plot(df, index_no):
        measure_list = np.array(["relative", "relative", "total", "relative","total","relative",'relative',"total",'relative',"total"])

        if len(index_no) > 0:
            measure_list = measure_list[np.arange(len(measure_list)) != index_no]
        fig = go.Figure()
        fig.add_trace(go.Waterfall(
        orientation='v',
        measure = measure_list,
        x = np.array(df['index']),
        y = df.Amount))

        return st.plotly_chart(fig) #fig.show()

    def pct_df(df):
        df = df[~(df==0).all(axis = 1)]
        df = df.set_index('Date')
        df = df[['Revenue', 'Net Income']].iloc[::-1].pct_change().mul(100).iloc[1:]#.iloc[::-1]
        return df



    def rev_income(df, co_name):
        fig = go.Figure()
        x=df.index

        fig.add_trace(go.Scatter(x=x, y=df['Revenue'], fill='tozeroy',
                        mode='none', name = 'revenue %'
                            ))
        # override default markers+lines
        fig.add_trace(go.Scatter(x=x, y= df['Net Income'], fill='tonexty',
                        mode= 'none', name = 'net income %'))
        fig.update_layout(title = "%s - Revenue & Net Income Percentage Change " % co_name)
        return st.plotly_chart(fig)
