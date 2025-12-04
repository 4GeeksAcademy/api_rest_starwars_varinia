"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, People, FavoritePeople, FavoritePlanets
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

# endpoints usuario
@app.route('/user', methods=['GET'])
def handle_hello():
    try:
        user = User.query.all()
        if not query_results:
            return jsonify({"msg":"No users were found"}), 400

        return jsonify({
        "msg": "OK",
        "results": [u.serialize() for u in users]
    }), 200
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

#endpoits usuario especifico
@app.route('/user/<int:user_id>', methods=['GET'])
def user_by_id(user_id):
    try:
        user = User.query.filter_by(user_id)
        if not user:
            return jsonify({"msg":"No not found"}), 400

        return jsonify({
        "msg": "OK",
        "results": user.serialize()
    }), 200
    
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

#planets endpoints
@app.route('/planets', methods=['GET'])
def planets():
    try:
        planets = Planets.query.all()
        if not planets:
            return jsonify({"msg":"No planets were found"}), 400

        return jsonify({
        "msg": "OK",
        "results": [p.serialize() for p in planets]
    }), 200
    except Exception as e:
        print(f"Error al obtener planetas: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

#endpoits planet especifico
@app.route('/planets/<int:planets_id>', methods=['GET'])
def planet_by_id(planets_id):
    try:
        planet= Planets.query.get(planets_id)
        if not planet:
            return jsonify({"msg":"No planets were found"}), 400

        return jsonify({
        "msg": "OK",
        "results": planet.serialize()
    }), 200
    except Exception as e:
        print(f"Error al obtener planetas: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

#endpoints people
@app.route('/people', methods=['GET'])
def people():
    try:
        people = People.query.all()
        if not people:
            return jsonify({"msg":"No people were found"}), 400

        return jsonify({
        "msg": "OK",
        "results": [p.serialize() for p in people]
    }), 200
    except Exception as e:
        print(f"Error al obtener personajes: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500

#endpoints people especifico
@app.route('/people/<int:people_id>', methods=['GET'])
def people_by_id(people_id):
    try:
        character = People.query.get(people_id)
        if not character:
            return jsonify({"msg":"No character were found"}), 400

        return jsonify({
        "msg": "OK",
        "results": character.serialize()
    }), 200
    except Exception as e:
        print(f"Error al obtener personajes: {e}")
        return jsonify({"msg": "Internal Server Error", "error": str(e)}), 500


#def favorite

def add_favorite (user_id, item_id, item_model, fav_model, field_name):
    user= User.query.get(user_id)
    if not user:
        return jsonify({"msg":"User not found"}), 400
    item= item_model.query.get(item_id)
    if not item:
        return jsonify({"msg":"Item not found"}), 400
    new_fav= fav_model(user_id=user_id, **{field_name: item_id})
    db.session.add(new_fav)
    db.session.commit()

    return jsonify({"msg": "Favorite added successfully"}), 200

#post data planet

@app.route("/user/<int:user_id>/favorite/planets", methods=["POST"])
def add_fav_planet(user_id):
    planet_id = request.json.get("planet_id")

    if not planet_id:
        return jsonify({"msg": "planet_id is required"}), 400

    return add_fav_planet(
        user_id=user_id,
        item_id=planet_id,
        item_model=Planets,
        fav_model=FavoritePlanets,
        field_name="id_planet"
    )

#post data people

@app.route("/user/<int:user_id>/favorite/people", methods=["POST"])
def add_fav_people(user_id):
    people_id = request.json.get("people_id")

    if not people_id:
        return jsonify({"msg": "people_id is required"}), 400

    return add_fav_people(
        user_id=user_id,
        item_id=people_id,
        item_model=People,
        fav_model=FavoritePeople,
        field_name="id_people"
    )

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


