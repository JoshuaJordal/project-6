"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""

import nose    # Testing framework
import logging
#from src.acp_times import open_time
import arrow
import collections
collections.Callable = collections.abc.Callable
from acp_times import *
from pymongo import MongoClient
import os
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)
client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.mydb


def test_brevets_open_120():
    assert open_time(120, 200, arrow.get('2021-01-01 00:00:00', 'YYYY-MM-DD HH:mm:ss')) == arrow.get('2021-01-01 03:32:00', 'YYYY-MM-DD HH:mm:ss')

def test_brevets_closed_120():
    assert close_time(120, 200, arrow.get('2021-01-01 00:00:00', 'YYYY-MM-DD HH:mm:ss')) == arrow.get('2021-01-01 08:00:00', 'YYYY-MM-DD HH:mm:ss')

def test_brevets_open_400():
    assert open_time(400, 400, arrow.get('2021-01-01 00:00:00', 'YYYY-MM-DD HH:mm:ss')) == arrow.get('2021-01-01 12:08:00', 'YYYY-MM-DD HH:mm:ss')

def test_brevets_closed_400():
    assert close_time(400, 400, arrow.get('2021-01-01 00:00:00', 'YYYY-MM-DD HH:mm:ss')) == arrow.get('2021-01-02 02:40:00', 'YYYY-MM-DD HH:mm:ss')

def test_brevets_open_550():
    assert open_time(550, 600, arrow.get('2021-01-01 00:00:00', 'YYYY-MM-DD HH:mm:ss')) == arrow.get('2021-01-01 17:08:00', 'YYYY-MM-DD HH:mm:ss')

def test_brevets_insert():
    db.races.insert_one({"open": '2021-01-01 00:00:00', "close": '2021-02-01 00:00:00', "km": '100', "miles": '60', "brevet": '100', "time": '2021-01-01 00:00:00'})
    assert(db.races.find({},{ "_id": 0 }) == {"open": '2021-01-01 00:00:00', "close": '2021-02-01 00:00:00', "km": '100', "miles": '60', "brevet": '100', "time": '2021-01-01 00:00:00'})

def test_brevets_retrieval():
    db.races.insert_one({"open": '2021-04-01 10:30:00', "close": '2021-05-01 10:30:00', "km": '350', "miles": '300', "brevet": '300', "time": '2021-03-01 12:30:00'})
    assert(db.races.find({},{ "_id": 0 }) == {"open": '2021-04-01 10:30:00', "close": '2021-05-01 10:30:00', "km": '350', "miles": '300', "brevet": '300', "time": '2021-03-01 12:30:00'})
