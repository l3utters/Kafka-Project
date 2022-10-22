import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime
from datetime import timedelta
import plotly.express as px
import time

st.set_page_config(layout="wide", initial_sidebar_state='collapsed', page_icon="📈")

st.header("Plots")

if not "sleep_time" in st.session_state:
    st.session_state.sleep_time = 1

if not "auto_refresh" in st.session_state:
    st.session_state.auto_refresh = True

auto_refresh = st.checkbox('Auto Refresh?', st.session_state.auto_refresh)

now = datetime.now()

refresh_time, rolling_window = st.columns(2)

if auto_refresh:
    with refresh_time:
        number = st.number_input('Refresh rate in seconds', value=st.session_state.sleep_time)
        st.session_state.sleep_time = number
        
    with rolling_window:  
        window_size = st.slider('Change size of rolling window in minutes', min_value=1, max_value=30, value=10, step=1)
        now1min = now - timedelta(minutes=window_size)

dt_string = now.strftime("%Y-%m-%d %H:%M:%S:%M")
st.write(f"Last update: {dt_string}")

try:
    client = MongoClient("mongodb://localhost:27017/")
    dbname = client['KafkaProject']
    collection_name = dbname["Light-Temp-Volt"]
    
    minback10 = now - timedelta(minutes=window_size)
    
    query =  {'DateTime':{'$gte':minback10,'$lt':now}}
    
    items = collection_name.find(query)
    
    # items = list(collection_name.find())
    df_ts = pd.DataFrame(items)
    client.close()
except:
    client.close()
    st.write("Please Ensure MongoDB instance is running")

if 'df_ts' in locals():        
    
    warning1, warning2 = st.columns(2)
    
    with st.container():
        
        if df_ts.tail(1)["Voltage"].item() > 16:
            st.success("Voltage output is optimal")
        elif df_ts.tail(1)["Voltage"].item() > 12.5:
            st.warning("Voltage output is acceptable")
        else:
            st.error("Voltage output is to low to power devices")
        
        with warning1:
    
            if df_ts.tail(1)["Lux"].item() < 200:
                st.error("Light is too low")
                
            elif df_ts.tail(1)["Lux"].item() < 400:
                st.warning("Light level is falling low")
                
            else:
                st.success("Light is at an acceptable levels")
                
        with warning2:
            
            if df_ts.tail(1)["Temperature"].item() > 35:
                st.error("Panel efficiency is decreased substantially")
                
            elif df_ts.tail(1)["Temperature"].item() > 30:
                st.warning("Temperature is decreasing panel efficiency")
                
            else:
                st.success("Temperature is at an acceptable level")
                
    current1, current2, current3 = st.columns(3)
     
    with st.container():
         
        with current1:
             
            st.metric("Current Voltage", str(df_ts.tail(1)["Voltage"].item()) + " V")
        with current2:
        
            st.metric("Current Lux", str(df_ts.tail(1)["Lux"].item()) + " Lux")
        
        with current3:
        
            st.metric("Current Temperature", str(df_ts.tail(1)["Temperature"].item()) + " C")
                
    fig = px.line(df_ts, x='DateTime', y="Voltage", markers=True)
    fig['layout'].update(margin=dict(l=0,r=0,b=0,t=40), title="Voltage as function of Time")
    fig.update_yaxes(range=[0, 25])
    if auto_refresh:
        fig.update_xaxes(range=[now1min, now])
    st.plotly_chart(fig, use_container_width=True)
    
    plot1, plot2 = st.columns(2)
    
    with plot1:
        
        fig = px.line(df_ts, x='DateTime', y="Lux", markers=True)
        fig['layout'].update(margin=dict(l=0,r=0,b=0,t=40), title="Lux as function of Time")
        fig.update_yaxes(range=[0, df_ts["Lux"].max() * 1.1])
        if auto_refresh:
            fig.update_xaxes(range=[now1min, now])
        st.plotly_chart(fig, use_container_width=True)
    
    with plot2:
    
        fig = px.line(df_ts, x='DateTime', y="Temperature", markers=True)
        fig['layout'].update(margin=dict(l=0,r=0,b=0,t=40), title="Temperature as function of Time")
        fig.update_yaxes(range=[0, 50 * 1.1])
        if auto_refresh:
            fig.update_xaxes(range=[now1min, now])
        st.plotly_chart(fig, use_container_width=True)
        
    # fig = go.Figure()
    
    # fig.add_trace(go.Scatter(x=df_ts['DateTime'], y=df_ts['Candela'], name='Gaps'))
    
    # st.plotly_chart(fig, use_container_width=True)
            
    del df_ts, items

if auto_refresh:
    time.sleep(number)
    st.experimental_rerun()