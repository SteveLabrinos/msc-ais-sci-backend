"""
    File name: app.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 25/5/2021
    Date last modified: 25/5/2021
    Python Version: 3.8
"""

from code.db import db


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
            'movieId': self.movie_id
        }

    @classmethod
    def find_by_id(cls, video_id):
        return cls.query.filter_by(id=video_id).first()

    @classmethod
    def find_by_movie(cls, movie_id):
        return cls.query.filter_by(movie_id=movie_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

