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

        result = Brevet.objects.get(id=_id).update(**input_json)
        
        return {'_id': str(result.id)}, 200