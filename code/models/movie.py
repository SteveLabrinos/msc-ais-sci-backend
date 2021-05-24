"""
    File name: app.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 24/5/2021
    Date last modified: 24/5/2021
    Python Version: 3.8
"""

from code.db import db
from code.models.actor import ActorModel

movie_actors = db.Table('movie_actors',
                        db.Column('movie_id', db.String(20), db.ForeignKey('movie.id'), primary_key=True),
                        db.Column('actor_id', db.String(20), db.ForeignKey('actor.id'), primary_key=True),
                        db.Column('role_name', db.String(50))
                        )


class MovieModel(db.Model):
    __tablename__ = 'movie'
    # __table_args__ = {'schema': 'face_recognition'}

    id = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50))
    image_url = db.Column(db.String(255))
    year = db.Column(db.Integer)

    # foreign key relationship with alias 1:M table
    alias = db.relationship('MovieAliasModel', lazy='dynamic')
    actors = db.relationship('ActorModel', secondary=movie_actors, lazy='dynamic')

    def __init__(self, id, title, type, image_url, year):
        self.id = id
        self.title = title
        self.type = type
        self.image_url = image_url
        self.year = year

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'imageUrl': self.image_url,
            'year': self.year,
            'actors': [a.json() for a in self.actors.all()]
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()




