# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 19:24:26 2021

@author: Maanas
"""

from google.protobuf.symbol_database import Default
import pandas as pd
import yfinance as yf
import streamlit as st
import datetime as dt
import plotly.graph_objects as go
import requests
from bs4 import BeautifulSoup


def calcMovingAverage(data, size):
    df = data.copy()
    df['sma'] = df['Adj Close'].rolling(size).mean()
    df['ema'] = df['Adj Close'].ewm(span=size, min_periods=size).mean()
    df.dropna(inplace=True)
    return df
        
def calc_macd(data):
    df = data.copy()
    df['ema12'] = df['Adj Close'].ewm(span=12, min_periods=12).mean()
    df['ema26'] = df['Adj Close'].ewm(span=26, min_periods=26).mean()
    df['macd'] = df['ema12'] - df['ema26']
    df['signal'] = df['macd'].ewm(span=9, min_periods=9).mean()
    df.dropna(inplace=True)
    return df

def calcBollinger(data, size):
    df = data.copy()
    df["sma"] = df['Adj Close'].rolling(size).mean()
    df["bolu"] = df["sma"] + 2*df['Adj Close'].rolling(size).std(ddof=0) 
    df["bold"] = df["sma"] - 2*df['Adj Close'].rolling(size).std(ddof=0) 
    df["width"] = df["bolu"] - df["bold"]
    df.dropna(inplace=True)
    return df

stockdata = pd.read_csv("C:/Users/Maanas/Desktop/Codes/Trading-main/Datasets/SP500.csv")
symbols = stockdata['Symbol'].sort_values().tolist()        

st.title('Algorithmic Stock Price Predictor and Live Tracker')

#We'll add this when we come up with something
expander=st.beta_expander(label='',expanded=False)
expander.write('**About this application**')

a=st.radio("Would you like to know where to invest or understand each Stock?", ("Invest", "Understand"))

if a=='Understand':    
    ticker = st.sidebar.selectbox(
            'Choose a Stock',symbols)
    
    stock = yf.Ticker(ticker)
    info=stock.info



    ln=info['longName']
    st.title(info['longName'])
    st.title(ticker)
    st.subheader('Stock Price History')
            
    opt1, opt2 = st.beta_columns(2)
            
    with opt1:
        numYearMA = st.number_input('Insert period (Year): ', min_value=1, max_value=10, value=2, key=0)    
            
    with opt2:
        windowSizeMA = st.number_input('Window Size (Day): ', min_value=5, max_value=500, value=20, key=1)  
                

    start = dt.datetime.today()-dt.timedelta(numYearMA * 365)
    end = dt.datetime.today()
    livedata = yf.download(ticker,start,end)
    df_ma = calcMovingAverage(livedata, windowSizeMA)
    df_ma = df_ma.reset_index()
                
    fig = go.Figure()
            
    fig.add_trace(
            go.Scatter(
                x = df_ma['Date'],
                y = df_ma['Adj Close'],
                name = '('+ ticker+ ') '+ "Prices Over Last " + str(numYearMA) + " Year(s)",
                mode='lines',
                line=dict(color='royalblue')
                        )
                )
    compstock2=st.selectbox('Choose stock to compare with: ', symbols)
    livedata2=yf.download(compstock2,start,end)
    df_ma2= calcMovingAverage(livedata2, windowSizeMA)
    df_ma2= df_ma2.reset_index()
    fig.add_trace(
        go.Scatter(
                x=df_ma2['Date'],
                y=df_ma2['Adj Close'],
                name = '('+ compstock2+ ') '+ "Prices Over Last " + str(numYearMA) + " Year(s)",
                mode='lines',
                line=dict(color='firebrick')
                    ))



                    
    fig.update_layout(showlegend=True,legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            ))
                
    fig.update_layout(legend_title_text='Trend')
    fig.update_yaxes(tickprefix="$")
    
        
    st.plotly_chart(fig, use_container_width=True)  
            

            
    st.subheader('Bollinger Band')
    opta, optb = st.beta_columns(2)
    with opta:
        numYearBoll = st.number_input('Insert period (Year): ', min_value=1, max_value=10, value=2, key=6) 
                
    with optb:
        windowSizeBoll = st.number_input('Window Size (Day): ', min_value=5, max_value=500, value=20, key=7)
            
    startBoll= dt.datetime.today()-dt.timedelta(numYearBoll * 365)
    endBoll = dt.datetime.today()
    dataBoll = yf.download(ticker,startBoll,endBoll)
    df_boll = calcBollinger(dataBoll, windowSizeBoll)
    df_boll = df_boll.reset_index()
    figBoll = go.Figure()
    figBoll.add_trace(
                    go.Scatter(
                            x = df_boll['Date'],
                            y = df_boll['bolu'],
                            name = "Upper Band"
                        )
                )
            
            
    figBoll.add_trace(
                        go.Scatter(
                                x = df_boll['Date'],
                                y = df_boll['sma'],
                                name = "SMA" + str(windowSizeBoll) + " Over Last " + str(numYearBoll) + " Year(s)"
                            )
                    )
            
            
    figBoll.add_trace(
                        go.Scatter(
                                x = df_boll['Date'],
                                y = df_boll['bold'],
                                name = "Lower Band"
                            )
                    )
            
    figBoll.update_layout(showlegend=True,legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1,
                xanchor="left",
                x=0
            ))
            
    figBoll.update_yaxes(tickprefix="$")
    st.plotly_chart(figBoll, use_container_width=True)
    st.sidebar.title("Stock News")
    send="https://www.google.com/search?q=should+you+invest+in+ "+ln.lower()+" stock"
    res=requests.get(send)
    soup=BeautifulSoup(res.content, "html.parser")
    all_links=[]
    all_titles=[]
    count=0
    for i in soup.select("a"):
        if count==5:
            break
        link=i.get("href")
        if("/url?q=https://" in link):
            if(("/url?q=https://support.google.com" not in link) and ("/url?q=https://accounts.google.com" not in link)):
                x=link.split("https://")
                y=x[1].split("&sa")
                new="https://"+y[0]
                all_links.append(new)
                z=i.text
                if("..." in z):
                    type2=z.split("...")
                    name=type2[0]
                else:
                    type1=z.split(" › ")
                    name=type1[0]
                all_titles.append(name)
                count+=1
    for i in range(len(all_titles)):
        make="["+str(all_titles[i])+"]"+" "+"("+str(all_links[i])+")"
        st.sidebar.markdown(make)
        st.sidebar.write("")
        st.sidebar.write("")
    



    ##Machine Learning part starts here

    a={}
    c=0
    for i in all_links:
        option=requests.get(i)
        soup=BeautifulSoup(option.content, "html.parser")
        content=[]
        pageinfo=soup.select("p")
        for j in pageinfo:
            content.append(j.text)
        indexnumber=all_links.index(i)
        webname=all_titles[indexnumber]
        a[c]=[webname, content]
        c+=1