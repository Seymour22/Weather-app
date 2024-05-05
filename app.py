import pickle
import pandas as pd
from pathlib import Path
from PIL import Image
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_lottie import st_lottie
import json

import requests
import threading
import time


icon = Image.open("icon.png")

def load_lottiefile(filepath:str):
    with open(filepath, "r") as f:
        return json.load(f)
    
partlycloudy=load_lottiefile('Animations/partlycloudy.json')
raining=load_lottiefile('Animations/raining.json')
snow=load_lottiefile('Animations/snow.json')
foghaze=load_lottiefile('Animations/foghaze.json')
sunny=load_lottiefile('Animations/sunny.json')
defaultweather=load_lottiefile('Animations/defaultweather.json')


# Function to retrieve weather data from API
def get_weather(city):
    api_key = '82f2c5b88afed0120c09e5532e359422'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    return data

# Display the weather  info and animation
def weather_display():
    st.title('SkyCast Weather Display')
    st.markdown("<p style='font-size: 30px; margin-bottom:0px;'>Enter city name</p>", unsafe_allow_html=True)
    city = st.text_input('', 'Cambridge, UK', max_chars=20)  # Default city, max_chars limits the input length
    
    #While True:
    try:
        weather_data = get_weather(city)

        
        weather_description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        wind_speed = weather_data['wind']['speed']
        humidity = weather_data['main']['humidity']

        if weather_data['cod'] == 200:
            st.write(f"<p style='font-size: 20px;margin-bottom:0.01px;'>Weather in {city}: {weather_description}</p>", unsafe_allow_html=True)
            st.write(f"<p style='font-size: 20px;margin-bottom:0.01px;'>Temperature: {temperature} °C</p>", unsafe_allow_html=True)

            st.write(f"<p style='font-size: 20px;margin-bottom:0.01px;'>Wind Speed: {wind_speed} m/s</p>", unsafe_allow_html=True)
            st.write(f"<p style='font-size: 20px;'>Humidity: {humidity}%</p>", unsafe_allow_html=True)

            
        #Make lower case as first word varies Eg Partly cloudy and Cloudy
        weather_description_l = weather_data['weather'][0]['description'].lower()
        
        
        if 'cloud' in weather_description_l:
            st_lottie(partlycloudy,height=400, width=400)
        elif 'rain' in weather_description_l:
            st_lottie(raining,height=400, width=400)
        elif 'snow' in weather_description_l:
            st_lottie(snow,height=400, width=400)
        elif 'fog' or 'haze' in weather_description_l:
            st_lottie(foghaze,height=400, width=400)
        elif 'sun' in weather_description_l:
            st_lottie(sunny,height=400, width=400)
        else:
            st_lottie(defaultweather,height=400, width=400)
            
    except KeyError:
        st.write("<p style='font-size: 20px;margin-bottom:0.01px;'>Invalid City.  Please try again</p>", unsafe_allow_html=True)


    #time.sleep(3)

def main():

    st.set_page_config(page_title="SkyCast Weather", page_icon=icon)

    userpw = pd.read_csv('usernopw.csv')
    names = userpw['Customer name']
    usernames = userpw['Username']

    # load hashed passwords
    file_path = Path(__file__).parent / "hashed_pw.pkl"
    with file_path.open("rb") as file:
        hashed_passwords = pickle.load(file)

    authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
        "weather_dashboard", "abcdef", cookie_expiry_days=30)

    name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        st.warning("Please enter your username and password")

    if authentication_status:
    
        
        weather_display()
        st.sidebar.title(f"Welcome {name}")
        authenticator.logout("Logout", "sidebar")
            

if __name__ == '__main__':
    main()
