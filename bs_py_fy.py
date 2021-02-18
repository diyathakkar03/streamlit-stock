#!/usr/bin/env python
# coding: utf-8
 
import icecream as ic 
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
from api_py_fy import api_data


class balance_sheet():
    def __init__(self,df):
        self.df = df    

    def bs_df_1(self):
        self.df['Date'] = self.df['Period'] + '_' + self.df['Accepted Date'].astype(str) 
        self.df = self.df.drop(['Accepted Date', 'Period', 'Symbol', 'Reported Currency', 'Filling Date'], axis = 1)
        self.df = self.df.set_index('Date')
        #Dropping columns which contains only zero 
        self.df = self.df.loc[:,(self.df != 0).any(axis=0)]
        df_1 = self.df.copy().iloc[::-1].pct_change().mul(100).iloc[::-1]
        return self.df, df_1.fillna(0)

   

    def con_func(df,per_df):
        per_df.columns = [i + ' %' for i in per_df.columns]
        df = pd.concat([df,per_df], axis = 1)
        return df

        #df_4 = con_func(df_2, df_3)


    def bs_plot_1(df, row_name):
        df = df.iloc[::-1]
        row_name_2 = row_name + ' %'
        row_1 = df.loc[:,row_name]
        row_2 = np.select([df.loc[:,row_name_2]<0,df.loc[:,row_name_2]>0,df.loc[:,row_name_2] == 0], ['Decrease', 'Increase', 'NA'])
        row_3 = df.loc[:,row_name_2]
        x = df.index
        fig = px.bar(x = x, y = row_1,title='%s'%row_name , color = row_2, hover_data= [row_3],
                        labels={'x':'Previous five quarters','y':'Amount in $'})
        return st.plotly_chart(fig)

class ratios():
    def __init__(self,df):
        self.df = df
    def ratio_df(self):
        df_1 = self.df.loc[:,['Date']]
        df_2 = self.df.drop(['Symbol','Date'], axis = 1) 
        return df_2,df_1
    def ratio_graph(df_1,df_2, col_name):
        x = df_2['Date']
        y = df_1[col_name]
        fig = px.line(x=x, y=y, title='Financial Ratios',
        labels={'y':'%s'%col_name,'x':'Date'})
        return st.plotly_chart(fig)