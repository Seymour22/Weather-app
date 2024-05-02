import pickle
from pathlib import Path
from PIL import Image
import streamlit as st
import streamlit_authenticator as stauth
import requests
from streamlit_lottie import st_lottie
import json

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
    # Replace 'API_KEY' with your actual API key
    api_key = '82f2c5b88afed0120c09e5532e359422'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    return data

def weather_display():
    st.title('SkyCast Weather Display')
    st.markdown("<p style='font-size: 30px; margin-bottom: 0.1px;'>Enter city name</p>", unsafe_allow_html=True)
    city = st.text_input('', 'Cambridge, UK', max_chars=20)  # Default city, max_chars limits the input length
    weather_data = get_weather(city)
    if weather_data['cod'] == 200:
        st.markdown(f"<p style='font-size: 24px;'>Weather in {city}: {weather_data['weather'][0]['description']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 24px;'>Temperature: {weather_data['main']['temp']} °C</p>", unsafe_allow_html=True)
    else:
        st.error('Failed to retrieve weather data.')
        
    weather_description = weather_data['weather'][0]['description'].lower()
    
    
    if 'cloud' in weather_description:
        st_lottie(partlycloudy,height=400, width=400)
    elif 'rain' in weather_description:
        st_lottie(raining,height=400, width=400)
    elif 'snow' in weather_description:
        st_lottie(snow,height=400, width=400)
    elif 'fog' or 'haze' in weather_description:
        st_lottie(foghaze,height=400, width=400)
    elif 'sun' in weather_description:
        st_lottie(sunny,height=400, width=400)
    else:
        st_lottie(defaultweather,height=400, width=400)

    

def main():

    st.set_page_config(page_title="SkyCast Weather", page_icon=icon)

    # --- USER AUTHENTICATION ---
    names = ["Peter Parker", "Rebecca Miller"]
    usernames = ["pparker", "rmiller"]

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
