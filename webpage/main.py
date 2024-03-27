from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from user_info import get_gitlab_info, user_all_info, group_gitlab_info
from static.constants import data_source, tools
from models import City, Activity, Flight, Hotel
from flask_sqlalchemy import SQLAlchemy

# Google Cloud SQL (change this accordingly)
USER = "postgres"
PASSWORD = "postgres"
PUBLIC_IP_ADDRESS ="35.223.216.248"
# PUBLIC_IP_ADDRESS = "localhost"
DBNAME = "toptraveldb"

# Configuration
# One-To-Many relation: Assume that a Publisher can have many Books
# but a Book can only have one Publisher.
app = Flask(__name__)

app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_STRING",
                                                       f'postgresql://{USER}:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # to suppress a warning message
db = SQLAlchemy(app)

########################################################################################################################
#                                           load data                                                                  #
########################################################################################################################
def select(model):
    stmt = db.select(model)
    res = []
    for i in db.session.execute(stmt):
        res.append(i[0].__dict__)
    return res

########################################################################################################################
#                                           load data                                                                  #
########################################################################################################################
# cities
with open(os.path.join(app.static_folder, 'data', 'cities', 'cities.json')) as f:
    city_list = json.load(f)['data']
f.close()

# activities
activity_list = select(Activity)

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

# hotels 
with open(os.path.join(app.static_folder, 'data', 'hotels', 'hotel_list.json')) as f:
    hotel_list = json.load(f)['data']
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
    return render_template('activities.html', activity_list=activity_list, page=1)


@app.route('/activities/page=<int:page>')
def activities(page=1):
    return render_template('activities.html', activity_list=activity_list, page=page)


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


@app.route('/hotels/id=<string:hotel_id>')
def this_hotel(hotel_id):
    for i in hotel_list:
        if i['hotelId'] == hotel_id:
            return render_template('this_hotel.html', hotel=i, activity_list=activity_list)
    return render_template('hotels.html', hotel_list=hotel_list, page=1)


@app.route('/hotels/page=<int:page>')
def hotels(page=1):
    return render_template('hotels.html', hotel_list=hotel_list, page=page)


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
