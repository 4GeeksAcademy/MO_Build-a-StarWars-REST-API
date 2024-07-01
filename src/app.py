"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for # type: ignore
from flask_migrate import Migrate # type: ignore
from flask_swagger import swagger # type: ignore
from flask_cors import CORS # type: ignore
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People , Planets , FavoritePeople, FavoritePlanets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/users', methods=['GET'])
def handle_user():
    
        user = User.query.all()
        user = list(map(lambda item: item.serialize(), user))

        return jsonify({
            "data": user
        }), 200


@app.route('/users/<int:id>', methods=['GET'])
def handle_user_id(id):
    
        user = User.query.get(id)
        

        return jsonify({
            "data": user.serialize()
        }), 200


@app.route('/people', methods=['GET'])
def handle_people():
    if request.method == 'GET':
        people = People.query.all()
        people = list(map(lambda item: item.serialize(), people))

        return jsonify({
            "data": people
        }), 200
    
@app.route('/people/<int:id>', methods=['GET'])
def handle_people_id(id):
    if request.method == 'GET':
        people = People.query.get(id)
        

        return jsonify({
            "data": people.serialize()
        }), 200    
   

@app.route('/planets', methods=['GET'])
def handle_planets():
    
        planets = Planets.query.all()
        planets = list(map(lambda item: item.serialize(), planets))

        return jsonify({
            "data": planets
        }), 200
    
@app.route('/planets/<int:id>', methods=['GET'])
def handle_planets_id(id):
        
        planets = Planets.query.get(id)
        
        return jsonify({
            "data": planets.serialize()
        }), 200   


@app.route("/planets/favorite/<int:planet_id>", methods=["POST"])
def post_fav_planet(planet_id):
    one = Planets.query.get(planet_id)
    user = User.query.get(1)
    if(one):
        new_fav = FavoritePlanets()
        new_fav.email = user.email
        new_fav.planet_id = planet_id
        db.session.add (new_fav)
        db.session.commit()
        return jsonify({
        "message": "Favorite planet added"
    })
    else:
        raise APIException("The planet not exist", status_code=404)


@app.route('/people/favorite/<int:people_id>', methods=["POST"])
def post_fav_people(people_id):
    one = People.query.get(people_id)
    user = User.query.get(1)
    if(one):
        new_fav = FavoritePeople()
        new_fav.email = user.email
        new_fav.people_id = people_id
        db.session.add (new_fav)
        db.session.commit()
        return jsonify({
        "message": "Favorite people added"
    })
    else:
        raise APIException("People not exist", status_code=404)

@app.route("/planets/favorite/<int:planet_id>", methods=["DELETE"])
def delete_fav_planet(planet_id):
    one = FavoritePlanets.query.filter_by(planet_id=planet_id).first()
    if(one):
        db.session.delete(one)
        db.session.commit()
        return jsonify({
        "message": "The planet with id" + str(planet_id) + "was dleted"
    })
    else:
        raise APIException("The planet does not exist", status_code=404)


@app.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_fav_people(people_id):
    one = FavoritePeople.query.filter_by(people_id=people_id).first()
    if(one):
        db.session.delete(one)
        db.session.commit()
        return jsonify({
        "mensaje": "People with id" + str(people_id) + "was deleted"
    })
    else:
        raise APIException("People do not exist", status_code=404)

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
