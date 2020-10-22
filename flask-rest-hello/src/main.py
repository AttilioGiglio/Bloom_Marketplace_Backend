"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Client
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

@app.route("/signup_client", methods=["POST", "GET"])
def signupClient():
    if request.method == "POST":
        new_client = json.loads(request.data)
        client = Client(name=new_client["name"], email=new_client["email"], password=new_client["password"],
                        role=new_client["role"])
        db.session.add(client)
        db.session.commit()
        return jsonify({"success": True}), 200
    if request.method == "GET":
        client_signup = Client.query.all()
        all_client_signup = list(map(lambda client: client.serialize(), client_signup))
        return jsonify(all_client_signup), 200

@app.route("/login_client", methods=["POST"])
def loginClient():
    current_user = json.loads(request.data)
    if not request.is_json:
        return jsonify({"msg": "No existe JSON en la consulta"}), 400
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"msg": "No existe correo"}), 400
    if not password:
        return jsonify({"msg": "No existe clave"}), 400
    user = Client.query.filter_by(email=email).first()
    return jsonify(user.serialize_orders()), 200

@app.route("/signup_business", methods=["POST"])
def getloginBusiness():

        return jsonify({"success": True}), 201 

@app.route("/login_business", methods=["POST"])
def loginBusiness():
    
        return jsonify(data), 400

@app.route("/login_business", methods=["GET"])
def getLoginBusiness():
    

    return jsonify(logins_json)


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
