from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, abort
import json
import os
from user_info import for_about_page
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

def select(model, attr=None, value=None, page_limit=None, page=1, order_by=None, desc=False, search=None):
    stmt = db.select(model)
    # Filter
    if attr and value != "0":
        stmt = stmt.where(attr == value)

    # Page limit
    if page_limit:
        stmt = stmt.limit(page_limit).offset((page-1)*12)

    # Sort
    if order_by:
        if desc:
            stmt = stmt.order_by(order_by.desc())
        else:
            stmt = stmt.order_by(order_by)

    # Search
    if search != '00' and search:
        for i in search.split():
            if model == Activity:
                stmt = stmt.filter(model.name.ilike(f'%{i}%') | model.description.ilike(f'%{i}%'))
            elif model == Hotel:
                stmt = stmt.filter(model.name.ilike(f'%{i}%'))

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
city_list = select(City)

# flights
flights_list = select(Flight)
flight_details = select(FlightDetails)

# hotels
hotel_list = select(Hotel)


@app.route('/')
@app.route('/home/')
def index():
    return render_template('index.html')


@app.route('/cities/<string:iataCode>')
def city(iataCode):
    activity_list = select(Activity, Activity.iataCode, iataCode, page_limit=10, order_by=Activity.rating, desc=True)
    hotel_list = select(Hotel, Hotel.iataCode, iataCode, page_limit=10, order_by=Hotel.rating, desc=True)
    return render_template('city.html', city=city_list[iataCode], activity_list=activity_list, hotel_list=hotel_list)


@app.route('/cities/order_by=<order_by>&desc=<int:desc>')
def cities(order_by, desc):
    city_list = select(City, order_by=getattr(City, order_by), desc=desc)
    return render_template('cities.html', city_list=city_list, order_by=order_by, desc=desc)


@app.route('/activities/id=<int:activity_id>')
def activity(activity_id):
    activity_list = select(Activity)
    return render_template('activity.html', activity=activity_list[str(activity_id)])


@app.route('/activities/page=<int:page>&order_by=<order_by>&desc=<int:desc>&attr=<attr>&value=<value>&search=<search>', methods=['GET', 'POST'])
def activities(page, order_by, desc, attr, value, search):
    if request.method == 'POST':
        search = request.form['search']
        if search == '':
            search = '00'
    activity_list = select(Activity, page_limit=12, page=page, order_by=getattr(Activity, order_by), desc=desc, attr=getattr(Activity, attr), value=value, search=search)
    count = len(select(Activity, attr=getattr(Activity, attr), value=value, search=search))
    curr_list = select_distinct(Activity.price_currencyCode)
    return render_template('activities.html', city_list=city_list, activity_list=activity_list, curr_list=curr_list, count=count, page=page, order_by=order_by, desc=desc, attr=attr, value=value, search=search)

@app.route('/flights/<int:flight_id>')
def single_flight(flight_id):
    flight_details = select(FlightDetails, attr=FlightDetails.flight_group, value=flight_id)
    return render_template('single_flight.html', flight=flights_list[flight_id], fd=flight_details.values())

@app.route('/flights/page=<int:page>&order_by=<order_by>&desc=<int:desc>&attr=<attr>&value=<value>')
def flights(page, order_by, desc, attr, value):
    flight_list_limit = select(Flight, page_limit=10, page=page, order_by=getattr(Flight, order_by), desc=desc, attr=getattr(Flight, attr), value=value)
    count = len(select(Flight, attr=getattr(Flight, attr), value=value))
    airline_list = select_distinct(Flight.airline)
    return render_template('flights.html', city_list=city_list, flight_list = flight_list_limit.values(), airline_list=airline_list, count=count, page=page, order_by=order_by, desc=desc, attr=attr, value=value)

@app.route('/hotels/id=<string:hotel_id>')
def this_hotel(hotel_id):
    activity_list = select(Activity, Activity.iataCode, hotel_list[str(hotel_id)]['iataCode'], page_limit=10, order_by=Activity.rating, desc=True)
    return render_template('this_hotel.html', hotel=hotel_list[str(hotel_id)], activity_list=activity_list)


