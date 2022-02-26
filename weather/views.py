from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from .models import Weather
from channels.db import database_sync_to_async
from .forms import InputForm
import aiohttp


# check if the data on precipitation is available in obtained json file
def is_rain(data):
    rain = 0.0
    if data.get('list')[0].get('rain') is None:
        return rain
    return data.get('list')[0].get('rain').get('1h', 0.0)


def weather_to_collect(data):
    weather_dict = {
                'city': data.get('list')[0].get('name'),
                'temp': data.get('list')[0].get('main').get('temp'),
                'hum': data.get('list')[0].get('main').get('humidity'),
                'rain': is_rain(data),  # error occurred on get method
                'icon': data.get('list')[0].get('weather')[0].get('icon')
    }
    return weather_dict


async def get_request(name):
    api_key = 'e418507682f1049e85bfeb6e06cba8ac'
    url = f'https://api.openweathermap.org/data/2.5/find?q={name}&appid=' + api_key + '&units=metric'
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url) as res:
            data = await res.json()
            return data


@database_sync_to_async
def update_weather(info):
    weather = Weather()
    for key, value in info.items():
        setattr(weather, key, value)
    weather.save()


async def index(request):
    weather_info = {}
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data.get("region_name")
            data = await get_request(city_name)
            weather_info = weather_to_collect(data)
            await update_weather(weather_info)
    else:
        form = InputForm()
        city_name = "Minsk"
        data = await get_request(city_name)
        weather_info = weather_to_collect(data)

    context = {"form": form, "info": weather_info}
    return render(request, 'weather/index.html', context)


def about(request):
    return render(request, 'weather/about.html')


def docs(request):
    return redirect('home')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')
