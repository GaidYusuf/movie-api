# Movie API with Flask

A RESTful API built with Flask for managing and retrieving information about movies. Includes user authentication using JWT.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Endpoints](#endpoints)
- [Usage](#usage)
- [Testing with Postman](#testing-with-postman)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration and login
- JWT-based authentication for secure access
- CRUD operations for managing movies (Create, Read, Update, Delete)
- RESTful API endpoints for interacting with movie data

## Technologies Used

- Flask
- SQLAlchemy
- Flask-JWT-Extended
- SQLite (for local database)

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your_username/movie-api-flask.git
   cd movie-api-flask

   ```
   
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
 
   ```

3. **Set up the database:**
    ```bash
    python
    >>> from app import db
    >>> db.create_all()
    >>> exit()

4. **Run the application**
    ```bash
    flask run

5. **Access the API:**
    Open your web browser or a tool like Postman and go to http://localhost:5000/ to interact with the API.

## Endpoints

GET /movies: Retrieve a list of all movies

POST /movies: Add a new movie

GET /movies/<id>: Retrieve details of a specific movie by ID

PUT /movies/<id>: Update a specific movie by ID

DELETE /movies/<id>: Delete a specific movie by ID

POST /register: Register a new user

POST /login: Authenticate and obtain JWT access token

GET /get_user: Retrieve user details


## Usage

### Register a New User

```http
POST /register
Content-Type: application/json

{
  "username": "new_user",
  "password": "password123"
}

### Login and Obtain JWT Token

```http
POST /login
Content-Type: application/json

{
  "username": "new_user",
  "password": "password123"
}

### Add a New Movie

```http
POST /movies
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
  "title": "New Movie",
  "release_year": 2024,
  "genre": "Action",
  "director": "Director Name",
  "rating": "PG-13",
  "duration": 120,
  "imdb_rating": 7.5
}


