from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from user_info import get_gitlab_info, user_all_info, group_gitlab_info
from static.constants import data_source, tools, postman_api
from models import City, Activity, Flight, Hotel, FlightDetails
from flask_sqlalchemy import SQLAlchemy
import unittest
from test import run

# Google Cloud SQL (change this accordingly)
USER = "postgres"
PASSWORD = "postgres"
PUBLIC_IP_ADDRESS ="35.223.216.248"
#PUBLIC_IP_ADDRESS = "localhost"
DBNAME = "toptraveldb"

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
        # Convert SQLAlchemy object to a dictionary
        obj_dict = {}
        for key in i[0].__dict__:
            if not key.startswith('_'):
                obj_dict[key] = getattr(i[0], key)
        res.append(obj_dict)
    return res

# cities
city_list = select(City)
activity_list = select(Activity)

# flights
flights_list = select(Flight)
flight_details = select(FlightDetails)

# hotels
hotel_list = select(Hotel)

# with open(os.path.join(app.static_folder, 'data', 'hotels', 'hotel_list.json')) as f:
#     hotel_list = json.load(f)['data']
# f.close()

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
    for i in range(len(flights_list)):
        if str(flights_list[i]['id']) == str(flight_id):
            return render_template('single_flight.html', flight = flights_list[i], fd = [d for d in flight_details if str(d['flight_group']) == str(flight_id)])
    return render_template('flights.html', flights=flights_list, page = 1)


@app.route('/flights/page=<int:page>')
def flights(page=1):
    return render_template('flights.html', flights=flights_list, page = page)


@app.route('/hotels/id=<string:hotel_id>')
def this_hotel(hotel_id):
    for i in hotel_list:
        if i['id'] == hotel_id:
            return render_template('this_hotel.html', hotel=i, activity_list=activity_list)
    return render_template('hotels.html', hotel_list=hotel_list, page=1)


@app.route('/hotels/page=<int:page>')
def hotels(page=1):
    return render_template('hotels.html', hotel_list=hotel_list, page=page)

# Define API Endpoints
@app.route('/activities/get/', methods=['GET'])
def get_activities():
    city_filter = request.args.get('city')
    if city_filter:
        filtered_activities = [activity for activity in activity_list if activity['iataCode'] == city_filter]
        return jsonify(filtered_activities)
    else:
        return jsonify(activity_list)

@app.route('/hotels/get/', methods=['GET'])
def get_hotels():
    city_filter = request.args.get('city')
    if city_filter:
        filtered_hotels = [h for h in hotel_list if h['iataCode'] == city_filter]
        return jsonify(filtered_hotels)
    else:
        return jsonify(hotel_list)

@app.route('/flights/get/', methods=['GET'])
def get_flights():
    city_filter = request.args.get('city')
    if city_filter:
        filtered_flights = [f for f in flights_list if f['arrival_city'] == city_filter]
        return jsonify(filtered_flights)
    else:
        return jsonify(flights_list)

@app.route('/flight_details/get/', methods=['GET'])
def get_flightdetails():
    return jsonify(flight_details)

@app.route('/cities/get/', methods=['GET'])
def get_cities():
    return jsonify(city_list)

@app.route('/about/')
def about():
    all_stats = get_gitlab_info()
    member_stats = user_all_info(all_stats)
    group_stats = group_gitlab_info(all_stats)

    return render_template('about.html', group_stats=group_stats, member_stats=member_stats, data_source=data_source,
                           tools=tools, postman_api=postman_api)

@app.route('/unittest/')
def unittest():
    return render_template('unittest.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
