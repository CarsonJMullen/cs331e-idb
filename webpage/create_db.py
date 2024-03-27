from models import app, db, City, Activity, Flight, Hotel
from flight_functions import create_convert_airline_cache, create_airport_to_city_cache, convert_airline, convert_duration, airport_to_city
import os
import json

# cities
with open(os.path.join(app.static_folder, 'data', 'cities', 'cities.json')) as f:
    city_list = json.load(f)['data']
f.close()

# activities
with open(os.path.join(app.static_folder, 'data', 'activities', 'activities_multiple_cities.json')) as f:
    activity_list = json.load(f)['data']
f.close()

# flights
cities = [city['iataCode'] for city in city_list]
flights = []
for city in cities:
    with open(os.path.join(app.static_folder, 'data', 'flights', city + '-2024-05-13.json')) as f:
        flights.append(json.load(f))
    f.close()

# hotels
with open(os.path.join(app.static_folder, 'data', 'hotels', 'hotel_list.json')) as f:
    hotel_list = json.load(f)['data']
f.close()

convert_airline_cache = create_convert_airline_cache()
airport_to_city_cache = create_airport_to_city_cache()

def create():
    # Populating
    # ----------
    for i in city_list:
        newCity = City(name=i['name'], iataCode=i['iataCode'], population=int(i['population'].replace(',', '')), location=i['location'], pictures=i['pictures'])
        db.session.add(newCity)
    # commit the session to my DB.
    db.session.commit()

    for i in activity_list:
        try:
            newActivity = Activity(id=int['id'], name=i['name'], description=i['description'], rating=float(i['rating']),
                               price_amount=i['price']['amount'], price_currencyCode=i['price']['currencyCode'],
                               pictures=i['pictures'], bookingLink=i['bookingLink'], iataCode=i['iataCode'])
        except:
            continue
        db.session.add(newActivity)
    db.session.commit()

    for i in hotel_list:
        newHotel = Hotel(id=i['hotelId'], name=i['name'].title(), latitude=i['geoCode']['latitude'], longitude=i['geoCode']['longitude'],
                         amenities=i['amenities'], rating=i['rating'], iataCode=i['iataCode'])
        db.session.add(newHotel)
    db.session.commit()

    id = 0
    for city in flights:
        for f in city['data']:
            newflight = Flight(id = id,
                               departure_airport = f['itineraries'][0]['segments'][0]['departure']['iataCode'],
                               arrival_airport = f['itineraries'][0]['segments'][-1]['arrival']['iataCode'],
                               arrival_city = airport_to_city(airport_to_city_cache, f['itineraries'][0]['segments'][-1]['arrival']['iataCode'])['cityCode'],
                               price = f['price']['total'],
                               seats_left = f['numberOfBookableSeats'],
                               duration = convert_duration(f['itineraries'][0]['duration']),
                               num_legs = len(f['itineraries'][0]['segments']),
                               departure_time = f['itineraries'][0]['segments'][0]['departure']['at'],
                               arrival_time = f['itineraries'][0]['segments'][-1]['arrival']['at'],
                               airline = convert_airline(convert_airline_cache, f['itineraries'][0]['segments'][0]['carrierCode'])
            )
            db.session.add(newflight)
            id += 1

    db.session.commit()

create()
