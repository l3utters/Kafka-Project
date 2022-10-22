import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime
from datetime import timedelta
import plotly.express as px
import numpy as np
from matplotlib import dates
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide", initial_sidebar_state='collapsed', page_icon="📊")

st.header("Analytics")

Analysis_type = st.selectbox("What type of Analysis?", options = ("Historic Data","Averages", "Running Averages", "Trend Analysis"))

Mongo_client = 'KafkaProject'
Mongo_collection = "Light-Temp-Volt"

def plotting(time_from, time_till):
    
    client = MongoClient("mongodb://localhost:27017/")
    dbname = client[Mongo_client]
    collection_name = dbname[Mongo_collection]

    query =  {'DateTime':{'$gte':time_from,'$lt':time_till}}

    items = collection_name.find(query)
    df_ts = pd.DataFrame(items)
    client.close()
    
    del items, query 
    
    return df_ts

if Analysis_type == "Historic Data":
    
    tab1, tab2 = st.tabs(["All Data", "By Date"])
    
    with tab1:
        
        now = datetime.now()+ timedelta(days=1)
        testdate = now - timedelta(days=365)
        
        df_ts = plotting(testdate, now)
        
        fig = px.line(df_ts, x="DateTime", y = "Voltage")
        fig.update_yaxes(range=[0,25])
        fig.update_layout(xaxis_title="Time", yaxis_title="Voltage")
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.line(df_ts, x="DateTime", y = "Lux")
        fig.update_layout(xaxis_title="Time", yaxis_title="Lux")
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.line(df_ts, x="DateTime", y = "Temperature")
        fig.update_yaxes(range=[0,50])
        fig.update_layout(xaxis_title="Time", yaxis_title="Celcius")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        
        date_range = st.date_input("Date to view", value = datetime.now())
        
        time_range = st.slider("Time range to view",
         value=(datetime(2022, 1, 1, 0, 0).time(),
                datetime(2022, 1, 1, 23, 59).time()), 
                format="HH:MM")
        
        time_from = datetime.combine(date_range, time_range[0])
        
        time_till = datetime.combine(date_range, time_range[1])
        
        now = datetime.now()
        testdate = now - timedelta(days=1)
        
        df_ts = plotting(testdate, now)
        
        fig = px.line(df_ts, x="DateTime", y = "Voltage")
        fig.update_yaxes(range=[0,25])
        fig.update_xaxes(range=(time_from, time_till))
        fig.update_layout(xaxis_title="Time", yaxis_title="Voltage")
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.line(df_ts, x="DateTime", y = "Lux")
        fig.update_xaxes(range=(time_from, time_till))
        fig.update_layout(xaxis_title="Time", yaxis_title="Lux")
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.line(df_ts, x="DateTime", y = "Temperature")
        fig.update_yaxes(range=[0,50])
        fig.update_xaxes(range=(time_from, time_till))
        fig.update_layout(xaxis_title="Time", yaxis_title="Celcius")
        st.plotly_chart(fig, use_container_width=True)

