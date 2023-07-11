from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Shapes, UserProfile, Sunradiation, Odor, Humidity, Raindrop, Temperature, Light, Moisture, Pressure, Shop, Specialists, Review
from django.shortcuts import render
from django.conf import settings
import requests
import json
from django.db import transaction
from django.db.models import Q
import openai
from geopy.geocoders import Nominatim
from django.http import JsonResponse

openai.api_key = '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'

def get_coordinates(address):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(address)

    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    elif location := geolocator.geocode(address, exactly_one=False):
        # Use the first close match found
        latitude = location[0].latitude
        longitude = location[0].longitude
        return latitude, longitude
    else:
        return None

@transaction.atomic
def index(request):
    context = {}
    return render(request, 'main/index.html', context)

@login_required()
def graphs(request, param):
    sunradiation_values = Sunradiation.objects.filter(user=request.user, **{f"{param}per__isnull": False}).order_by(f"{param}").values_list(
        f'{param}per', flat=True)
    sunradiation_data = list(sunradiation_values)

    odor_values = Odor.objects.filter(user=request.user, **{f"{param}per__isnull": False}).order_by(f"{param}").values_list(f'{param}per',
                                                                                                       flat=True)
    odor_data = list(odor_values)

    humidity_values = Humidity.objects.filter(user=request.user, **{f"{param}per__isnull": False}).order_by(f"{param}").values_list(
        f'{param}per', flat=True)
    humidity_data = list(humidity_values)

    raindrop_values = Raindrop.objects.filter(user=request.user, **{f"{param}per__isnull": False}).order_by(f"{param}").values_list(
        f'{param}per', flat=True)
    raindrop_data = list(raindrop_values)

    temperature_values = Temperature.objects.filter(user=request.user, **{f"{param}per__isnull": False}).order_by(f"{param}").values_list(
        f'{param}per', flat=True)
    temperature_data = list(temperature_values)

    light_values = Light.objects.filter(user=request.user, **{f"{param}per__isnull": False}).order_by(f"{param}").values_list(f'{param}per',
                                                                                                         flat=True)
    light_data = list(light_values)

    moisture_values = Moisture.objects.filter(user=request.user, **{f"{param}per__isnull": False}).order_by(f"{param}").values_list(
        f'{param}per', flat=True)
    moisture_data = list(moisture_values)

    pressure_values = Pressure.objects.filter(user=request.user, **{f"{param}per__isnull": False}).order_by(f"{param}").values_list(
        f'{param}per', flat=True)
    pressure_data = list(pressure_values)

    context = {'humidity_data': humidity_data,
               'sunradiation_data': sunradiation_data,
               'odor_data': odor_data,
               'raindrop_data': raindrop_data,
               'temperature_data': temperature_data,
               'light_data': light_data,
               'moisture_data': moisture_data,
               'pressure_data': pressure_data,
               'interval': param,
               }

    print(light_data)
    print(humidity_data)
    print(sunradiation_data)

    return render(request, 'main/graphs.html', context)


@login_required()
def graphspredict(request, param):
    sunradiation_values = Sunradiation.objects.filter(user=request.user, **{f"{param}per__isnull": False}).order_by(f"{param}").values_list(
        f'{param}per', flat=True)
    sunradiation_data = list(sunradiation_values)

    odor_values = Odor.objects.filter(user=request.user, **{f"{param}per__isnull": False}).order_by(f"{param}").values_list(f'{param}per',
                                                                                                       flat=True)
    odor_data = list(odor_values)

    humidity_values = Humidity.objects.filter(user=request.user, **{f"{param}per__isnull": False}).order_by(f"{param}").values_list(
        f'{param}per', flat=True)
    humidity_data = list(humidity_values)

    raindrop_values = Raindrop.objects.filter(user=request.user, **{f"{param}per__isnull": False}).order_by(f"{param}").values_list(
        f'{param}per', flat=True)
    raindrop_data = list(raindrop_values)

    temperature_values = Temperature.objects.filter(user=request.user, **{f"{param}per__isnull": False}).order_by(f"{param}").values_list(
        f'{param}per', flat=True)
    temperature_data = list(temperature_values)

    light_values = Light.objects.filter(user=request.user, **{f"{param}per__isnull": False}).order_by(f"{param}").values_list(f'{param}per',
                                                                                                         flat=True)
    light_data = list(light_values)

    moisture_values = Moisture.objects.filter(user=request.user, **{f"{param}per__isnull": False}).order_by(f"{param}").values_list(
        f'{param}per', flat=True)
    moisture_data = list(moisture_values)

    pressure_values = Pressure.objects.filter(user=request.user, **{f"{param}per__isnull": False}).order_by(f"{param}").values_list(
        f'{param}per', flat=True)
    pressure_data = list(pressure_values)

    superlist = [humidity_data, sunradiation_data, odor_data, raindrop_data, temperature_data, light_data, moisture_data, pressure_data]
    for i in superlist:
        input_sequence = str(i)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=input_sequence + "\nHere is my array with values. Your task is to predict next values(if all are 0, then just return the same list) and give me array with the same length, but with predicted values.",
            max_tokens=120,
            n=1,
            stop=None,
            temperature=0.7
        )

        predicted_sequence = response.choices[0].text
        list_sequence = eval(predicted_sequence)
        i = list_sequence

    context = {'humidity_data': humidity_data,
               'sunradiation_data': sunradiation_data,
               'odor_data': odor_data,
               'raindrop_data': raindrop_data,
               'temperature_data': temperature_data,
               'light_data': light_data,
               'moisture_data': moisture_data,
               'pressure_data': pressure_data,
               'interval': param,
               }

    print(light_data)
    print(humidity_data)
    print(sunradiation_data)

    return render(request, 'main/graphspredict.html', context)


