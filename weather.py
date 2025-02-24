#!/usr/bin/python3

import requests
import json

def get_weather_gov(latitude, longitude):
    try:
        # 1. Get the gridpoints from lat/lon
        points_url = f"https://api.weather.gov/points/{latitude},{longitude}"
        points_response = requests.get(points_url)
        points_response.raise_for_status()
        points_data = points_response.json()
        forecast_url = points_data['properties']['forecastHourly']

        # 2. Get the forecast data
        forecast_response = requests.get(forecast_url)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        # Extract the current forecast
        current_forecast = forecast_data['properties']['periods'][0] #gets the first period which is the current one.
        return current_forecast

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"Error processing weather data: {e}")
        return None

def display_weather_gov(weather_data):
    if weather_data:
        try:
            temperature = weather_data["temperature"]
            unit = weather_data["temperatureUnit"]
            description = weather_data["shortForecast"]
            wind_speed = weather_data["windSpeed"]
            wind_direction = weather_data["windDirection"]

            print("Weather.gov Forecast:")
            print(f"  Temperature: {temperature}°{unit}")
            print(f"  Description: {description}")
            print(f"  Wind: {wind_speed} {wind_direction}")

        except KeyError:
            print("Invalid weather data format.")
    else:
        print("Could not retrieve weather information.")

import requests

def get_lat_lon(city_name, country_code=None):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1,  # Get only the most relevant result
    }
    if country_code:
        params["countrycodes"] = country_code

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        if data:
            latitude = float(data[0]["lat"])
            longitude = float(data[0]["lon"])
            return latitude, longitude
        else:
            return None  # City not found

    except requests.exceptions.RequestException as e:
        print(f"Error fetching coordinates: {e}")
        return None
    except (KeyError, ValueError, IndexError) as e :
        print(f"Error processing coordinates: {e}")
        return None

import requests

def get_location_from_ip(ip_address):
    try:
        url = f"http://ip-api.com/json/{ip_address}"
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        if data["status"] == "success":
            return data
        else:
            print(f"IP lookup failed: {data['message']}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching IP data: {e}")
        return None
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error processing IP data: {e}")
        return None

if __name__ == "__main__":
    ip_address = "" #Leave blank to get your own IP.
    location_data = get_location_from_ip(ip_address)

    if location_data:
        # print(f"IP: {location_data['query']}")
        print(f"City: {location_data['city']}")
        # print(f"Region: {location_data['regionName']}")
        # print(f"Country: {location_data['country']}")
        print(f"Latitude: {location_data['lat']}")
        print(f"Longitude: {location_data['lon']}")
        # print(f"Timezone: {location_data['timezone']}")
        # print(f"ISP: {location_data['isp']}")
    else:
        print("Could not retrieve location information.")
if __name__ == "__main__":
    latitude = location_data['lat']
    longitude = location_data['lon']

    weather_data = get_weather_gov(latitude, longitude)
    display_weather_gov(weather_data)
