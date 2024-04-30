import pickle
from pathlib import Path
from PIL import Image
import streamlit as st
import streamlit_authenticator as stauth
import requests

im = Image.open("icon.png")

# Function to retrieve weather data from API
def get_weather(city):
    # Replace 'API_KEY' with your actual API key
    api_key = '82f2c5b88afed0120c09e5532e359422'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    return data

def weather_display():
    st.title('Weather Display')
    st.markdown("<p style='font-size: 30px; margin-bottom: 0.1px;'>Enter city name</p>", unsafe_allow_html=True)
    city = st.text_input('', 'Cambridge, UK', max_chars=20)  # Default city, max_chars limits the input length
    weather_data = get_weather(city)
    if weather_data['cod'] == 200:
        st.markdown(f"<p style='font-size: 24px;'>Weather in {city}: {weather_data['weather'][0]['description']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 24px;'>Temperature: {weather_data['main']['temp']} °C</p>", unsafe_allow_html=True)
    else:
        st.error('Failed to retrieve weather data.')


def main():
    # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
    st.set_page_config(page_title="Weather App", page_icon=im, layout="wide")

    # Set sidebar width and border
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            width: 25%;
            padding: 0 20px;
            border-right: 1px solid #d0d0d0;
        }
        .stApp {
            padding: 20px;
            padding-left: 25%;
            padding-right: 25%;
        }
        .login-box input[type="text"], .login-box input[type="password"] {
            width: 200px !important;  /* Adjust the width as needed */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- USER AUTHENTICATION ---
    names = ["Peter Parker", "Rebecca Miller"]
    usernames = ["pparker", "rmiller"]

    # load hashed passwords
    file_path = Path(__file__).parent / "hashed_pw.pkl"
    with file_path.open("rb") as file:
        hashed_passwords = pickle.load(file)

    authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
        "sales_dashboard", "abcdef", cookie_expiry_days=30)

    name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        st.warning("Please enter your username and password")

    if authentication_status:
        # Call the weather display function here
        weather_display()

        # ---- SIDEBAR ----
        authenticator.logout("Logout", "sidebar")
        st.sidebar.title(f"Welcome {name}")

if __name__ == '__main__':
    main()