if Analysis_type == "Averages":
    
    st.subheader("What timelength of averaging?")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Minute", "Hourly", "Daily", "Weekly", "Monthly"])
    
    with tab1:
        
        st.subheader("Over past 3 days")
        
        now = datetime.now()+ timedelta(days=1)
        testdate = now - timedelta(days=3)
        
        length = st.number_input('Length of Average per minute', value=3,min_value=1)
        
        df_ts = plotting(testdate, now)
        
        size = str(length) + 'T'
        
        daily_voltage = df_ts.resample(size, on='DateTime').mean()['Voltage']
        daily_temp = df_ts.resample(size, on='DateTime').mean()['Temperature']
        daily_candela = df_ts.resample(size, on='DateTime').mean()['Lux']
        
        fig = px.bar(daily_voltage)
        fig.update_xaxes(range=[testdate, now])
        fig.update_yaxes(range=[0,25])
        fig.update_layout(xaxis_title="Time", yaxis_title="Voltage")
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.bar(daily_temp)
        fig.update_xaxes(range=[testdate, now])
        fig.update_yaxes(range=[-10,50])
        fig.update_layout(xaxis_title="Time", yaxis_title="Celcius")
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.bar(daily_candela)
        fig.update_xaxes(range=[testdate, now])
        fig.update_layout(xaxis_title="Time", yaxis_title="Lux")
        st.plotly_chart(fig, use_container_width=True)
        
        del daily_temp, daily_candela, df_ts, length
        
    with tab2:
        
        st.subheader("Over past week")
        
        now = datetime.now()+ timedelta(days=1)
        testdate = now - timedelta(days=7)
        date_range = st.date_input("Date Range", value=(testdate, now), key='hourly')
        
        df_ts = plotting(testdate, now)
        
        daily_voltage = df_ts.resample('H', on='DateTime').mean()['Voltage']
        daily_temp = df_ts.resample('H', on='DateTime').mean()['Temperature']
        daily_candela = df_ts.resample('H', on='DateTime').mean()['Lux']
        
        fig = px.bar(daily_voltage)
        fig.update_xaxes(range=[date_range[0], date_range[1]])
        fig.update_yaxes(range=[0,25])
        fig.update_layout(xaxis_title="Time", yaxis_title="Voltage")
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.bar(daily_temp)
        fig.update_xaxes(range=[date_range[0], date_range[1]])
        fig.update_yaxes(range=[-10,50])
        fig.update_layout(xaxis_title="Time", yaxis_title="Celcius")
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.bar(daily_candela)
        fig.update_xaxes(range=[date_range[0], date_range[1]])
        fig.update_layout(xaxis_title="Time", yaxis_title="Lux")
        st.plotly_chart(fig, use_container_width=True)
        
        del daily_temp, daily_candela, df_ts
        
    with tab3:
        
        st.subheader("Over past week")
        
        now = datetime.now()+ timedelta(days=1)
        testdate = now - timedelta(days=7)
        date_range = st.date_input("Date Range", value=(testdate, now), key='daily')
        
        df_ts = plotting(testdate, now)
        
        daily_voltage = df_ts.resample('D', on='DateTime').mean()['Voltage']
        daily_temp = df_ts.resample('D', on='DateTime').mean()['Temperature']
        daily_candela = df_ts.resample('D', on='DateTime').mean()['Lux']
        
        fig = px.bar(daily_voltage)
        fig.update_xaxes(range=[date_range[0], date_range[1]])
        fig.update_yaxes(range=[0,25])
        fig.update_layout(xaxis_title="Time", yaxis_title="Voltage")
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.bar(daily_temp)
        fig.update_xaxes(range=[date_range[0], date_range[1]])
        fig.update_yaxes(range=[-10,50])
        fig.update_layout(xaxis_title="Time", yaxis_title="Celcius")
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.bar(daily_candela)
        fig.update_xaxes(range=[date_range[0], date_range[1]])
        fig.update_layout(xaxis_title="Time", yaxis_title="Lux")
        st.plotly_chart(fig, use_container_width=True)
        
        del daily_temp, daily_candela, df_ts
        
    with tab4:
        
        st.subheader("Over past month")
        
        now = datetime.now()+ timedelta(days=1)
        testdate = now - timedelta(days=28)
        date_range = st.date_input("Date Range", value=(testdate, now), key='weekly')
        
        df_ts = plotting(testdate, now)
        
        daily_voltage = df_ts.resample('W', on='DateTime').mean()['Voltage']
        daily_temp = df_ts.resample('W', on='DateTime').mean()['Temperature']
        daily_candela = df_ts.resample('W', on='DateTime').mean()['Lux']
        
        fig = px.bar(daily_voltage)
        fig.update_xaxes(range=[date_range[0], date_range[1]])
        fig.update_yaxes(range=[0,25])
        fig.update_layout(xaxis_title="Time", yaxis_title="Voltage")
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.bar(daily_temp)
        fig.update_xaxes(range=[date_range[0], date_range[1]])
        fig.update_yaxes(range=[-10,50])
        fig.update_layout(xaxis_title="Time", yaxis_title="Celcius")
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.bar(daily_candela)
        fig.update_xaxes(range=[date_range[0], date_range[1]])
        fig.update_layout(xaxis_title="Time", yaxis_title="Lux")
        st.plotly_chart(fig, use_container_width=True)
        
        del daily_temp, daily_candela, df_ts
        
    with tab5:
        
        st.subheader("Over past year")
        
        now = datetime.now()+ timedelta(days=1)
        testdate = now - timedelta(days=365)
        date_range = st.date_input("Date Range", value=(testdate, now), key='montly')
        
        df_ts = plotting(testdate, now)
        
        daily_voltage = df_ts.resample('M', on='DateTime').mean()['Voltage']
        daily_temp = df_ts.resample('M', on='DateTime').mean()['Temperature']
        daily_candela = df_ts.resample('M', on='DateTime').mean()['Lux']
        
        fig = px.bar(daily_voltage)
        fig.update_xaxes(range=[date_range[0], date_range[1]])
        fig.update_yaxes(range=[0,25])
        fig.update_layout(xaxis_title="Time", yaxis_title="Voltage")
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.bar(daily_temp)
        fig.update_xaxes(range=[date_range[0], date_range[1]])
        fig.update_yaxes(range=[-10,50])
        fig.update_layout(xaxis_title="Time", yaxis_title="Celcius")
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.bar(daily_candela)
        fig.update_xaxes(range=[date_range[0], date_range[1]])
        fig.update_layout(xaxis_title="Time", yaxis_title="Lux")
        st.plotly_chart(fig, use_container_width=True)
        
        del daily_temp, daily_candela, df_ts
        
