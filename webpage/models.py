from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

# Google Cloud SQL (change this accordingly)
USER = "postgres"
PASSWORD = "toptravel"
# PUBLIC_IP_ADDRESS ="34.68.182.175"
PUBLIC_IP_ADDRESS = "localhost"
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

class City(db.Model):
    __tablename__ = 'city'

    name = db.Column(db.String(30), nullable=False)
    iataCode = db.Column(db.String(3), primary_key=True)
    population = db.Column(db.Integer)
    location = db.Column(db.String(30))
    pictures = db.Column(db.ARRAY(db.Text))

    activities = db.relationship('Activity', backref='city')
    flights = db.relationship('Flight', backref='city')
    hotels = db.relationship('Hotel', backref='city')


class Activity(db.Model):
    __tablename__ = 'activity'

    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    rating = db.Column(db.Numeric(2, 1))
    price_amount = db.Column(db.String(8))
    price_currencyCode = db.Column(db.String(3))
    pictures = db.Column(db.ARRAY(db.Text))
    bookingLink = db.Column(db.Text)
    iataCode = db.Column(db.String(3), db.ForeignKey('city.iataCode'))


# TBD
class Flight(db.Model):
    __tablename__ = 'flight'

    id = db.Column(db.String(80), primary_key=True)
    departure_airport = db.Column(db.String(3), nullable=False)
    arrival_airport = db.Column(db.String(3), nullable=False)
    iataCode = db.Column(db.String(3), db.ForeignKey('city.iataCode'))
    price = db.Column(db.String(8))
    seats_left = db.Column(db.Integer)
    duration = db.Column(db.DateTime)
    num_legs = db.Column(db.Integer)
    departure_time = db.Column(db.DateTime)
    arrival_time = db.Column(db.DateTime)
    airline = db.Column(db.String(30))

class FlightDetails(db.Model):
    __tablename__ = 'flight_details'

    id = db.Column(db.String(80), primary_key=True)
    flight_group = db.Column(db.String(80), db.ForeignKey('flight.id'))
    flight_number = db.Column(db.Integer)
    departure_airport = db.Column(db.String(3), nullable=False)
    departure_time = db.Column(db.DateTime)
    arrival_airport = db.Column(db.String(3))
    arrival_time = db.Column(db.DateTime)
    arrival_terminal = db.Column() #FIX THIS ONE
    flight_duration = db.Column(db.DateTime)
    airline = db.Column(db.String(30))
    
class Hotel(db.Model):
    __tablename__ = 'hotel'

    id = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    latitude = db.Column(db.Numeric(8, 5))
    longitude = db.Column(db.Numeric(8, 5))
    amenities = db.Column(db.ARRAY(db.String(20)))
    rating = db.Column(db.SmallInteger)
    iataCode = db.Column(db.String(3), db.ForeignKey('city.iataCode'))


db.drop_all()
db.create_all()
