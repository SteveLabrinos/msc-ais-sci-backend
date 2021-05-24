"""
    File name: app.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 24/5/2021
    Date last modified: 24/5/2021
    Python Version: 3.8
"""

from code.db import db
from code.models.movie import MovieModel


class MovieAliasModel(db.Model):
    __tablename__ = 'movie_alias'
    __table_args__ = {'schema': 'face_recognition'}

    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(255), nullable=False)

    # relate to parent table movie
    movie_id = db.Column(db.String(20), db.ForeignKey(MovieModel.id))

    def __init__(self, alias, movie_id):
        self.alias = alias
        self.movie_id = movie_id

    def json(self):
        return {'alias': self.alias, 'movie_id': self.movie_id}

    @classmethod
    def find_by_alias(cls, alias):
        return cls.query.filter_by(alias=alias).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
