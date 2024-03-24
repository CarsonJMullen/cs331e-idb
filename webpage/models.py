from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os


# Google Cloud SQL (change this accordingly) 
USER ="postgres"
PASSWORD ="toptravel"
PUBLIC_IP_ADDRESS ="localhost:5432"
DBNAME ="bookdb"


# Configuration
# One-To-Many relation: Assume that a Publisher can have many Books 
# but a Book can only have one Publisher.
app = Flask(__name__)

app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_STRING", f'postgresql://{USER}:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # to suppress a warning message
db = SQLAlchemy(app)


class City(db.Model):
    __tablename__ = 'city'

    name = db.Column(db.String(20), nullable = False)
    iataCode = db.Column(db.String(3), primary_key = True)
    population = db.Column(db.String(12))
    location = db.Column(db.String(20))
    pictures = db.Column(db.Array(db.String(200)))

    activities = db.relationship('Activity', backref = 'city')
    flights = db.relationship('Flight', backref = 'city')
    hotels = db.relationship('Hotel', backref = 'city')

class Activity(db.Model):
    __tablename__ = 'activity'

    id = db.Column(db.String(10), primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    description = db.Column(db.String(250))
    rating = db.Column(db.String(3))
    price_amount = db.Column(db.String(8))
    price_currencyCode = db.Column(db.String(3))
    pictures = db.Column(db.Array(db.String(200)))
    bookingLink = db.Column(db.String(200))
    iataCode = db.Column(db.String(3), db.ForeignKey('city.iataCode'))


# TBD
class Flight(db.Model):
    __tablename__ = 'flight'

    id = db.Column(db.String(80), nullable=False)
    iataCode = db.Column(db.String(3), db.ForeignKey('city.iataCode'))


class Hotel(db.Model):
    __tablename__ = 'hotel'

    id = db.Column(db.String(8), primary_key = True)
    name = db.Column(db.String(80), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    amenities = db.Column(db.Array(db.String(20)))
    rating = db.Column(db.Integer)
    iataCode = db.Column(db.String(3), db.ForeignKey('city.iataCode'))


db.drop_all()
db.create_all()