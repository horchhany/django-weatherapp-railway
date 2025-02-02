from django.shortcuts import redirect, render, HttpResponse
from .models import Items, City
import requests
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.


def home(request):

    # define API_KEY and the base url for openweathermap
    API_KEY = '9b24e0c851acb009e8cd7ee45c25f489'
    url ='https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

    # Check if the request is a POST (when adding a new city)
    if request.method == 'POST':
        city_name = request.POST.get('city') #Get city name from the form

        # Fetch weather data for the city from the API
        response = requests.get(url.format(city_name, API_KEY)).json()

        # Check if city exists in the API
        if response['cod'] == 200:
            if not City.objects.filter(name=city_name).exists():
            #Save the new city to database
                City.objects.create(name=city_name)
                messages.success(request, f'{city_name} has been adding successfuly')
            else:
                messages.info(request, f'{city_name} already exists!')
        else:
            messages.error(request, f'{city_name} Not found!')
        return redirect('home')
    # Fetch weather data for all saved cities
    weather_data = []
    try:    
        cities = City.objects.all()   #Get all cities from database
        for city in cities:
            response = requests.get(url.format(city.name, API_KEY)).json()

            if response['cod'] ==200:
                timezone_offset = response.get("timezone", 0)  # ✅ Fix applied
                
                utc_now = datetime.utcnow()  # Current UTC time
                local_time = utc_now + timedelta(seconds=timezone_offset)  # Convert to local time
                city_weather = {
                    'city'        : city.name,
                    'temperature' : response['main']['temp'],
                    'description' : response['weather'][0]['description'],
                    'icon'        : response['weather'][0]['icon'],
                    'local_time'  : local_time.strftime("%Y-%m-%d %H:%M:%S"),  # Local time for the city
                }
                weather_data.append(city_weather)
            else:
                City.objects.filter(name=city.name).delete()

    except requests.RequestException as e:
        print('Error connecting to weather service. Please try again later')
    
    context = {'weather_data' : weather_data}
    return render(request, 'home.html', context)


def items_pro(request):
    products = Items.objects.all()
    return render(
        request=request, 
        template_name='products.html',
        context={'my_items':products}
    )