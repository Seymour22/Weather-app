import pickle
import pandas as pd
from pathlib import Path
from PIL import Image
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_lottie import st_lottie
import json
import requests

class WeatherAnimationLoader:
    def __init__(self, animations_dir):
        self.animations = {
            "partlycloudy": self.load_lottiefile(f"{animations_dir}/partlycloudy.json"),
            "raining": self.load_lottiefile(f"{animations_dir}/raining.json"),
            "snow": self.load_lottiefile(f"{animations_dir}/snow.json"),
            "foghaze": self.load_lottiefile(f"{animations_dir}/foghaze.json"),
            "sunny": self.load_lottiefile(f"{animations_dir}/sunny.json"),
            "defaultweather": self.load_lottiefile(f"{animations_dir}/defaultweather.json")
        }

    @staticmethod
    def load_lottiefile(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)

class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather(self, city):
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric'
        response = requests.get(url)
        return response.json()

class WeatherDisplay:
    def __init__(self, weather_service, animation_loader):
        self.weather_service = weather_service
        self.animation_loader = animation_loader

    def display(self):
        st.title('SkyCast Weather Display')
        st.markdown("<p style='font-size: 30px; margin-bottom:0px;'>Enter city name</p>", unsafe_allow_html=True)
        city = st.text_input('', 'Cambridge, UK', max_chars=20)  # Default city, max_chars limits the input length

        try:
            weather_data = self.weather_service.get_weather(city)

            if weather_data['cod'] == 200:
                weather_description = weather_data['weather'][0]['description']
                temperature = weather_data['main']['temp']
                wind_speed = weather_data['wind']['speed']
                humidity = weather_data['main']['humidity']

                st.write(f"<p style='font-size: 20px;margin-bottom:0.01px;'>Weather in {city}: {weather_description}</p>", unsafe_allow_html=True)
                st.write(f"<p style='font-size: 20px;margin-bottom:0.01px;'>Temperature: {temperature} °C</p>", unsafe_allow_html=True)
                st.write(f"<p style='font-size: 20px;margin-bottom:0.01px;'>Wind Speed: {wind_speed} m/s</p>", unsafe_allow_html=True)
                st.write(f"<p style='font-size: 20px;'>Humidity: {humidity}%</p>", unsafe_allow_html=True)

                self.display_animation(weather_description.lower())
            else:
                st.error('Failed to retrieve weather data.')

        except KeyError:
            st.write("<p style='font-size: 20px;margin-bottom:0.01px;'>Invalid City. Please try again</p>", unsafe_allow_html=True)

    def display_animation(self, weather_description):
        if 'cloud' in weather_description:
            st_lottie(self.animation_loader.animations['partlycloudy'], height=400, width=400)
        elif 'rain' in weather_description:
            st_lottie(self.animation_loader.animations['raining'], height=400, width=400)
        elif 'snow' in weather_description:
            st_lottie(self.animation_loader.animations['snow'], height=400, width=400)
        elif 'fog' in weather_description or 'haze' in weather_description:
            st_lottie(self.animation_loader.animations['foghaze'], height=400, width=400)
        elif 'sun' in weather_description:
            st_lottie(self.animation_loader.animations['sunny'], height=400, width=400)
        else:
            st_lottie(self.animation_loader.animations['defaultweather'], height=400, width=400)

class Authenticator:
    def __init__(self, user_data_file):
        self.names, self.usernames = self.load_user_data(user_data_file)
        self.hashed_passwords = self.load_hashed_passwords(Path(__file__).parent / "hashed_pw.pkl")
        self.authenticator = stauth.Authenticate(
            self.names, self.usernames, self.hashed_passwords, "weather_dashboard", "abcdef", cookie_expiry_days=30
        )

    @staticmethod
    def load_user_data(user_data_file):
        userpw = pd.read_csv(user_data_file)
        return userpw['Customer name'].tolist(), userpw['Username'].tolist()

    @staticmethod
    def load_hashed_passwords(file_path):
        with file_path.open("rb") as file:
            return pickle.load(file)

    def login(self):
        return self.authenticator.login("Login", "main")

    def logout(self):
        self.authenticator.logout("Logout", "sidebar")

def main():
    st.set_page_config(page_title="SkyCast Weather", page_icon=Image.open("icon.png"))

    authenticator = Authenticator('usernopw.csv')
    name, authentication_status, username = authenticator.login()

    if authentication_status == False:
        st.error("Username/password is incorrect")
    elif authentication_status == None:
        st.warning("Please enter your username and password")
    else:
        weather_service = WeatherService(api_key='82f2c5b88afed0120c09e5532e359422')
        animation_loader = WeatherAnimationLoader('Animations')
        weather_display = WeatherDisplay(weather_service, animation_loader)
        
        weather_display.display()
        
        st.sidebar.title(f"Welcome {name}")
        authenticator.logout()

if __name__ == '__main__':
    main()