if Analysis_type == "Running Averages":
    
    st.subheader("Over past 24 hours")
    
    average_length = st.number_input("Size of rolling window", min_value = 3, max_value=10)
    
    now = datetime.now()+ timedelta(days=1)
    testdate = now - timedelta(days=1)    
    date_range = st.date_input("Date Range", value=(testdate, now), key='test')
    
    now = datetime.now()
    testdate = now - timedelta(days=1)
        
    df_ts = plotting(testdate, now)
    
    rolling_voltage = df_ts['Voltage'].rolling(average_length).mean()
    
    fig = px.line(x=df_ts["DateTime"], y= rolling_voltage)
    fig.update_xaxes(range=[date_range[0], date_range[1]])
    fig.update_yaxes(range=[0,25])
    fig.update_layout(xaxis_title="Time", yaxis_title="Voltage")
    st.plotly_chart(fig, use_container_width=True)
    
    rolling_temp = df_ts["Temperature"].rolling(average_length).mean()
    
    fig = px.line(x=df_ts["DateTime"], y= rolling_temp)
    fig.update_xaxes(range=[date_range[0], date_range[1]])
    fig.update_yaxes(range=[-10,50])
    fig.update_layout(xaxis_title="Time", yaxis_title="Celcius")
    st.plotly_chart(fig, use_container_width=True)
    
    rolling_light = df_ts["Lux"].rolling(average_length).mean()
    
    fig = px.line(x=df_ts["DateTime"], y= rolling_light)
    fig.update_xaxes(range=[date_range[0], date_range[1]])
    fig.update_layout(xaxis_title="Time", yaxis_title="Lux")
    st.plotly_chart(fig, use_container_width=True)
    
    del rolling_temp, rolling_light, df_ts, testdate, now
    