@app.route('/hotels/page=<int:page>&order_by=<order_by>&desc=<int:desc>&attr=<attr>&value=<value>&search=<search>', methods=['GET', 'POST'])
def hotels(page, order_by, desc, attr, value, search):
    if request.method == 'POST':
        search = request.form['search']
        if search == '':
            search = '00'
    hotel_list_filtered = select(Hotel, page_limit=12, page=page, order_by=getattr(Hotel, order_by), desc=desc, attr=getattr(Hotel, attr), value=value, search=search)
    count = len(select(Hotel, attr=getattr(Hotel, attr), value=value, search=search))
    return render_template('hotels.html', city_list=city_list ,hotel_list=hotel_list_filtered, count=count, page=page, order_by=order_by, desc=desc, attr=attr, value=value, search=search)


# Define API Endpoints

@app.route('/activities/get/', methods=['GET'])
def get_activities():
    city_filter = request.args.get('city')
    id_filter = request.args.get('id')
    rating_filter = request.args.get('rating')
    price_filter = request.args.get('price')
    currency_filter = request.args.get('currency')

    activities = db.session.query(Activity)
    if city_filter:
        activities = activities.filter_by(iataCode = city_filter)
    if id_filter:
        activities = activities.filter_by(id = id_filter)
    if rating_filter:
        activities = activities.filter(Activity.rating >= rating_filter)
    if price_filter:
        activities = activities.filter(Activity.price_amount <= price_filter)
    if currency_filter:
        activities = activities.filter_by(price_currencyCode = currency_filter)
        
    response = []
    for activity in activities:
        response.append({
            'id': activity.id, 
            'name': activity.name,
            'description': activity.description,
            'rating': activity.rating,
            'price_amount': activity.price_amount,
            'price_currencyCode': activity.price_currencyCode,
            'pictures': activity.pictures,
            'bookingLink': activity.bookingLink,
            'iataCode': activity.iataCode
        })
    return make_response({'activities':response}, 200)


@app.route('/activities/get/<int:a_id>/', methods=['GET'])
def get_one_activity(a_id):
    activity = db.session.query(Activity).filter_by(id = str(a_id)).first()
    response = {
        'id': activity.id, 
        'name': activity.name,
        'description': activity.description,
        'rating': activity.rating,
        'price_amount': activity.price_amount,
        'price_currencyCode': activity.price_currencyCode,
        'pictures': activity.pictures,
        'bookingLink': activity.bookingLink,
        'iataCode': activity.iataCode
    }
    return make_response(response, 200)


@app.route('/hotels/get/', methods=['GET'])
def get_hotels():

    hotels = db.session.query(Hotel)
    
    city_filter = request.args.get('city')
    id_filter = request.args.get('id')
    rating_filter = request.args.get('rating')

    if city_filter:
        hotels = hotels.filter_by(iataCode = city_filter)
    if id_filter:
        hotels = hotels.filter_by(id = id_filter)
    if rating_filter:
        hotels = hotels.filter(Hotel.rating >= rating_filter)
        
    response = []
    for hotel in hotels:
        response.append({
            'id': hotel.id, 
            'name': hotel.name,
            'latitude': hotel.latitude,
            'longitude': hotel.longitude,
            'amenities': hotel.amenities,
            'rating': hotel.rating,
            'iataCode': hotel.iataCode
        })
    return make_response({'hotels':response}, 200)


@app.route('/hotels/get/<string:h_id>/', methods=['GET'])
def get_one_hotel(h_id):
    hotel = db.session.query(Hotel).filter_by(id = h_id).first_or_404()
    response = {
            'id': hotel.id, 
            'name': hotel.name,
            'latitude': hotel.latitude,
            'longitude': hotel.longitude,
            'amenities': hotel.amenities,
            'rating': hotel.rating,
            'iataCode': hotel.iataCode
    }
    return make_response(response, 200)


