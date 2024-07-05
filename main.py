from fastapi import FastAPI, Request
import httpx
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# API Keys 
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

#APIs URL
GEOLOCATION_API_URL =  "http://ip-api.com/json/"
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.get("/api/user")
async def user(request: Request, user_name: str):
    
        user_ip = request.client.host

        # Getting location
        async with httpx.AsyncClient() as client:
            location_response = await client.get(GEOLOCATION_API_URL.format(ip=user_ip))
            location_data = location_response.json()

        city = location_data.get("city", "Unknown Location")

        # Getting weather
        latitude, longitude = location_data.get("loc", "0,0").split(',')
        weather_params = {
            "lat": latitude,
            "lon": longitude,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }

        async with httpx.AsyncClient() as client:
            weather_response = await client.get(WEATHER_API_URL, params=weather_params)
            weather_data = weather_response.json()

        # Extract the current temperature
        temperature = weather_data.get("main", {}).get("temp", 0)

        message = f"Hello, {user_name}!, the temperature is {temperature} degrees Celsius in {city}"

        return {
            "client_ip": user_ip,
            "location": city,
            "message": message
        }
    
    
# @app.get("/test-env")
# async def test_env():rm -rf venv
#     return {"WEATHER_API_KEY": WEATHER_API_KEY}