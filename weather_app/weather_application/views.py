from django.shortcuts import render
import datetime

import requests


def index(request):
    API_KEY = open("C:/Users/Paweł/Desktop/WeatherApp/API_KEY",
                   "r").read().strip()

    current_weather_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

    forecast_url = "http://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"

    if request.method == "POST":
        city1 = request.POST['city1']  # Need valid city
        city2 = request.POST.get('city2', None)  # Optional city

        current_weather1, daily_forecast1 = fetch_weather_and_forecast(
            city1, API_KEY, current_weather_url, forecast_url)

        if city2:
            current_weather2, daily_forecast2 = fetch_weather_and_forecast(
                city2, API_KEY, current_weather_url, forecast_url)
        else:
            current_weather2, daily_forecast2 = None, None

        context = {
            'current_weather1': current_weather1,
            'daily_forecast1': daily_forecast1,
            'current_weather2': current_weather2,
            'daily_forecast2': daily_forecast2,
        }

        return render(request, "weather_application/index.html", context)

    else:
        return render(request, "weather_application/index.html")


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(
        forecast_url.format(lat, lon, api_key)).json()

    current_weather = {
        'city': response['name'],
        'country': response['sys']['country'],
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }

    daily_forecast = []
    for daily_data in forecast_response.get('daily', []):
        daily_forecast.append({
            'date': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%d %b, %Y'),
            'min_temperature': round(daily_data['temp']['min'] - 273.15, 2),
            'max_temperature': round(daily_data['temp']['max'] - 273.15, 2),
            'description': daily_data['weather'][0]['description'],
            'icon': daily_data['weather'][0]['icon']
        })

    return current_weather, daily_forecast
