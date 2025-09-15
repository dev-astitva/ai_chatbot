import requests
from config import load_conf

conf = load_conf()
WEATHER_API_KEY = conf["weather_api_key"]

def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": WEATHER_API_KEY, "units": "metric"}
    response = requests.get(base_url, params=params)
    data = response.json()

    if data.get("cod") != 200:
        return "City not found or API error."

    main = data.get("main", {})
    weather = data.get("weather", [{}])[0]
    result = (
        f"Weather in {city.title()}:\n"
        f"  {weather.get('description', '').title()}\n"
        f"  Temperature: {main.get('temp', '?')} °C\n"
        f"  Humidity: {main.get('humidity', '?')} %\n"
        f"  Pressure: {main.get('pressure', '?')} hPa"
    )
    return result
