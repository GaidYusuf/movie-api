from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(120), nullable=False)
    director = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.String(120), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    imdb_rating = db.Column(db.Float, nullable=False)

    def __rep__(self):
        return f"<Movie(title='{self.title}', year={self.release_year}, genre='{self.genre}', director='{self.director}', rating='{self.rating}', duration='{self.duration}', imdb_rating={self.imdb_rating})>"


@app.route('/')
def index():
    return """
    <h1>Welcome to the Movie API</h1>
    <p>This is a RESTful API for managing and retrieving information about movies.</p>
    <p>Use the following endpoints to interact with the API:</p>
    <ul>
        <li>GET /movies - Retrieve a list of all movies</li>
        <li>POST /movies - Add a new movie</li>
        <li>GET /movies/&lt;id&gt; - Retrieve details of a specific movie by ID</li>
        <li>PUT /movies/&lt;id&gt; - Update a specific movie by ID</li>
        <li>DELETE /movies/&lt;id&gt; - Delete a specific movie by ID</li>
    </ul>
    """


@app.route('/movies')
def get_movies():
    movies = Movie.query.all()

    # serialize (converting object state into a format that can be transmitted or stored i.e JSON) SQLAlchemy objects to JSON
    movies_list = []
    for movie in movies:
        movie_data = {
            'id': movie.id,
            'title': movie.title,
            'release_year': movie.release_year,
            'genre': movie.genre,
            'director': movie.director,
            'rating': movie.rating,
            'duration': movie.duration,
            'imdb_rating': movie.imdb_rating
        }
        movies_list.append(movie_data)

    return {"movies": movies_list}


@app.route('/movies', methods=['POST'])
def add_movies():

    # request.get_json retrieves JSON data from the client to my server
    data = request.get_json()

    title = data['title']
    release_year = data['release_year']
    genre = data['genre']
    director = data['director']
    rating = data["rating"]
    duration = data["duration"]
    imdb_rating = data["imdb_rating"]

    # check if a movie with the same title already exists
    movies = Movie.query.all()
    movie_exist = False
    for movie in movies:
        if movie.title == title:
            movie_exist = True
            return {"error": 'Movie with this title already exists'}

    if movie_exist is False:

        # create a new Movie object using data from the JSON request
        new_movie = Movie(title=title, release_year=release_year, genre=genre,
                          director=director, rating=rating, duration=duration, imdb_rating=imdb_rating)

        # add the new movie to database
        db.session.add(new_movie)
        db.session.commit()

        return {'message': 'Movie added successfully'}


@app.route('/movies/<id>', methods=['DELETE'])
def delete_movie(id):

    # query movie by id
    movie = Movie.query.get(id)

    # fetch all remaining movies and update their id's
    movies = Movie.query.order_by(Movie.id).all()
    for index, movie in enumerate(movies):
        movie.id = index + 1

    # delete movie from database
    db.session.delete(movie)
    db.session.commit()

    return {'message': 'Movie deleted successfully'}
