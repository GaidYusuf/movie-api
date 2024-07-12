from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import datetime, timedelta

# instantiate flask app
app = Flask(__name__)

# configure application to make use of preferred DBMS
# SQlite will be used as the preferred DBMS as it doesn't require a separate server
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# configure the application for JWT Authentication
app.config['SECRET_KEY'] = 'your_strong_secret_key'
app.config["JWT_SECRET_KEY"] = 'your_jwt_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(
    hours=2)  # Example: Set token expiration time

# initialize the database in my application
# instantiate db object and this will act as a bridge between the application and the database
db = SQLAlchemy(app)

# JWT initialization
jwt = JWTManager(app)


class Movie(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(120), nullable=False)
    director = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.String(120), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    imdb_rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Movie(id='{self.id}', title='{self.title}', year={self.release_year}, genre='{self.genre}', director='{self.director}', rating='{self.rating}', duration='{self.duration}', imdb_rating={self.imdb_rating})>"


# create User Model to store user's details
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


@app.route('/register', methods=['GET', 'POST'])
def register():

    # request.get_json retrieves JSON data from the client to my server
    data = request.get_json()

    username = data['username']
    password = data['password']

    user_exists = bool(User.query.filter_by(username=username).first())
    if user_exists is True:
        return jsonify({'error': 'User already exists'}), 400

    # create a new User object using data from the JSON request
    new_user = User(username=username, password=password)

    # add the new user to database
    db.session.add(new_user)
    db.session.commit()


@app.route('/login', methods=['POST'])
def login():

    # request.get_json retrieves JSON data from the client to my server
    data = request.get_json()

    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200

    return jsonify({'error': 'Invalid username or password'}), 401


# @jwt_required decorator is used to protect specific routes that require authentication
# This decorator will confirm that there's a JWT access token in the request headers before allowing access to the page
@app.route('/get_user', methods=['GET'])
@jwt_required()
def get_user():
    # fetch the user ID from the JWT token
    user_id = get_jwt_identity()

    # query the user by id from the User table
    user = User.query.get_or_404(user_id)

    user_data = {
        'id': user.id,
        'username': user.username,
        'password': user.password,
    }

    # check if user exists
    if user:
        return jsonify(user_data), 200
    else:
        return jsonify({'message': 'User not found'}), 404


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

    # query that retrieves all records from the Movie table in the database.
    movies = Movie.query.all()

    # serialize SQLAlchemy objects to JSON
    # serialize means converting object state into a format that can be transmitted or stored i.e JSON
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

    return jsonify(movies_list), 200


@app.route('/movies/<id>', methods=['GET'])
def get_one_movie(id):

    # query movie by id
    movie = Movie.query.get_or_404(id)

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

    return jsonify(movie_data), 200


@app.route('/movies', methods=['POST'])
@jwt_required()
def add_movie():

    # request.get_json retrieves JSON data from the client to my server
    data = request.get_json()

    # Check if all required fields are present in the request data
    required_fields = ['title', 'release_year', 'genre',
                       'director', 'rating', 'duration', 'imdb_rating']
    for field in required_fields:
        if field not in data:
            # If any required field is missing, return an error response with a 400 status code
            return {'error': f'Missing required field: {field}'}, 400

    title = data['title']
    release_year = data['release_year']
    genre = data['genre']
    director = data['director']
    rating = data['rating']
    duration = data['duration']
    imdb_rating = data['imdb_rating']

    # check if a movie with the same title already exists
    movie_exists = bool(Movie.query.filter_by(title=title).first())
    if movie_exists is True:
        return {"error": 'Movie with this title already exists'}, 400

    # create a new Movie object using data from the JSON request
    new_movie = Movie(title=title, release_year=release_year, genre=genre,
                      director=director, rating=rating, duration=duration, imdb_rating=imdb_rating)

    # add the new movie to database
    db.session.add(new_movie)
    db.session.commit()

    return {'message': 'Movie added successfully'}, 201


@app.route('/movies/<id>', methods=['PUT'])
@jwt_required()
def update_movie(id):

    # fetch specific movie to update by querying its ID
    movie = Movie.query.get_or_404(id)

    # retrieve JSON data from the client to my server
    data = request.get_json()

    title = data['title']
    release_year = data['release_year']
    genre = data['genre']
    director = data['director']
    rating = data["rating"]
    duration = data["duration"]
    imdb_rating = data["imdb_rating"]

    # update movie attributes in database
    movie.title = title
    movie.release_year = release_year
    movie.genre = genre
    movie.director = director
    movie.rating = rating
    movie.duration = duration
    movie.imdb_rating = imdb_rating

    # commit the changes to the database
    db.session.commit()

    return {'message': 'Movie updated successfully'}, 201


@app.route('/movies/<id>', methods=['DELETE'])
@jwt_required()
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

    return {'message': 'Movie deleted successfully'}, 201
