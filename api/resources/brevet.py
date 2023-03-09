"""
Resource: Brevet
"""
from flask import Response, request
from flask_restful import Resource

# You need to implement this in database/models.py
from database.models import Brevet

class Brevet(Resource):
    def get(self, _id):
        json_object = Brevet.objects(id=_id).to_json()
        return Response(json_object, mimetype="application/json", status=200)

    def delete(self, _id):
        result = Brevet.objects(id=_id).delete()
        return {'_id': str(result.id)}, 200

    def put(self, _id):
        input_json = request.json

        distance = input_json["distance"]
        location = input_json["locaiton"]
        open = input_json["open"]
        close = input_json["close"]
        checkpoints = input_json["checkpoints"]

        result = Brevet.objects(id=_id).update(
            set__distance=distance,
            set__location=location, 
            set__open=open, 
            set__close=close, 
            set__checkpoints=checkpoints
            )
        
        return {'_id': str(result.id)}, 200