def graphsai(request):
    context = {}
    return render(request, 'main/graphsai.html', context)

def profile(request):
    context = {}
    return render(request, 'main/profile.html', context)

def add_shape(request):
    if request.method == "POST":
        userprofile = UserProfile.objects.get(user=request.user)
        drawn_shapes = request.POST.getlist('drawn_shapes[]')
        print(drawn_shapes)
        for shape in drawn_shapes:
            shape_obj = Shapes.objects.create(user=request.user, shape=shape)
            userprofile.shapes.add(shape_obj)
        return redirect('geolocation')

def geolocation(request):
    userprofile = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        lat = request.POST['lat']
        long = request.POST['long']
        userprofile.geolocation1 = str(lat)
        userprofile.geolocation2 = str(long)
        userprofile.save()
    else:
        if userprofile.geolocation1:
            lat = float(userprofile.geolocation1)
            long = float(userprofile.geolocation2)
        else:
            return render(request, 'main/geolocation.html')

    shapes = userprofile.shapes.all()
    drawn_shapes = [shape.shape for shape in shapes]
    print(drawn_shapes)
    context = {'lat':lat, 'long':long, 'drawn_shapes': drawn_shapes}
    return render(request, 'main/geolocation.html', context)


def shop(request):
    goods = Shop.objects.all()
    context = {'goods':goods}
    return render(request, 'main/shop.html', context)

def specialists(request):
    experience = request.GET.getlist('experience')
    city = request.GET.getlist('city')
    specialization = request.GET.getlist('profession')


    conditions = Q()
    if experience:
        if 'no' in experience:
            conditions |= Q(experience__gte=0)
        if '1-3' in experience:
            conditions |= Q(experience__range=(1, 3))
        if '3-6' in experience:
            conditions |= Q(experience__range=(3, 6))
        if '6-9' in experience:
            conditions |= Q(experience__range=(6, 9))
        if '10+' in experience:
            conditions |= Q(experience__gte=10)

    if city:
        if 'all' not in city:
            conditions &= Q(city__in=city)  # Filter by selected cities

    if specialization:
        if 'all' not in specialization:
            conditions &= Q(specialization__in=specialization)  # Filter by selected specializations

    filtered_specialists = Specialists.objects.filter(conditions)

    context = {'specialists': filtered_specialists}
    return render(request, 'main/specialists.html', context)

def education(request):
    context = {}
    return render(request, 'main/education.html', context)

def loginsystem(request):
    if request.method == "GET":
        return render(request, 'main/loginsystem.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'main/loginsystem.html',
                          {'form': AuthenticationForm, 'error': 'Неверный логин и/или пароль'})


