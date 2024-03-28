#!/usr/bin/env python3

# -------
# imports
# -------

import os
import sys
import unittest
from models import db, City

#TODO: create at least three unit tests for each model using Python unittest.
#TODO: update how many unittests you made in static/constants.py

# -----------
# DBTestCases
# -----------
class DBTestCases(unittest.TestCase):
    # ---------
    # insertion
    # ---------

    def test_city_insert_1(self):
        s = City(name='Beijing')
        db.session.add(s)
        db.session.commit()

        r = db.session.query(City).filter_by(name='Beijing').one()
        self.assertEqual(str(r.name), 'Beijing')

        db.session.query(City).filter_by(name='Beijing').delete()
        db.session.commit()

    def test_city_insert_2(self):
        s = City(iataCode='BZJ')
        db.session.add(s)
        db.session.commit()

        r = db.session.query(City).filter_by(iataCode='BZJ').one()
        self.assertEqual(str(r.iataCode), 'BZJ')

        db.session.query(City).filter_by(iataCode='BZJ').delete()
        db.session.commit()

    def test_city_insert_3(self):
        s = City(location='China')
        db.session.add(s)
        db.session.commit()

        r = db.session.query(City).filter_by(location='China').one()
        self.assertEqual(str(r.location), 'China')

        db.session.query(City).filter_by(location='China').delete()
        db.session.commit()

 

if __name__ == '__main__':
    unittest.main()
