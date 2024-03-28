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
    # insertion
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
    # def test_flight_insert(self):
    #     s = Flight(id=-1 ,arrival_airport = 'SZX',departure_airport = "PEK", airline='BOEING MURDER', arrival_city = 'SZX')
    #     db.session.add(s)
    #     db.session.commit()

    #     r = db.session.query(Flight).filter_by(airline='BOEING MURDER').one()
    #     self.assertEqual(str(r.airline), 'BOEING MURDER')

    #     db.session.query(Flight).filter_by(airline='BOEING MURDER').delete()
    #     db.session.commit()

    # def test_flight_delete(self):
    #     s = Flight(id = -2, arrival_airport = 'SZX',departure_airport = "PEK", airline='BOEING MURDER', arrival_city = 'SZX')
    #     db.session.add(s)
    #     db.session.commit()

    #     r = db.session.query(Flight).filter_by(departure_airport = "PEK").one()
    #     self.assertEqual(str(r.departure_airport), 'PEK')

    #     db.session.query(Flight).filter_by(departure_airport = "PEK").delete()
    #     db.session.commit()

    # def test_flight_update(self):
    #     s = Flight(id = -3, arrival_airport = 'SZX',departure_airport = "PEK", price='100000000.0', airline='BOEING MURDER', arrival_city = 'SZX')
    #     db.session.add(s)
    #     db.session.commit()

    #     r = db.session.query(Flight).filter_by(price='100000000.0').one()
    #     self.assertEqual(str(r.price), '100000000.0')

    #     db.session.query(Flight).filter_by(price='100000000.0').delete()
    #     db.session.commit()


    # FlightDetails 
        
    # Activity 
        
    # Hotels 
        
if __name__ == '__main__':
    unittest.main()