@app.route('/flights/get/', methods=['GET'])
def get_flights():
    flights = db.session.query(Flight)
    
    city_filter = request.args.get('city')
    id_filter = request.args.get('id')
    airline_filter = request.args.get('airline')

    if city_filter:
        flights = flights.filter_by(arrival_city = city_filter)
    if id_filter:
        flights = flights.filter_by(id = id_filter)
    if airline_filter:
        flights = flights.filter_by(airline=airline_filter)
    
    response = []
    for flight in flights:
        response.append({
            'id': flight.id, 
            'departure_airport': flight.departure_airport,
            'arrival_airport': flight.arrival_airport,
            'arrival_city': flight.arrival_city,
            'price': flight.price,
            'seats_left': flight.seats_left,
            'duration': flight.duration,
            'num_legs': flight.num_legs,
            'departure_time': flight.departure_time,
            'arrival_time': flight.arrival_time,
            'airline': flight.airline
        })
    return make_response({'flights':response}, 200)


@app.route('/flights/get/<int:f_id>/', methods=['GET'])
def get_one_flight(f_id):
    flight = db.session.query(Flight).filter_by(id = str(f_id)).first_or_404()
    response = {
            'id': flight.id, 
            'departure_airport': flight.departure_airport,
            'arrival_airport': flight.arrival_airport,
            'arrival_city': flight.arrival_city,
            'price': flight.price,
            'seats_left': flight.seats_left,
            'duration': flight.duration,
            'num_legs': flight.num_legs,
            'departure_time': flight.departure_time,
            'arrival_time': flight.arrival_time,
            'airline': flight.airline
    }
    return make_response(response, 200)


@app.route('/flight_details/get/', methods=['GET'])
def get_flightdetails():
    flight_details = db.session.query(FlightDetails)
    
    id_filter = request.args.get('id')
    group_filter = request.args.get('group')
    airline_filter = request.args.get('airline')

    if id_filter:
        flight_details = flight_details.filter_by(id = id_filter)
    if airline_filter:
        flight_details = flight_details.filter_by(airline = airline_filter)
    if group_filter:
        flight_details = flight_details.filter_by(flight_group = group_filter)
    
    response = []
    for flight_detail in flight_details:
        response.append({
            'id': flight_detail.id, 
            'flight_group': flight_detail.flight_group,
            'flight_number': flight_detail.flight_number,
            'departure_airport': flight_detail.departure_airport,
            'departure_time': flight_detail.departure_time,
            'arrival_airport': flight_detail.arrival_airport,
            'arrival_time': flight_detail.arrival_time,
            'arrival_terminal': flight_detail.arrival_terminal,
            'flight_duration': flight_detail.flight_duration,
            'airline': flight_detail.airline
        })
    return make_response({'flight_details':response}, 200)

@app.route('/flight_details/get/<int:fd_id>/', methods=['GET'])
def get_one_flight_detail(fd_id):
    flight_detail = db.session.query(FlightDetails).filter_by(id = str(fd_id)).first_or_404()
    response = {
            'id': flight_detail.id, 
            'flight_group': flight_detail.flight_group,
            'flight_number': flight_detail.flight_number,
            'departure_airport': flight_detail.departure_airport,
            'departure_time': flight_detail.departure_time,
            'arrival_airport': flight_detail.arrival_airport,
            'arrival_time': flight_detail.arrival_time,
            'arrival_terminal': flight_detail.arrival_terminal,
            'flight_duration': flight_detail.flight_duration,
            'airline': flight_detail.airline
    }
    return make_response(response, 200)


@app.route('/cities/get/', methods=['GET'])
def get_cities():
    cities = db.session.query(City)
    
    response = []
    for city in cities:
        response.append({
            'id': city.id, 
            'name': city.name,
            'population': city.population,
            'location': city.location,
            'pictures': city.pictures,
        })
    return make_response({'cities':response}, 200)


@app.route('/cities/get/<string:c_id>/', methods=['GET'])
def get_one_city(c_id):
    city = db.session.query(City).filter_by(id = c_id).first_or_404()
    
    response = {
            'id': city.id, 
            'name': city.name,
            'population': city.population,
            'location': city.location,
            'pictures': city.pictures,
    }

    return make_response({'hotels':response}, 200)


@app.route('/about/')
def about():
    member_stats, group_stats = for_about_page()

    return render_template('about.html', group_stats=group_stats, member_stats=member_stats, data_source=data_source,
                           tools=tools, postman_api=postman_api)


@app.route('/unittest/')
def unittest():
    return render_template('unittest.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
