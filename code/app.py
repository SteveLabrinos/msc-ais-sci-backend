"""
    File name: app.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 18/5/2021
    Date last modified: 25/5/2021
    Python Version: 3.8
"""

from flask import Flask
from flask_restful import Api
from code.db import db
from code.resources.movie import Movie, MovieList
from code.resources.alias import MovieAlias
from code.resources.video import Video
from code.resources.actor import ActorDataset
from flask_migrate import Migrate

# Downloading a sample of the list to reduce time results
MAX_VIDEO_SEARCH = 2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///csi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db.init_app(app)
migrate = Migrate(app, db)


# create db tables if they don't exist before the first call
@app.before_first_request
def create_table():
    db.create_all()


api.add_resource(MovieList, '/api/movie')
api.add_resource(Movie, '/api/movie/<string:movie_id>')
api.add_resource(MovieAlias, '/api/movie/alias/<string:alias>')
api.add_resource(Video, '/api/video/<string:movie_id>')
api.add_resource(ActorDataset, '/api/dataset/<string:movie_id>/size/<int:size>')


if __name__ == "__main__":
    db.create_all()
    app.run(port=5000, debug=True)
