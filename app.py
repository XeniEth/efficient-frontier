from PIL import Image
import streamlit as st
from constants import *
import datetime
import requests
import json
import pandas as pd


if __name__=='__main__':
    st.header('Efficient Frontier')

    st.sidebar.title('Navigation')

    ct = datetime.datetime.now()
    st.sidebar.write("Current time:", ct)

    coin_choice = st.sidebar.text_input("Coin:", "BTC")

    # Get Data

    endpoint = 'https://min-api.cryptocompare.com/data/histoday'
    res = requests.get(endpoint + '?fsym='+coin_choice+'&tsym=USD&limit=2000')
    hist = pd.DataFrame(json.loads(res.content)['Data'])

    hist = hist.set_index('time')
    hist.index = pd.to_datetime(hist.index, unit='s')
    hist['date']=hist.index

    hist.drop(["conversionType", "conversionSymbol"], axis = 'columns', inplace = True)
    
    hist_year = hist[pd.DatetimeIndex(hist['date']).month*pd.DatetimeIndex(hist['date']).day==1]
    hist_year.drop(['date'])
    
    st.header(coin_choice +' annual activity')
    st.write(hist_year.sort_values(by=['time'], ascending=False))
    
    hist_month = hist[pd.DatetimeIndex(hist['date']).day==1]
    hist_year.drop(['date'])

    st.header(coin_choice +' monthly activity')
    st.write(hist_month.sort_values(by=['time'], ascending=False))
    
