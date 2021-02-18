#!/usr/bin/env python
# coding: utf-8
 
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


class api_data():
    def __init__(self,ticker, link, fsname):
        self.link = link[fsname] 
        self.ticker = ticker
        self.fsname = fsname
        
    def remove(self,string):
        pattern = re.compile(r'\s+')
        string = re.sub(pattern, '', string)
        return string.lower()
            
    def col_name_func(self, data_frame):
        return [(re.sub(r'([A-Z])', r' \1', col_name)).title() for col_name in data_frame.columns]
    
    #@st.cache(suppress_st_warning=True)
    def get_data(self, data_or_col = 'data', col_name = None):
        try: 
            link = self.link.format(self.ticker)
            link_1 = link.format(self.ticker)
            txt_file = requests.get(link_1)
            # checking if sufficent data is available    
            txt_file.text[5]
            json_file = txt_file.json()
            col_labels = sorted(list(set([self.remove(j) for i in json_file for j in list(i.keys())])))
            if data_or_col == 'col':
                return col_labels 
            elif col_labels == col_name: 
                df = pd.json_normalize(json_file)
                df.columns = self.col_name_func(df)
                df = df.iloc[0:5,:]
                return df
            else:
                raise AttributeError 
        except AttributeError:
             st.error(print('Sufficent Data Not available or invalid ticker symbol'))
        except IndexError as e:
             st.error(print('Sufficent Data Not available or invalid ticker symbol'))
        except ValueError: 
            print('Data format is incorrect')
    def bs_is(df):
        try:    
            df = df.iloc[:,:-2] 
            df['Accepted Date'] = pd.DatetimeIndex(df['Accepted Date']).date
            return df 
        except AttributeError:
             st.error(print('ufficent Data Not available or invalid ticker symbol- No Data Frame was passed from previous function'))
   
