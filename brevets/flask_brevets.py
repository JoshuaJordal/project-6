"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
from pymongo import MongoClient
import os
import requests

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()


###
# API CALLERS
##

API_ADDR = os.environ["API_ADDR"]
API_PORT = os.environ["API_PORT"]
API_URL = f"http://{API_ADDR}:{API_PORT}/api"

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############

@app.route("/_calc_times")
def _calc_times():
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    brevet = request.args.get('brevet', 200, int)
    time = request.args.get('time')
    open_time = acp_times.open_time(km, brevet, arrow.get(time)).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, brevet, arrow.get(time)).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)

@app.route("/_insert_times", methods=["POST"])
def _insert_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    try:
        app.logger.debug("Got a JSON request")
        input_json = request.json
        brevet = int(input_json['brevet'])
        time = input_json["time"]
        checkpoints = input_json["checkpoints"]
        valid = 1

        for checkpoint in checkpoints:
            km = int(checkpoint["distance"])
            if(km > (brevet * 1.2)):
                valid = 0
            open_time = acp_times.open_time(km, brevet, arrow.get(time)).format('YYYY-MM-DDTHH:mm')
            close_time = acp_times.close_time(km, brevet, arrow.get(time)).format('YYYY-MM-DDTHH:mm')
            checkpoint["open_time"] = open_time
            checkpoint["close_time"] = close_time
        
        if(not valid):
            return flask.jsonify({"valid": 0})
        _id = requests.post(f"{API_URL}/brevets", json={"length": brevet, "start_time": time, "checkpoints": checkpoints})
        app.logger.debug(flask.jsonify(result={}))
        return flask.jsonify(result={}, status=1)
    
    except:
        return flask.jsonify(result={},
                        message="Oh no! Server error!", 
                        status=0, 
                        mongo_id='None')

@app.route("/_get_times", methods=["POST"])
def _get_times():
    try:
        races = requests.get(f"{API_URL}/brevets").json()
        races = races[0]
        brevet = races["length"]
        time = races["start_time"]
        checkpoints = races["checkpoints"]
        app.logger.debug("races={}".format(races))
        def sortfunc(e):
            return e['distance']
        checkpoints.sort(key=sortfunc)
        return flask.jsonify(
                result={"brevet": brevet, "time": time, "checkpoints": checkpoints}, 
                status=1)
    except:
        return flask.jsonify(
                result={}, 
                status=0,
                message="Something went wrong, couldn't fetch any lists!")

@app.route("/_cleardb")
def _cleardb():
    #db.races.drop()
    return flask.jsonify({})
#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
