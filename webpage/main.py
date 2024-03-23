from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from user_info import get_gitlab_info, user_all_info, group_gitlab_info
from static.constants import data_source, tools

app = Flask(__name__)

hotel_list = [
    { # this hotel is not in hotel_list.json
        "chainCode": "DS",
        "iataCode": "BER",
        "dupeId": 700140863,
        "name": "COSMO HOTEL",
        "hotelId": "DSBERCHB",
        "geoCode": {
            "latitude": 52.51167,
            "longitude": 13.4014
        },
        "address": {
            "countryCode": "DE"
        },
        "distance": {
            "value": 17.97,
            "unit": "KM"
        },
        "amenities": [
            "AIR_CONDITIONING",
            "WIFI",
            "ROOM_SERVICE"
        ],
        "rating": 5,
        "lastUpdate": "2023-06-15T10:15:56"
    },
    {
        "chainCode": "LW",
        "iataCode": "NYC",
        "dupeId": 700113468,
        "name": "THE GREENWICH HOTEL",
        "hotelId": "LWNYC730",
        "geoCode": {
            "latitude": 40.71985,
            "longitude": -74.01022
        },
        "address": {
            "countryCode": "US"
        },
        "distance": {
            "value": 0.73,
            "unit": "KM"
        },
        "amenities": [
            "AIR_CONDITIONING",
            "WIFI",
            "ROOM_SERVICE"
        ],
        "rating": 5,
        "lastUpdate": "2023-06-15T10:12:33"
    },
    {
        "chainCode": "DC",
        "iataCode": "PAR",
        "dupeId": 700010162,
        "name": "LE MEURICE",
        "hotelId": "DCPAR625",
        "geoCode": {
            "latitude": 48.86512,
            "longitude": 2.32777
        },
        "address": {
            "countryCode": "FR"
        },
        "distance": {
            "value": 2.02,
            "unit": "KM"
        },
        "amenities": [
            "AIR_CONDITIONING",
            "WIFI",
            "ROOM_SERVICE"
        ],
        "rating": 5,
        "lastUpdate": "2023-06-15T09:55:00"
    }
]

########################################################################################################################
#                                           load data                                                                  #
########################################################################################################################
# cities
with open(os.path.join(app.static_folder, 'data', 'cities', 'cities.json')) as f:
    city_list = json.load(f)['data']
f.close()

# activities
with open(os.path.join(app.static_folder, 'data', 'activities', 'activities_multiple_cities.json')) as f:
    activity_list = json.load(f)['data']
f.close()

# flights
with open(os.path.join(app.static_folder, 'data', 'flights', 'AUS-NYC-24-02-17.json')) as f:
    ny_flights = json.load(f)
f.close()

with open(os.path.join(app.static_folder, 'data', 'flights', 'AUS-BER-24-02-17.json')) as f:
    ber_flights = json.load(f)
f.close()

with open(os.path.join(app.static_folder, 'data', 'flights', 'AUS-PAR-24-02-17.json')) as f:
    par_flights = json.load(f)
f.close()

locations_list = [ny_flights, ber_flights, par_flights]
# print(locations_list)
flights_list = locations_list[0] # this only reads ny_flights


# print(flights_list["data"])

def convert_airline(s):
    d = flights_list['dictionaries']['carriers']
    if s in d:
        return d[s]
    else:
        return "Unknown"


def airport_to_city(airport):
    d = flights_list['dictionaries']['locations']

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


@app.route('/')
@app.route('/home/')
def index():
    return render_template('index.html')


@app.route('/cities/<string:iataCode>')
def city(iataCode):
    for i in city_list:
        if i['iataCode'] == str(iataCode):
            return render_template('city.html', city=i, activity_list=activity_list, hotel_list=hotel_list)
    return render_template('cities.html', city_list=city_list)


@app.route('/cities/')
def cities():
    return render_template('cities.html', city_list=city_list)


@app.route('/activities/id=<int:activity_id>')
def activity(activity_id):
    for i in activity_list:
        if i['id'] == str(activity_id):
            return render_template('activity.html', activity=i)
    return render_template('activities.html', activity_list=activity_list, page=0)


@app.route('/activities/page=<int:page>')
def activities(page=3):
    activities_page = page
    return render_template('activities.html', activity_list=activity_list, page=activities_page)


@app.route('/flights/<string:flight_id>')
def single_flight(flight_id):
    for f in flights_list['data']:
        if f['id'] == str(flight_id):
            itineraries = f['itineraries']
            return render_template('single_flight.html', flight=f, convert_duration=convert_duration,
                                   convert_airline=convert_airline, airport_to_city=airport_to_city,
                                   activity_list=activity_list, hotel_list=hotel_list, itineraries=itineraries)
    return render_template('flights.html', flights=flights_list['data'], convert_duration=convert_duration,
                           convert_airline=convert_airline, airport_to_city=airport_to_city)


@app.route('/flights/')
def flights():
    return render_template('flights.html', flights=flights_list['data'], convert_duration=convert_duration,
                           convert_airline=convert_airline, airport_to_city=airport_to_city)


@app.route('/hotels/<string:hotel_id>')
def this_hotel(hotel_id):
    for i in hotel_list:
        if i['hotelId'] == hotel_id:
            return render_template('this_hotel.html', hotel=i, activity_list=activity_list)
    return render_template('hotels.html', hotel_list=hotel_list)


@app.route('/hotels/')
def hotels():
    return render_template('hotels.html', hotel_list=hotel_list)


@app.route('/about/')
def about():
    all_stats = get_gitlab_info()
    member_stats = user_all_info(all_stats)
    group_stats = group_gitlab_info(all_stats)

    return render_template('about.html', group_stats=group_stats, member_stats=member_stats, data_source=data_source,
                           tools=tools)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
