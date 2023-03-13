"""
Resource: Brevets
"""
from flask import Response, request
from flask_restful import Resource
from datetime import datetime

# You need to implement this in database/models.py
from database.models import Brevet

class Brevets(Resource):
    def get(self):
        json_object = Brevet.objects().to_json()
        return Response(json_object, mimetype="application/json", status=200)
    
    def post(self):
        input_json = request.json

        length = input_json["length"]
        start_time = input_json["start_time"]
        checkpoints = input_json["checkpoints"]
        Brevet.objects().delete() #clear db before inserting
        result = Brevet(length=length, start_time=start_time, checkpoints=checkpoints).save()
        return {'_id': str(result.id)}, 200
    