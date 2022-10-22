import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import plotly.express as px

api_key = ""

st.set_page_config(layout="wide", initial_sidebar_state='collapsed', page_icon="📊")

st.header("Weather Forecast")

current_url = "https://api.openweathermap.org/data/2.5/weather?"

forecast_url = "https://api.openweathermap.org/data/2.5/forecast?"

location = st.text_input("Where are you currently located?", value = "Potchefstroom")

if location != "":

    complete_url = current_url + "appid=" + api_key + "&units=metric" + "&q=" + location
    
    response = requests.get(complete_url).json()
    
    y = response["main"]
    
    z = response["weather"]
    
    s = response["sys"]
    
    datetime = datetime.fromtimestamp(s["sunset"])
    
    st.subheader("Current weather")
    
    with st.container():
        
        metric1, metric2, metric3 = st.columns(3)
        
        with metric1:
        
            st.metric("Current Temperature: ", str(y["temp"]) + " °C")
        with metric2:
            
            st.metric("Current Description: ", z[0]["description"].capitalize())
        with metric3:
        
            st.metric("Time of sunset: ", str(datetime))
    
    complete_url = forecast_url + "appid=" + api_key + "&units=metric" + "&q=" + location
    
    response = requests.get(complete_url).json()
    
    st.subheader("9 Hour Forecast")
    
    with st.container():
        
        hour1, hour2, hour3 = st.columns(3)
        
        hour_forecast = response["list"][0]["weather"][0]["description"]
        forecast_time = response["list"][0]["dt_txt"]
        
        with hour1:
            
            with st.container():
                
                st.metric("Weather at " + str(forecast_time) +":",
                          value = str(response["list"][0]['main']['temp']) + " °C")
            
                st.metric('Weather Description: ', hour_forecast.capitalize())
                
                st.metric('Cloud Coverage Percentage: ',
                          str(response["list"][0]['clouds']['all']) + "%")
            
        hour_forecast = response["list"][1]["weather"][0]["description"]
        forecast_time = response["list"][1]["dt_txt"]
            
        with hour2:
            
            with st.container():
            
                st.metric("Weather at " + str(forecast_time) +":",
                          value= str(response["list"][1]['main']['temp']) + " °C")
           
                st.metric('Weather Description: ', hour_forecast.capitalize())
                
                st.metric('Cloud Coverage Percentage: ',
                          str(response["list"][1]['clouds']['all']) + "%")
            
        hour_forecast = response["list"][2]["weather"][0]["description"]
        forecast_time = response["list"][2]["dt_txt"]
            
        with hour3:
            
            with st.container():
            
                st.metric("Weather at " + str(forecast_time) +":",
                          value= str(response["list"][2]['main']['temp']) + " °C")
                
                st.metric('Weather Description: ',
                          hour_forecast.capitalize())
                    
                st.metric('Cloud Coverage Percentage: ',
                          str(response["list"][2]['clouds']['all']) + "%")
                
    st.subheader("5 Day Forecast")
            
    weather_df = pd.DataFrame()
    weather_df['Date-Time'] = []
    weather_df['Weather Description'] = []
    weather_df['Temperature'] = []
    weather_df['Cloud Coverage (%)'] = []
    
    for i in range(0, 39):
        
        weather_df.loc[i] = [response["list"][i]["dt_txt"], 
                             response["list"][i]["weather"][0]["description"].capitalize(), 
                             response["list"][i]['main']['temp'],
                             response["list"][i]['clouds']['all']]
    
    fig = px.bar(weather_df,
                 x='Date-Time',
                 y ='Temperature',
                 text="Weather Description",
                 color='Cloud Coverage (%)')
    
    st.plotly_chart(fig, use_container_width=True)
