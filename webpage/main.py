from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from user_info import get_gitlab_info, user_all_info, group_gitlab_info
from static.constants import data_source, tools

app = Flask(__name__)

hotel_list = [
{
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

city_list = [
    {
        'name': 'Berlin',
        'id': '1',
        'population': '3,769,495',
        'location': 'Germany',
        'pictures': [
            'https://upload.wikimedia.org/wikipedia/commons/4/4b/Museumsinsel_Berlin_Juli_2021_1_%28cropped%29.jpg'
        ],
        'iataCode': 'BER'
    },
    {
        'name': 'Paris',
        'id': '2',
        'population': '11,276,701',
        'location': 'France',
        'pictures': [
            'https://upload.wikimedia.org/wikipedia/commons/4/4b/La_Tour_Eiffel_vue_de_la_Tour_Saint-Jacques%2C_Paris_ao%C3%BBt_2014_%282%29.jpg'
        ],
        'iataCode': 'PAR'
    },
    {
        'name': 'New York City',
        'id': '3',
        'population': '8,804,190',
        'location': 'United States of America',
        'pictures': [
            'https://upload.wikimedia.org/wikipedia/commons/7/7a/View_of_Empire_State_Building_from_Rockefeller_Center_New_York_City_dllu_%28cropped%29.jpg'
        ],
        'iataCode': 'NYC'
    },
    {
        'name': 'Rome',
        'id': '4',
        'population': '4,355,725',
        'location': 'Italy',
        'pictures': [
            'https://upload.wikimedia.org/wikipedia/commons/0/0b/Rome_skyline_panorama.jpg'
        ],
        'iataCode': 'FCO'
    },
    {
        'name': 'Cape Town',
        'population': '4,977,833',
        'location': 'South Africa',
        'pictures': [
            'https://upload.wikimedia.org/wikipedia/commons/f/fb/Cape_Town_Mountain.jpg'
        ],
        'iataCode': 'CPT'
    },
    {
        'name': 'Sydney',
        'population': '5,297,089',
        'location': 'Australia',
        'pictures': [
            'https://upload.wikimedia.org/wikipedia/commons/5/53/Sydney_Opera_House_and_Harbour_Bridge_Dusk_%282%29_2019-06-21.jpg'
        ],
        'iataCode': 'SYD'
    },
    {
        'name': 'Amsterdam',
        'population': '821,752',
        'location': 'Netherlands',
        'pictures': [
            'https://upload.wikimedia.org/wikipedia/commons/5/57/Imagen_de_los_canales_conc%C3%A9ntricos_en_%C3%81msterdam.png'
        ],
        'iataCode': 'AMS'
    },
    {
        'name': 'London',
        'population': '9,748,033',
        'location': 'England',
        'pictures': [
            'https://upload.wikimedia.org/wikipedia/commons/6/67/London_Skyline_%28125508655%29.jpeg'
        ],
        'iataCode': 'LON'
    },
    {
        'name': 'Barcelona',
        'population': '5,711,917',
        'location': 'Spain',
        'pictures': [
            'https://upload.wikimedia.org/wikipedia/commons/5/56/Aerial_view_of_Barcelona%2C_Spain_%2851227309370%29_%28cropped%29.jpg'
        ],
        'iataCode': 'BCN'
    },
    {
        'name': 'Mexico City',
        'population': '9,209,944',
        'location': 'Mexico',
        'pictures': [
            'https://upload.wikimedia.org/wikipedia/commons/4/4f/Sobrevuelos_CDMX_HJ2A4913_%2825514321687%29_%28cropped%29.jpg'
        ],
        'iataCode': 'EZE'
    },
    {
        'name': 'Athens',
        'population': '3,154,591',
        'location': 'Greece',
        'pictures': [
            'https://upload.wikimedia.org/wikipedia/commons/e/e4/The_Acropolis_from_Mount_Lycabettus_on_October_5%2C_2019_%28cropped%29.jpg'
        ],
        'iataCode': 'ATH'
    },
    {
        'name': 'Madrid',
        'population': '6,825,005',
        'location': 'Spain',
        'pictures': [
            'https://upload.wikimedia.org/wikipedia/commons/1/14/Madrid_-_Sky_Bar_360%C2%BA_%28Hotel_Riu_Plaza_Espa%C3%B1a%29%2C_vistas_19.jpg'
        ],
        'iataCode': 'MAD'
    },
]

with open(os.path.join(app.static_folder, 'data', 'activities', 'activities_multiple_cities.json')) as f:
    activity_list = json.load(f)['data']

with open(os.path.join(app.static_folder, 'data', 'flights', 'AUS-NYC-24-02-17.json')) as f:
    ny_flights = json.load(f)

with open(os.path.join(app.static_folder, 'data', 'flights', 'AUS-BER-24-02-17.json')) as f:
    ber_flights = json.load(f)

with open(os.path.join(app.static_folder, 'data', 'flights', 'AUS-PAR-24-02-17.json')) as f:
    par_flights = json.load(f)

locations_list = [ny_flights, ber_flights, par_flights]
flights_list = locations_list[0]

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

@app.route('/activities/<int:activity_id>')
def activity(activity_id):
    for i in activity_list:
        if i['id'] == str(activity_id):
            return render_template('activity.html', activity=i)
    return render_template('activities.html', activity_list=activity_list)

@app.route('/activities/')
def activities():

    return render_template('activities.html', activity_list=activity_list)

@app.route('/flights/<string:flight_id>')
def single_flight(flight_id):

    for f in flights_list['data']:
        if f['id'] == str(flight_id):
            itineraries = f['itineraries']
            return render_template('single_flight.html', flight=f, convert_duration = convert_duration, convert_airline = convert_airline, airport_to_city=airport_to_city, activity_list = activity_list, hotel_list = hotel_list, itineraries=itineraries)
    return render_template('flights.html', flights = flights_list['data'], convert_duration = convert_duration, convert_airline = convert_airline, airport_to_city=airport_to_city)

@app.route('/flights/')
def flights():
    return render_template('flights.html', flights = flights_list['data'], convert_duration = convert_duration, convert_airline = convert_airline, airport_to_city=airport_to_city)

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

    return render_template('about.html', group_stats=group_stats, member_stats=member_stats, data_source=data_source, tools=tools)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