def signupsystem(request):
    if request.method == "GET":
        return render(request, 'main/signupsystem.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] != request.POST['password2']:
            return render(request, 'main/signupsystem.html',
                          {'form': UserCreationForm, 'error': 'Passwords don\'t match!'})
        else:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'],
                                                first_name=request.POST['name'],
                                                last_name=request.POST['lastname']
                                                )
                user.save()
                login(request, user)

                profession = request.POST['profession']
                if profession == "Владелец Фермы":
                    user_profile = UserProfile.objects.create(user=request.user)
                    phone = int(request.POST['phone'])
                    profession = request.POST['profession']
                    user_profile.telephone = phone
                    user_profile.profession = profession
                    user_profile.save()

                    val10 = [Humidity, Raindrop, Moisture]
                    val7 = [Temperature, Light, Pressure, Odor]
                    val30 = [Sunradiation,]

                    val7_data = [
                        {'min': i, 'minper': 0} for i in range(0, 61, 2)
                    ]
                    val7_data1 = [
                        {'day': i, 'dayper': 0} for i in range(0, 25)
                    ]
                    val7_data2 = [
                        {'week': i, 'weekper': 0} for i in range(0, 8)
                    ]
                    val7_data3 = [
                        {'month': i, 'monthper': 0} for i in range(0, 31)
                    ]
                    val7_data4 = [
                        {'year': i, 'yearper': 0} for i in range(0, 13)
                    ]


                    val10_data = [
                        {'min': 0, 'minper': 0},
                        {'min': 6, 'minper': 0},
                        {'min': 12, 'minper': 0},
                        {'min': 18, 'minper': 0},
                        {'min': 24, 'minper': 0},
                        {'min': 30, 'minper': 0},
                        {'min': 36, 'minper': 0},
                        {'min': 42, 'minper': 0},
                        {'min': 48, 'minper': 0},
                        {'min': 54, 'minper': 0},
                        {'min': 60, 'minper': 0}
                    ]

                    val10_data1 = [
                        {'day': 0, 'dayper': 0},
                        {'day': 2, 'dayper': 0},
                        {'day': 4, 'dayper': 0},
                        {'day': 6, 'dayper': 0},
                        {'day': 8, 'dayper': 0},
                        {'day': 10, 'dayper': 0},
                        {'day': 12, 'dayper': 0},
                        {'day': 14, 'dayper': 0},
                        {'day': 16, 'dayper': 0},
                        {'day': 18, 'dayper': 0},
                        {'day': 20, 'dayper': 0},
                        {'day': 22, 'dayper': 0},
                        {'day': 24, 'dayper': 0}
                    ]

                    val10_data2 = [
                        {'week': 0, 'weekper': 0},
                        {'week': 1, 'weekper': 0},
                        {'week': 2, 'weekper': 0},
                        {'week': 3, 'weekper': 0},
                        {'week': 4, 'weekper': 0},
                        {'week': 5, 'weekper': 0},
                        {'week': 6, 'weekper': 0},
                        {'week': 7, 'weekper': 0}
                    ]

                    val10_data3 = [
                        {'month': 0, 'monthper': 0},
                        {'month': 3, 'monthper': 0},
                        {'month': 6, 'monthper': 0},
                        {'month': 9, 'monthper': 0},
                        {'month': 12, 'monthper': 0},
                        {'month': 15, 'monthper': 0},
                        {'month': 18, 'monthper': 0},
                        {'month': 21, 'monthper': 0},
                        {'month': 24, 'monthper': 0},
                        {'month': 27, 'monthper': 0},
                        {'month': 30, 'monthper': 0},
                    ]

                    val10_data4 = [
                        {'year': 0, 'yearper': 0},
                        {'year': 1, 'yearper': 0},
                        {'year': 2, 'yearper': 0},
                        {'year': 3, 'yearper': 0},
                        {'year': 4, 'yearper': 0},
                        {'year': 5, 'yearper': 0},
                        {'year': 6, 'yearper': 0},
                        {'year': 7, 'yearper': 0},
                        {'year': 8, 'yearper': 0},
                        {'year': 9, 'yearper': 0},
                        {'year': 10, 'yearper': 0},
                        {'year': 11, 'yearper': 0},
                        {'year': 12, 'yearper': 0},
                    ]





                    odors_data = [
                        {'min': 0, 'minper': 0},
                        {'min': 10, 'minper': 0},
                        {'min': 20, 'minper': 0},
                        {'min': 30, 'minper': 0},
                        {'min': 40, 'minper': 0},
                        {'min': 50, 'minper': 0},
                        {'min': 60, 'minper': 0}
                    ]

                    odors_data1 = [
                        {'day': 0, 'dayper': 0},
                        {'day': 4, 'dayper': 0},
                        {'day': 8, 'dayper': 0},
                        {'day': 12, 'dayper': 0},
                        {'day': 16, 'dayper': 0},
                        {'day': 20, 'dayper': 0},
                        {'day': 24, 'dayper': 0}
                    ]

                    odors_data2 = [
                        {'week': 0, 'weekper': 0},
                        {'week': 1, 'weekper': 0},
                        {'week': 2, 'weekper': 0},
                        {'week': 3, 'weekper': 0},
                        {'week': 4, 'weekper': 0},
                        {'week': 5, 'weekper': 0},
                        {'week': 6, 'weekper': 0},
                        {'week': 7, 'weekper': 0}
                    ]

                    odors_data3 = [
                        {'month': 0, 'monthper': 0},
                        {'month': 5, 'monthper': 0},
                        {'month': 10, 'monthper': 0},
                        {'month': 15, 'monthper': 0},
                        {'month': 20, 'monthper': 0},
                        {'month': 25, 'monthper': 0},
                        {'month': 30, 'monthper': 0},
                    ]

                    odors_data4 = [
                        {'year': 0, 'yearper': 0},
                        {'year': 2, 'yearper': 0},
                        {'year': 4, 'yearper': 0},
                        {'year': 6, 'yearper': 0},
                        {'year': 8, 'yearper': 0},
                        {'year': 10, 'yearper': 0},
                        {'year': 12, 'yearper': 0},
                    ]

                    for data in val7_data:
                        sunradiation = Sunradiation.objects.create(user=request.user, min=data['min'],
                                                                   minper=data['minper'])
                        user_profile.sunradiation.add(sunradiation)

                    for data in val7_data1:
                        sunradiation = Sunradiation.objects.create(user=request.user, day=data['day'],
                                                                   dayper=data['dayper'])
                        user_profile.sunradiation.add(sunradiation)

                    for data in val7_data2:
                        sunradiation = Sunradiation.objects.create(user=request.user, week=data['week'],
                                                                   weekper=data['weekper'])
                        user_profile.sunradiation.add(sunradiation)

                    for data in val7_data3:
                        sunradiation = Sunradiation.objects.create(user=request.user, month=data['month'],
                                                                   monthper=data['monthper'])
                        user_profile.sunradiation.add(sunradiation)

                    for data in val7_data4:
                        sunradiation = Sunradiation.objects.create(user=request.user, year=data['year'],
                                                                   yearper=data['yearper'])
                        user_profile.sunradiation.add(sunradiation)

                    for data in val10_data:
                        humidity = Humidity.objects.create(user=request.user, min=data['min'], minper=data['minper'])
                        raindrop = Raindrop.objects.create(user=request.user, min=data['min'], minper=data['minper'])
                        moisture = Moisture.objects.create(user=request.user, min=data['min'], minper=data['minper'])
                        user_profile.humidity.add(humidity)
                        user_profile.raindrop.add(raindrop)
                        user_profile.moisture.add(moisture)

                    for data in val10_data1:
                        humidity = Humidity.objects.create(user=request.user, day=data['day'], dayper=data['dayper'])
                        raindrop = Raindrop.objects.create(user=request.user, day=data['day'], dayper=data['dayper'])
                        moisture = Moisture.objects.create(user=request.user, day=data['day'], dayper=data['dayper'])
                        user_profile.humidity.add(humidity)
                        user_profile.raindrop.add(raindrop)
                        user_profile.moisture.add(moisture)

                    for data in val10_data2:
                        humidity = Humidity.objects.create(user=request.user, week=data['week'],
                                                           weekper=data['weekper'])
                        raindrop = Raindrop.objects.create(user=request.user, week=data['week'],
                                                           weekper=data['weekper'])
                        moisture = Moisture.objects.create(user=request.user, week=data['week'],
                                                           weekper=data['weekper'])
                        user_profile.humidity.add(humidity)
                        user_profile.raindrop.add(raindrop)
                        user_profile.moisture.add(moisture)

                    for data in val10_data3:
                        humidity = Humidity.objects.create(user=request.user, month=data['month'],
                                                           monthper=data['monthper'])
                        raindrop = Raindrop.objects.create(user=request.user, month=data['month'],
                                                           monthper=data['monthper'])
                        moisture = Moisture.objects.create(user=request.user, month=data['month'],
                                                           monthper=data['monthper'])
                        user_profile.humidity.add(humidity)
                        user_profile.raindrop.add(raindrop)
                        user_profile.moisture.add(moisture)

                    for data in val10_data4:
                        humidity = Humidity.objects.create(user=request.user, year=data['year'],
                                                           yearper=data['yearper'])
                        raindrop = Raindrop.objects.create(user=request.user, year=data['year'],
                                                           yearper=data['yearper'])
                        moisture = Moisture.objects.create(user=request.user, year=data['year'],
                                                           yearper=data['yearper'])
                        user_profile.humidity.add(humidity)
                        user_profile.raindrop.add(raindrop)
                        user_profile.moisture.add(moisture)

                    for odor_data in odors_data:
                        odor = Odor.objects.create(user=request.user, min=odor_data['min'], minper=odor_data['minper'])
                        temperature = Temperature.objects.create(user=request.user, min=odor_data['min'], minper=odor_data['minper'])
                        light = Light.objects.create(user=request.user, min=odor_data['min'], minper=odor_data['minper'])
                        pressure = Pressure.objects.create(user=request.user, min=odor_data['min'], minper=odor_data['minper'])
                        user_profile.odor.add(odor)
                        user_profile.temperature.add(temperature)
                        user_profile.light.add(light)
                        user_profile.pressure.add(pressure)

                    for odor_data in odors_data1:
                        odor = Odor.objects.create(user=request.user, day=odor_data['day'], dayper=odor_data['dayper'])
                        temperature = Temperature.objects.create(user=request.user, day=odor_data['day'],
                                                                 dayper=odor_data['dayper'])
                        light = Light.objects.create(user=request.user, day=odor_data['day'],
                                                     dayper=odor_data['dayper'])
                        pressure = Pressure.objects.create(user=request.user, day=odor_data['day'],
                                                           dayper=odor_data['dayper'])
                        user_profile.odor.add(odor)
                        user_profile.temperature.add(temperature)
                        user_profile.light.add(light)
                        user_profile.pressure.add(pressure)

                    for odor_data in odors_data2:
                        odor = Odor.objects.create(user=request.user, week=odor_data['week'],
                                                   weekper=odor_data['weekper'])
                        temperature = Temperature.objects.create(user=request.user, week=odor_data['week'],
                                                                 weekper=odor_data['weekper'])
                        light = Light.objects.create(user=request.user, week=odor_data['week'],
                                                     weekper=odor_data['weekper'])
                        pressure = Pressure.objects.create(user=request.user, week=odor_data['week'],
                                                           weekper=odor_data['weekper'])
                        user_profile.odor.add(odor)
                        user_profile.temperature.add(temperature)
                        user_profile.light.add(light)
                        user_profile.pressure.add(pressure)

                    for odor_data in odors_data3:
                        odor = Odor.objects.create(user=request.user, month=odor_data['month'],
                                                   monthper=odor_data['monthper'])
                        temperature = Temperature.objects.create(user=request.user, month=odor_data['month'],
                                                                 monthper=odor_data['monthper'])
                        light = Light.objects.create(user=request.user, month=odor_data['month'],
                                                     monthper=odor_data['monthper'])
                        pressure = Pressure.objects.create(user=request.user, month=odor_data['month'],
                                                           monthper=odor_data['monthper'])
                        user_profile.odor.add(odor)
                        user_profile.temperature.add(temperature)
                        user_profile.light.add(light)
                        user_profile.pressure.add(pressure)

                    for odor_data in odors_data4:
                        odor = Odor.objects.create(user=request.user, year=odor_data['year'],
                                                   yearper=odor_data['yearper'])
                        temperature = Temperature.objects.create(user=request.user, year=odor_data['year'],
                                                                 yearper=odor_data['yearper'])
                        light = Light.objects.create(user=request.user, year=odor_data['year'],
                                                     yearper=odor_data['yearper'])
                        pressure = Pressure.objects.create(user=request.user, year=odor_data['year'],
                                                           yearper=odor_data['yearper'])
                        user_profile.odor.add(odor)
                        user_profile.temperature.add(temperature)
                        user_profile.light.add(light)
                        user_profile.pressure.add(pressure)

                    user_profile.save()
                    return redirect('graphsai')
                else:
                    specialist = Specialists.objects.create(user=request.user)
                    specialist.fullname = str(request.POST['name']) + " " + str(request.POST['lastname'])
                    specialist.save()

                    return redirect('index')
            except IntegrityError:
                return render(request, 'main/signupsystem.html', {'form': UserCreationForm, 'error': 'Username is already taken!'})

@login_required
def logoutsystem(request):
    if request.method == "GET":
        logout(request)
        return redirect('loginsystem')