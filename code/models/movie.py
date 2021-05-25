"""
    File name: app.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 24/5/2021
    Date last modified: 25/5/2021
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

    # foreign key relationships
    alias = db.relationship('MovieAliasModel', lazy='dynamic')
    actors = db.relationship('ActorModel', secondary=movie_actors)
    videos = db.relationship('VideoModel', lazy='dynamic')

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
            'actors': [self.get_role_name(a).json() for a in self.actors]
        }

    def get_role_name(self, actor):
        actor.role_name = db.session.execute(
            "SELECT role_name FROM movie_actors WHERE movie_id=:movie_id AND actor_id=:actor_id",
            {'movie_id': self.id, 'actor_id': actor.id}
        ).first()[0]

        return actor

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        for a in self.actors:
            print(f'saving actor: {a.json()}')
            db.session.execute(
                "UPDATE movie_actors SET role_name = :role_name WHERE movie_id=:movie_id AND actor_id=:actor_id",
                {"role_name": a.role_name, "movie_id": self.id, "actor_id": a.id}
            )
            db.session.commit()

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
