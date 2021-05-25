"""
    File name: app.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 24/5/2021
    Date last modified: 24/5/2021
    Python Version: 3.8
"""

from flask_restful import Resource
from code.models.actor import ActorModel


class Actor(Resource):
    def get(self, actor_id):
        actor = ActorModel.find_by_id(actor_id)
        if actor:
            return actor.json()
        return {'message': f'Actor with id {actor_id} not found'}, 404


