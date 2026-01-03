import streamlit as st
import requests
import matplotlib.pyplot as plt
from datetime import datetime

# Page setup
st.set_page_config(page_title="🌤️ Weather Report", page_icon="⛅", layout="centered")

st.title("🌤️ Weather Report App")
st.write("Enter a city name to get the live weather details & 5-day forecast")

# User input
city = st.text_input("Enter City Name:")

if city:
    api_key = "823d44e2aa7066d717ed953c56ad2438"  # your API key
    current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

    # Current weather
    response = requests.get(current_url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        description = data['weather'][0]['description'].title()

        st.success(f"📍 City: {city.title()}")
        st.metric("🌡️ Temperature (°C)", f"{temp} °C")
        st.metric("💧 Humidity (%)", f"{humidity}%")
        st.metric("🌬️ Wind Speed (m/s)", f"{wind}")
        st.info(f"🌥️ Condition: {description}")
    else:
        st.error("❌ City not found or API error.")

    # Forecast (5-day every 3 hours data)
    forecast_response = requests.get(forecast_url)
    if forecast_response.status_code == 200:
        forecast_data = forecast_response.json()

        dates, temps = [], []
        for entry in forecast_data['list']:
            dt_txt = entry['dt_txt']
            temp_val = entry['main']['temp']

            # Pick one forecast per day (12:00 PM)
            if "12:00:00" in dt_txt:
                dates.append(datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S").strftime("%d %b"))
                temps.append(temp_val)

        st.subheader("📊 5-Day Forecast")
        fig, ax = plt.subplots()
        ax.plot(dates, temps, marker="o", linestyle="-", color="blue")
        ax.set_title(f"Temperature Forecast for {city.title()}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Temperature (°C)")
        st.pyplot(fig)
    else:
        st.warning("⚠️ Could not fetch forecast data.")
