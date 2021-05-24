"""
    File name: app.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 18/5/2021
    Date last modified: 24/5/2021
    Python Version: 3.8
"""

from flask import Flask
from flask_restful import Api
from code.db import db
from code.resources.movie import Movie, MovieList
from code.resources.alias import MovieAlias
from api_keys import DB_CONNECTION
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNECTION
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db.init_app(app)
migrate = Migrate(app, db)


api.add_resource(MovieList, '/api/movie')
api.add_resource(Movie, '/api/movie/<string:movie_id>')
api.add_resource(MovieAlias, '/api/movie/alias/<string:alias>')


if __name__ == "__main__":
    app.run(port=5000, debug=True)
