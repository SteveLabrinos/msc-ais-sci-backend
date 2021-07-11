"""
    File name: execution_in_sequence.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 24/5/2021
    Date last modified: 24/5/2021
    Python Version: 3.8
"""

from code.db import db


# define the M:N relation for movie and actor
class MovieActorsModel(db.Model):
    __tablename__ = 'movie_actor'
    # __table_args__ = {'schema': 'face_recognition'}

    movie_id = db.Column(db.String(20), db.ForeignKey('movie.id'), primary_key=True)
    actor_id = db.Column(db.String(20), db.ForeignKey('actor.id'), primary_key=True)
    role_name = db.Column(db.String(50))

    def __init__(self, movie_id, actor_id, role_name):
        self.movie_id = movie_id
        self.actor_id = actor_id
        self.role_name = role_name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()