if Analysis_type == "Trend Analysis":
        
    date_range = st.date_input("Date to view", value = datetime.now(), key='date1')
    
    time_range = st.slider("Time range to view",
     value=(datetime(2022, 1, 1, 6, 0).time(), datetime(2022, 1, 1, 18, 0).time()), 
     format="HH:MM", key='time1')
    
    prediction = st.checkbox('Add forecast data?')
    
    time_from = datetime.combine(date_range, time_range[0])
    
    time_till = datetime.combine(date_range, time_range[1])
    
    df_ts = plotting(time_from, time_till)
    
    if 'df_ts' in locals():    
    
        x = dates.date2num(df_ts['DateTime'])
        y = df_ts['Voltage']
        z = np.polyfit(x, df_ts['Voltage'], 3)
        p = np.poly1d(z)
        
        if prediction:
            
            timestamp_list = [df_ts.tail(1)["DateTime"].item() + timedelta(minutes=x)
                              for x in range(120)]
                    
            df = pd.DataFrame(timestamp_list)
            df['DateTime'] = pd.to_datetime(df[0])
    
            timestamps = dates.date2num(df['DateTime'])  
        
        fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])
        
        fig.add_trace(go.Scatter(x=df_ts['DateTime'], y = df_ts["Voltage"], mode="markers", line=dict(color="#304DDF")),row=1, col=1, secondary_y=False)
        fig.update_yaxes(range=[0,25])
        fig.update_xaxes(range=(time_from, time_till))
        fig.add_trace(go.Scatter(x=df_ts['DateTime'], y=p(x), line=dict(color="#FF4F00"), name='Trend'),row=1, col=1, secondary_y=True)
        fig.update_layout(xaxis_title="Time", yaxis_title="Voltage")
        
        if prediction:
            
            test = np.polyval(z, timestamps)
            
            fig.add_trace(go.Scatter(x=df['DateTime'],
                                     y=test,
                                     line=dict(color="#21C128"),
                                     name='Prediction'),
                                     row=1,
                                     col=1,
                                     secondary_y=False)
        
        st.plotly_chart(fig, use_container_width=True)
        
        x = dates.date2num(df_ts['DateTime'])
        y = df_ts['Lux']
        z = np.polyfit(x, df_ts['Lux'], 3)
        p = np.poly1d(z)
        
        fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])
        
        fig.add_trace(go.Scatter(x=df_ts['DateTime'],
                                 y = df_ts["Lux"],
                                 mode="markers",
                                 line=dict(color="#304DDF")),
                                 row=1,
                                 col=1,
                                 secondary_y=False)

        fig.update_xaxes(range=(time_from, time_till))
        fig.add_trace(go.Scatter(x=df_ts['DateTime'], y=p(x), line=dict(color="#FF4F00"), name='Trend'))
        fig.update_layout(xaxis_title="Time", yaxis_title="Lux")
        
        if prediction:
            
            test = np.polyval(z, timestamps)
            
            fig.add_trace(go.Scatter(x=df['DateTime'],
                                     y=test,
                                     line=dict(color="#21C128"),
                                     name='Prediction'),
                                     row=1,
                                     col=1,
                                     secondary_y=False)
        
        st.plotly_chart(fig, use_container_width=True)
        
        x = dates.date2num(df_ts['DateTime'])
        y = df_ts['Temperature']
        z = np.polyfit(x, df_ts['Temperature'], 3)
        p = np.poly1d(z)
        
        fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=df_ts['DateTime'],
                                 y = df_ts["Temperature"],
                                 mode="markers",
                                 line=dict(color="#304DDF")),
                                 row=1,
                                 col=1,
                                 secondary_y=False)

        fig.update_yaxes(range=[0,50])
        fig.add_trace(go.Scatter(x=df_ts['DateTime'],
                                 y=p(x),
                                 line=dict(color="#FF4F00"),
                                 name='Trend'))

        fig.update_xaxes(range=(time_from, time_till))
        fig.update_layout(xaxis_title="Time", yaxis_title="Celcius")
        
        if prediction:
            
            test = np.polyval(z, timestamps)
            
            fig.add_trace(go.Scatter(x=df['DateTime'],
                                     y=test,
                                     line=dict(color="#21C128"),
                                     name='Prediction'),
                                     row=1,
                                     col=1,
                                     secondary_y=False)
        
        st.plotly_chart(fig, use_container_width=True)
        
        del df_ts, x, y, z, p