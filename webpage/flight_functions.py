from models import app
import os
import json

with open(os.path.join(app.static_folder, 'data', 'cities', 'cities.json')) as f:
    city_list = json.load(f)['data']
f.close()

cities = [city['iataCode'] for city in city_list]
flights = []

for city in cities:
    with open(os.path.join(app.static_folder, 'data', 'flights', city + '-2024-05-13.json')) as f:
        flights.append(json.load(f))
    f.close()

def create_convert_airline_cache():
    full_d = {}
    for flights_list in flights:
        d = flights_list['dictionaries']['carriers']
        full_d = {**full_d, **d}
    return full_d

def create_airport_to_city_cache():
    full_d = {}
    for flights_list in flights:
        d = flights_list['dictionaries']['locations']
        full_d = {**full_d, **d}
    return full_d

def convert_airline(d, s):
    if s in d:
        return d[s]
    else:
        return "Unknown"

def airport_to_city(d, airport):
    if airport in d:
        return d[airport]
    else:
        return airport

def convert_duration(duration):
    # Remove the 'PT' prefix
    duration = duration[2:]

    hours = 0
    minutes = 0

    if 'H' in duration:
        hours_index = duration.index('H')
        hours = int(duration[:hours_index])
        duration = duration[hours_index + 1:]

    if 'M' in duration:
        minutes_index = duration.index('M')
        minutes = int(duration[:minutes_index])

    # Format the hours and minutes into HH:MM
    formatted_time = '{:02d}:{:02d}'.format(hours, minutes)

    return formatted_time


