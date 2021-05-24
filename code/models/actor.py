"""
    File name: app.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 24/5/2021
    Date last modified: 24/5/2021
    Python Version: 3.8
"""

from code.db import db


class ActorModel(db.Model):
    __tablename__ = 'actor'
    # __table_args__ = {'schema': 'face_recognition'}

    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50))
    image = db.Column(db.String(255))

    def __init__(self, id, name, image):
        self.id = id
        self.name = name
        self.image = image

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'imageUrl': self.image,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
