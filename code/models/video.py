"""
    File name: execution_in_sequence.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 25/5/2021
    Date last modified: 25/5/2021
    Python Version: 3.8
"""

from code.db import db
from code.models.actor import ActorModel


video_actors = db.Table('video_actors',
                        db.Column('video_id', db.String(20), db.ForeignKey('video.id'), primary_key=True),
                        db.Column('actor_id', db.String(20), db.ForeignKey('actor.id'), primary_key=True),
                        db.Column('duration', db.Integer)
                        )


class VideoModel(db.Model):
    __tablename__ = 'video'

    id = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    view_count = db.Column(db.Integer)
    like_count = db.Column(db.Integer)
    dislike_count = db.Column(db.Integer)
    comment_count = db.Column(db.Integer)
    duration_sec = db.Column(db.Integer)

    movie_id = db.Column(db.String(20), db.ForeignKey('movie.id'))
    actors = db.relationship('ActorModel', secondary=video_actors)

    def __init__(self, id, title, view_count, like_count, dislike_count, comment_count, duration_sec):
        self.id = id
        self.title = title
        self.view_count = view_count
        self.like_count = like_count
        self.dislike_count = dislike_count
        self.comment_count = comment_count
        self.duration_sec = duration_sec

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'viewCount': self.view_count,
            'likeCount': self.like_count,
            'dislikeCount': self.dislike_count,
            'commentCount': self.comment_count,
            'durationSeconds': self.duration_sec,
            'movieId': self.movie_id,
            'actors': [self.get_duration(a).json() for a in self.actors]
        }

    def get_duration(self, actor):
        actor.duration = db.session.execute(
            "SELECT duration FROM video_actors WHERE video_id=:video_id AND actor_id=:actor_id",
            {'video_id': self.id, 'actor_id': actor.id}
        ).first()[0]

        return actor

    @classmethod
    def find_by_id(cls, video_id):
        return cls.query.filter_by(id=video_id).first()

    @classmethod
    def find_by_movie(cls, movie_id):
        return cls.query.filter_by(movie_id=movie_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

        for a in self.actors:
            db.session.execute(
                "UPDATE video_actors SET duration = :duration WHERE video_id = :video_id AND actor_id = :actor_id",
                {"duration": a.duration, "video_id": self.id, "actor_id": a.id}
                # "INSERT INTO video_actors VALUES (:video_id, :actor_id, :duration)",
                # {"video_id": self.id, "actor_id": a.id, "duration": a.duration}
            )
            db.session.commit()



