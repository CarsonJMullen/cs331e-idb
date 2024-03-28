#!/usr/bin/env python3

# -------
# imports
# -------

import os
import sys
import unittest
from models import db, City, Flight, FlightDetails, Hotel, Activity

#TODO: create at least three unit tests for each model using Python unittest.
#TODO: update how many unittests you made in static/constants.py

# -----------
# DBTestCases
# -----------
class DBTestCases(unittest.TestCase):
    # ---------
    # insertion, deletion, and update 
    # ---------

    # city tests 


    def test_city_insert(self):
        s = City(name='Beijing', iataCode='BZJ')
        db.session.add(s)
        db.session.commit()

        r = db.session.query(City).filter_by(name='Beijing').one()
        self.assertEqual(str(r.name), 'Beijing')

        db.session.query(City).filter_by(name='Beijing').delete()
        db.session.commit()


    def test_city_delete(self):
        s = City(name='Beijing', iataCode='BZJ')
        db.session.add(s)
        db.session.commit()

        result1 = db.session.execute(db.select(db.func.count()).select_from(City)).scalar()

        db.session.query(City).filter_by(name='Beijing').delete()
        db.session.commit()
    
        result2 = db.session.execute(db.select(db.func.count()).select_from(City)).scalar()
        self.assertEqual(result2, result1-1)
        

    def test_city_update(self):
        s = City(name = 'Beijing', iataCode='BZJ')
        db.session.add(s)
        db.session.commit()

        db.session.query(City).filter_by(iataCode='BZJ').update({City.population: 21500000})
        db.session.commit()
        
        r = db.session.query(City).filter_by(iataCode='BZJ').one()
        self.assertEqual(r.population, 21500000)

        db.session.query(City).filter_by(iataCode='BZJ').delete()
        db.session.commit()


    # flight tests 
        

    def test_flight_insert(self):
        s = Flight(id=-1 ,arrival_airport = 'SZX',departure_airport = 'PEK', airline='BOEING MURDER', arrival_city = 'MAD')
        db.session.add(s)
        db.session.commit()

        r = db.session.query(Flight).filter_by(airline='BOEING MURDER').one()
        self.assertEqual(str(r.airline), 'BOEING MURDER')

        db.session.query(Flight).filter_by(airline='BOEING MURDER').delete()
        db.session.commit()

    def test_flight_delete(self):
        s = Flight(id = -1, arrival_airport = 'SZX',departure_airport = 'PEK', airline='BOEING MURDER', arrival_city = 'MAD')
        db.session.add(s)
        db.session.commit()

        result1 = db.session.execute(db.select(db.func.count()).select_from(Flight)).scalar()

        db.session.query(Flight).filter_by(airline='BOEING MURDER').delete()
        db.session.commit()
    
        result2 = db.session.execute(db.select(db.func.count()).select_from(Flight)).scalar()
        self.assertEqual(result2, result1-1)


    def test_flight_update(self):
        s = Flight(id = -1, arrival_airport = 'SZX',departure_airport = "PEK", airline='BOEING MURDER', arrival_city = 'MAD')
        db.session.add(s)
        db.session.commit()

        db.session.query(Flight).filter_by(airline='BOEING MURDER').update({Flight.price: '100000'})
        db.session.commit()
        
        r = db.session.query(Flight).filter_by(airline='BOEING MURDER').one()
        self.assertEqual(str(r.price), '100000')

        db.session.query(Flight).filter_by(airline='BOEING MURDER').delete()
        db.session.commit()


    # FlightDetails 
        
    
    def test_flightDetail_insert(self):
        s = FlightDetails(id=-1 , flight_group = 0, departure_airport = 'MAD')
        db.session.add(s)
        db.session.commit()

        r = db.session.query(FlightDetails).filter_by(id=-1).one()
        self.assertEqual(r.id, -1)

        db.session.query(FlightDetails).filter_by(id=-1).delete()
        db.session.commit()

    def test_flightDetail_delete(self):
        s = FlightDetails(id=-1 , flight_group = 0, departure_airport = 'MAD')
        db.session.add(s)
        db.session.commit()

        result1 = db.session.execute(db.select(db.func.count()).select_from(FlightDetails)).scalar()

        db.session.query(FlightDetails).filter_by(id=-1).delete()
        db.session.commit()
    
        result2 = db.session.execute(db.select(db.func.count()).select_from(FlightDetails)).scalar()
        self.assertEqual(result2, result1-1)


    def test_flightDetail_update(self):
        s = FlightDetails(id=-1 , flight_group = 0, departure_airport = 'MAD')
        db.session.add(s)
        db.session.commit()

        db.session.query(FlightDetails).filter_by(id=-1).update({FlightDetails.airline: 'BOEING MURDER'})
        db.session.commit()
        
        r = db.session.query(FlightDetails).filter_by(id=-1).one()
        self.assertEqual(str(r.airline), 'BOEING MURDER')

        db.session.query(FlightDetails).filter_by(id=-1).delete()
        db.session.commit()
     

    # Activity 
        

    def test_Activity_insert(self):
        s = Activity(id='0000000001' , name='bycicyle ryding', iataCode='MAD')
        db.session.add(s)
        db.session.commit()

        r = db.session.query(Activity).filter_by(name='bycicyle ryding').one()
        self.assertEqual(str(r.name), 'bycicyle ryding')

        db.session.query(Activity).filter_by(name='bycicyle ryding').delete()
        db.session.commit()


    def test_Activity_delete(self):
        s = Activity(id='0000000001' , name='bycicyle ryding', iataCode='MAD')
        db.session.add(s)
        db.session.commit()

        result1 = db.session.execute(db.select(db.func.count()).select_from(Activity)).scalar()

        db.session.query(Activity).filter_by(name='bycicyle ryding').delete()
        db.session.commit()
    
        result2 = db.session.execute(db.select(db.func.count()).select_from(Activity)).scalar()
        self.assertEqual(result2, result1-1)


    def test_Activity_update(self):
        s = Activity(id='0000000001' , name='bycicyle ryding', iataCode='MAD')
        db.session.add(s)
        db.session.commit()

        db.session.query(Activity).filter_by(name='bycicyle ryding').update({Activity.rating: 4.2})
        db.session.commit()
        
        r = db.session.query(Activity).filter_by(name='bycicyle ryding').one()
        self.assertEqual(str(r.rating), '4.2')

        db.session.query(Activity).filter_by(name='bycicyle ryding').delete()
        db.session.commit()
    

    # Hotels 


    def test_Hotel_insert(self): 
        s = Hotel(id='00000001' , name='north jester', iataCode='MAD')
        db.session.add(s)
        db.session.commit()

        r = db.session.query(Hotel).filter_by(name='north jester').one()
        self.assertEqual(str(r.name), 'north jester')

        db.session.query(Hotel).filter_by(name='north jester').delete()
        db.session.commit()

    
    def test_Hotel_delete(self):
        s = Hotel(id='00000001' , name='north jester', iataCode='MAD')
        db.session.add(s)
        db.session.commit()

        result1 = db.session.execute(db.select(db.func.count()).select_from(Hotel)).scalar()

        db.session.query(Hotel).filter_by(name='north jester').delete()
        db.session.commit()
    
        result2 = db.session.execute(db.select(db.func.count()).select_from(Hotel)).scalar()
        self.assertEqual(result2, result1-1)

    
    def test_Hotel_update(self):
        s = Hotel(id='00000001' , name='north jester', iataCode='MAD')
        db.session.add(s)
        db.session.commit()

        db.session.query(Hotel).filter_by(name='north jester').update({Hotel.rating: 5})
        db.session.commit()
        
        r = db.session.query(Hotel).filter_by(name='north jester').one()
        self.assertEqual(str(r.rating), '5')

        db.session.query(Hotel).filter_by(name='north jester').delete()
        db.session.commit()

def run():
    unittest.main()
        
if __name__ == '__main__':
    run()
