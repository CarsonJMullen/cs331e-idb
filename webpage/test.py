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
        s = City(name='NewCity')
        db.session.add(s)
        db.session.commit()

        r = db.session.query(City).filter_by(name='NewCity').one()
        self.assertEqual(str(r.name), 'NewCity')

        db.session.query(City).filter_by(name='NewCity').delete()
        db.session.commit()


if __name__ == '__main__':
    unittest.main()
