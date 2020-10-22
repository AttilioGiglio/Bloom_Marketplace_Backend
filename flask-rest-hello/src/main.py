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
from models import db, Client, Supplier
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
        client = Client(
            name=new_client["name"], 
            email=new_client["email"], 
            password=new_client["password"],
            role=new_client["role"]
        )
        db.session.add(client)
        db.session.commit()
        return jsonify({"success": True}), 200
    if request.method == "GET":
        client_signup = Client.query.all()
        all_client_signup = list(map(lambda client: client.serialize(), client_signup))
        return jsonify(all_client_signup), 200

@app.route("/login_client", methods=["POST"])
def loginClient():

    if not request.is_json:
        return jsonify({"msg": "No existe JSON en la consulta"}), 400
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"msg": "No existe email"}), 400
    if not password:
        return jsonify({"msg": "No existe clave"}), 400
    user = Client.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"msg": "No existe usuario con ese correo"}), 404
    return jsonify(user.serialize()), 200

@app.route("/signup_business", methods=["POST", "GET"])
def signupSupplier():

    if request.method == "POST":
        new_supplier = json.loads(request.data)
        supplier = Supplier(
            name=new_supplier["name"], 
            email=new_supplier["email"], 
            password=new_supplier["password"],
            role=new_supplier["role"]
        )
        db.session.add(supplier)
        db.session.commit()
        return jsonify({"success": True}), 200
    if request.method == "GET":
        supplier_signup = Supplier.query.all()
        all_supplier_signup = list(map(lambda supplier: supplier.serialize(), supplier_signup))
        return jsonify(all_supplier_signup), 200

@app.route("/login_business", methods=["POST"])
def loginSupplier():

    if not request.is_json:
        return jsonify({"msg": "No existe JSON en la consulta"}), 400
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"msg": "No existe email"}), 400
    if not password:
        return jsonify({"msg": "No existe clave"}), 400
    user = Supplier.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"msg": "No existe usuario con ese correo"}), 404
    return jsonify(user.serialize()), 200

@app.route("/profile_business", methods=["POST"])
def profileBusiness():
    info_supplier = json.loads(request.data)
    billinginfobusiness = BillingInfoBusiness(
        business_legal_name=info_supplier["business_legal_name"], 
        business_id=info_supplier["business_id"] 
    )
    email = request.json.get("email", None)

    user = User.query.filter_by(email=email)
    if user is None:
        return jsonify({"msge": "user dosent exist"}), 400
    db.return_.append(user)
    db.session.add(return_)
    db.session.commit()
    # billing_card_business = Billing_card_business(
    #     card_name=info_supplier["card_name"], 
    #     card_number=info_supplier["card_number"], 
    #     cvv=info_supplier["cvv"],
    #     month=info_supplier["month"],
    #     year=info_supplier["year"],
    # )
    # billing_info_business = Billing_info_business(
    #     address=info_supplier["address"], 
    #     comuna=info_supplier["comuna"],
    #     region=info_supplier["region"],
    # )
    db.session.add(billing_info_business)
    db.session.commit()
    return jsonify({"success": True}), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
