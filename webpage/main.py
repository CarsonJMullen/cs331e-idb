from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from user_info import get_gitlab_info, user_all_info, group_gitlab_info
from static.constants import data_source, tools, postman_api
from models import City, Activity, Flight, Hotel, FlightDetails
from flask_sqlalchemy import SQLAlchemy

# Google Cloud SQL (change this accordingly)
USER = "postgres"
PASSWORD = "postgres"
# PUBLIC_IP_ADDRESS = "35.223.216.248"
PUBLIC_IP_ADDRESS = "localhost"
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


def select_dict(model, attr=None, value=None, page_limit=None, page=1, order_by=None, desc=False):
    stmt = db.select(model)
    # Filter
    if attr and value != "0":
        stmt = stmt.where(attr == value)

    # Page limit
    if page_limit:
        stmt = stmt.limit(page_limit).offset((page-1)*10)

    # Sort
    if order_by:
        if desc:
            stmt = stmt.order_by(order_by.desc())
        else:
            stmt = stmt.order_by(order_by)

    # Convert SQLAlchemy object to a dictionary
    res = {}
    for i in db.session.execute(stmt):
        i_dict = i[0].__dict__
        obj_dict = {}
        for key in i_dict:
            if not key.startswith('_'):
                obj_dict[key] = getattr(i[0], key)
        res[i_dict['id']] = obj_dict
    return res

def select_distinct(attr):
    stmt = db.select(attr).distinct()
    res = []
    for i in db.session.execute(stmt):
        res.append(i[0])
    return res


# cities
city_list = select_dict(City)

# flights
flights_list = select(Flight)
flight_details = select(FlightDetails)

# hotels
hotel_list = select_dict(Hotel)


@app.route('/')
@app.route('/home/')
def index():
    return render_template('index.html')


@app.route('/cities/<string:iataCode>')
def city(iataCode):
    activity_list = select_dict(Activity, Activity.iataCode, iataCode, page_limit=10, order_by=Activity.rating, desc=True)
    hotel_list = select_dict(Hotel, Hotel.iataCode, iataCode, page_limit=10, order_by=Hotel.rating, desc=True)
    return render_template('city.html', city=city_list[iataCode], activity_list=activity_list, hotel_list=hotel_list)


@app.route('/cities/order_by=<order_by>&desc=<int:desc>')
def cities(order_by, desc):
    city_list = select_dict(City, order_by=getattr(City, order_by), desc=desc)
    return render_template('cities.html', city_list=city_list, order_by=order_by, desc=desc)


@app.route('/activities/id=<int:activity_id>')
def activity(activity_id):
    activity_list = select_dict(Activity)
    return render_template('activity.html', activity=activity_list[str(activity_id)])


@app.route('/activities/page=<int:page>&order_by=<order_by>&desc=<int:desc>&attr=<attr>&value=<value>')
def activities(page, order_by, desc, attr, value):
    activity_list = select_dict(Activity, page_limit=10, page=page, order_by=getattr(Activity, order_by), desc=desc, attr=getattr(Activity, attr), value=value)
    count = len(select_dict(Activity, attr=getattr(Activity, attr), value=value))
    curr_list = select_distinct(Activity.price_currencyCode)
    return render_template('activities.html', city_list=city_list, activity_list=activity_list, curr_list=curr_list, count=count, page=page, order_by=order_by, desc=desc, attr=attr, value=value)


@app.route('/flights/<string:flight_id>')
def single_flight(flight_id):
    for i in range(len(flights_list)):
        if str(flights_list[i]['id']) == str(flight_id):
            return render_template('single_flight.html', flight=flights_list[i],
                                   fd=[d for d in flight_details if str(d['flight_group']) == str(flight_id)])
    return render_template('flights.html', flights=flights_list, page=1)

@app.route('/flights/page=<int:page>&order_by=<order_by>&desc=<int:desc>&attr=<attr>&value=<value>')
def flights(page, order_by, desc, attr, value):
    flight_list_limit = select_dict(Flight, page_limit=10, page=page, order_by=getattr(Flight, order_by), desc=desc, attr=getattr(Flight, attr), value=value)
    count = len(select_dict(Flight, attr=getattr(Flight, attr), value=value))
    airline_list = select_distinct(Flight.airline)
    return render_template('flights.html', city_list=city_list, flight_list = flight_list_limit.values(), airline_list=airline_list, count=count, page=page, order_by=order_by, desc=desc, attr=attr, value=value)

@app.route('/hotels/id=<string:hotel_id>')
def this_hotel(hotel_id):
    activity_list = select_dict(Activity, Activity.iataCode, hotel_list[str(hotel_id)]['iataCode'], page_limit=10, order_by=Activity.rating, desc=True)
    return render_template('this_hotel.html', hotel=hotel_list[str(hotel_id)], activity_list=activity_list)


@app.route('/hotels/page=<int:page>&order_by=<order_by>&desc=<int:desc>&attr=<attr>&value=<value>')
def hotels(page, order_by, desc, attr, value):
    hotel_list_filtered = select_dict(Hotel, page_limit=10, page=page, order_by=getattr(Hotel, order_by), desc=desc, attr=getattr(Hotel, attr), value=value)
    count = len(select_dict(Hotel, attr=getattr(Hotel, attr), value=value))
    return render_template('hotels.html', city_list=city_list ,hotel_list=hotel_list_filtered, count=count, page=page, order_by=order_by, desc=desc, attr=attr, value=value)


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
