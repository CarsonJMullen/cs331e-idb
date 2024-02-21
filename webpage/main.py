from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime
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
activity_list = [
{
    "type": "activity",
    "id": "7145",
    "self": {
        "href": "https://test.api.amadeus.com/v1/shopping/activities/7145",
        "methods": [
            "GET"
        ]
    },
    "name": "Potsdam Bike Tour with Rail Transport from Berlin",
    "description": "Take a day-trip from Berlin and discover UNESCO World Heritage listed Potsdam, all by the seat of your bike! From park lands to alleyways, you're English-speaking guide will recount historical anecdotes as you explore an array of Prussian and Cold War sites.",
    "geoCode": {
        "latitude": 52.5209951,
        "longitude": 13.4091129
    },
    "rating": "4.8",
    "price": {
        "amount": "70.0",
        "currencyCode": "EUR"
    },
    "pictures": [
        "https://media.tacdn.com/media/attractions-splice-spp-674x446/07/6f/f1/21.jpg"
    ],
    "bookingLink": "http://www.partner.viator.com/en/13257/tours/Berlin/Potsdam-Day-Bike-Tour/d488-3933BIKEPOTS?eap=prod-qahHG7va6hJGURBQV5vH-13257&aid=vba13257en",
    "minimumDuration": "6 hours",
    "city": "Berlin",
    "iataCode": "BER"
},
    {
        "type": "activity",
        "id": "1747814",
        "self": {
            "href": "https://test.api.amadeus.com/v1/shopping/activities/1747814",
            "methods": [
                "GET"
            ]
        },
        "name": "Compagnie des Bateaux Mouches Bastille Day Seine River Dinner Cruise",
        "description": "Have a Champagne dinner cruise, taste a French traditional cooking, prepared on board by our own chef. Enjoy a 2h15 magic cruise with live music! At the end of the dinner, make yourself comfortable and watch the firework display from the upper-deck.",
        "geoCode": {
            "latitude": 48.86401059999999,
            "longitude": 2.3059374
        },
        "rating": "4.3",
        "price": {
            "amount": "195.0",
            "currencyCode": "EUR"
        },
        "pictures": [
            "https://media.tacdn.com/media/attractions-splice-spp-674x446/06/70/07/58.jpg"
        ],
        "bookingLink": "http://www.partner.viator.com/en/13257/tours/Paris/Bastille-day-dinner-cruise/d479-23561P13?eap=prod-sRa7AtLuF4UkLYO6mKPY-13257&aid=vba13257en",
        "minimumDuration": "2 hours",
        "city": "Paris",
        "iataCode": "PAR"
    },
    {
        "type": "activity",
        "id": "53568",
        "self": {
            "href": "https://test.api.amadeus.com/v1/shopping/activities/53568",
            "methods": [
                "GET"
            ]
        },
        "name": "New York City Rockstar Bar and Nightclub Crawl",
        "description": "Enjoy a fabulous night out in New York City on this all-inclusive bar crawl. Join your party host and take advantage of NYC's electrifying nightlife as you visit several bars and clubs for drinks and dancing.",
        "geoCode": {
            "latitude": 40.73527429999999,
            "longitude": -74.0056814
        },
        "rating": "4.6",
        "price": {
            "amount": "81.0",
            "currencyCode": "USD"
        },
        "pictures": [
            "https://media.tacdn.com/media/attractions-splice-spp-674x446/06/6f/03/5d.jpg"
        ],
        "bookingLink": "http://www.partner.viator.com/en/13257/tours/New-York-City/Rockstarcrawls-NYC-Bar-Crawl/d687-5511P8?eap=prod-W8SNN6s2Yp6jQIueqwfW-13257&aid=vba13257en",
        "minimumDuration": "5 hours",
        "city": "New York",
        "iataCode": "NYC"
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
    }
]


json_file_path = os.path.join(app.static_folder, 'data', 'flights', 'AUS-NYC-24-02-17.json')
with open(json_file_path) as f:
    ny_flights = json.load(f)


def convert_airline(s):
    d = ny_flights['dictionaries']['carriers']
    if s in d:
        return d[s]
    else:
        return "Unknown"
    
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


@app.route('/flights/')
def flights():
    prices = [flight['price']['total'] for flight in ny_flights['data']]
    seats = [flight['numberOfBookableSeats'] for flight in ny_flights['data']]
    durations = [convert_duration(flight['itineraries'][0]['duration']) for flight in ny_flights['data']]
    segments_count = [len(flight['itineraries'][0]['segments']) for flight in ny_flights['data']]
    departure_iata = [flight['itineraries'][0]['segments'][0]['departure']['iataCode'] for flight in ny_flights['data']]
    departure_time = [datetime.fromisoformat(flight['itineraries'][0]['segments'][0]['arrival']['at']).strftime("%I:%M %p") for flight in ny_flights['data']]
    arrival_iata = [flight['itineraries'][0]['segments'][-1]['arrival']['iataCode'] for flight in ny_flights['data']]
    arrival_time = [datetime.fromisoformat(flight['itineraries'][0]['segments'][-1]['arrival']['at']).strftime("%I:%M %p %m-%d-%Y") for flight in ny_flights['data']]
    airlines = [convert_airline(flight['itineraries'][0]['segments'][0]['carrierCode']) for flight in ny_flights['data']]

    # Zipping all the lists together
    table_data = zip(departure_iata, arrival_iata, prices, seats, durations, segments_count, departure_time,  arrival_time, airlines)

    return render_template('flights.html', flights = ny_flights['data'], convert_duration = convert_duration, convert_airline = convert_airline)

@app.route('/hotels/<string:hotel_id>')
def this_hotel(hotel_id):
    for i in hotel_list:
        if i['hotelId'] == hotel_id:
            return render_template('this_hotel.html', hotel=i)
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
