import os
from flask_cors import CORS
from flask import Flask, request, abort, jsonify, session, Response, redirect
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth, setup_auth0
app = Flask(__name__)
setup_db(app)
CORS(app)
# ==========================================================================
# LOGIN FOR AUTH0
# ==========================================================================

AUTHORIZE = "authorize?audience"


@app.route('/')
@app.route('/login')
def login():
    return redirect(
      "https://{}/{}={}&response_type=token&client_id={}&redirect_uri={}"
      .format(AUTH0_DOMAIN, AUTHORIZE, API_AUDIENCE, CLIENT_ID,
              AUTH0_CALLBACK_URL))


@app.route('/login-results')
def login_result():
    return jsonify({"success": True})

# ==========================================================================
# END OF LOGIN
# ==========================================================================


# ==========================================================================
# ENDPOINTS
# ==========================================================================


# ==========================================================================
# MOVIE ENDPOINTS
# ==========================================================================


@app.route('/movies', methods=["GET"])
@requires_auth('get:movies')
def get_movies():
    all_movies = Movie.query.all()
    movies = [item.format() for item in all_movies]
    return jsonify({"success": True,
                    "movies": movies})


@app.route('/movies', methods=["POST"])
@requires_auth('post:movies')
def post_movies(jwt):
    try:
        # posts movie by creating the two feilds
        # one feild being the title other being the release date
        data = request.get_json()
        movie_title = data.get('title', None)
        movie_release_date = data.get('release_date', None)

        post_movie = Movie(title=movie_title, release_date=movie_release_date)
        post_movie.insert()

        return jsonify({'success': True,
                        'movie': post_movie.format()})
    except Movie.doesnotexist:
        abort(500)


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movies(movie_id):
    movie = Movie.query.get(movie_id)
    deleted_movie = movie.format()
    success = movie.delete()
    if(success):
        return jsonify({
            'success': True,
            "deleted_movie": deleted_movie})
    else:
        abort(500)


@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(movie_id):
    movie = Movie.query.get(movie_id)
    data = request.get_json()
    if('title' in data):
        movie.title = data['title']
    if('release_date' in data):
        try:
            movie.release_date = release_date
        except Movie.notupdated:
            abort(400)
    success = movie.update()
    updated_movie = Movie.query.get(movie_id)
    if(success):
        return jsonify({'success': True,
                        'updated movie': updated_movie.format()})
    else:
        abort(500)


# ==========================================================================
# ACTOR ENDPOINTS
# ==========================================================================


@app.route('/actors', methods=["GET"])
@requires_auth('get:movies')
def get_actors():
    all_actors = Actor.query.all()
    actors = [item.format() for item in all_actors]
    return jsonify({"success": True,
                    "actors": actors})


@app.route('/actors', methods=["POST"])
@requires_auth('post:actors')
def post_actors(jwt):
    try:
        # posts actor by creating the two feilds
        # one feild
        data = request.get_json()
        actor_name = data.get('name', None)
        actor_age = data.get('age', None)
        actor_gender = data.get('gender', None)
        post_actor = Actor(name=actor_name, age=actor_age, gender=actor_gender)
        post_actor.insert()
        return jsonify({'success': True,
                        'posted_actor': post_actor.format()})
    except Actor.notcreated:
        abort(500)


@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actors(actor_id):
    actor = Actor.query.get(actor_id)
    deleted_actor = actor.format()
    success = actor.delete()
    if(success):
        return jsonify({
            'success': True,
            "deleted_actor": deleted_actor})
    else:
        abort(500)


@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(actor_id):
    actor = Actor.query.get(actor_id)
    data = request.get_json()
    if('name' in data):
        actor.title = data['title']
    if('age' in data):
        actor.age = data['age']
    if('gender' in data):
        actor.gender = data['gender']
    success = actor.update()
    updated_actor = Actor.query.get(actor_id)
    if(success):
        return jsonify({'success': True,
                        'updated actor': updated_actor.format()})
    else:
        abort(500)


# ==========================================================================
# ERROR HANDLERS
# ==========================================================================


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
      }), 422


@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
      }), 404


@app.errorhandler(500)
def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "error with server"
      }), 500


@app.errorhandler(AuthError)
def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 401,
      "message": "unAuthorized"
      }), 401


if __name__ == '__main__':
    app.run()
