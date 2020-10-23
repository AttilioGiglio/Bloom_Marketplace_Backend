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
from models import db, Client, Supplier, Information, Product, Order
from datetime import datetime
from flask_uploads import UploadSet, configure_upload, IMAGES

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

photos = UploadsSet('PHOTOS', IMAGES)
app.config['UPLOAD_PHOTOS_DEST'] = '/pictures'

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
        return jsonify({"exitoso": True}), 200

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
        return jsonify({"exitoso": True}), 200

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
def postProfileBusiness():
    info_supplier = json.loads(request.data)

    information = Information(
        business_legal_name=info_supplier["business_legal_name"], 
        business_id=info_supplier["business_id"],
        card_name=info_supplier["card_name"], 
        card_number=info_supplier["card_number"], 
        cvv=info_supplier["cvv"],
        month=info_supplier["month"],
        year=info_supplier["year"],
        address=info_supplier["address"], 
        comuna=info_supplier["comuna"],
        region=info_supplier["region"],
        supplier_id=info_supplier["supplier_id"]
    )

    db.session.add(information)
    db.session.commit()
    return jsonify({"exitoso": True}), 200

@app.route("/profile_business/<id>", methods=["PUT", "GET"])
def putProfileBusiness(id):
    if request.method == "PUT":
        if id is None:
            return jsonify({"msge": "bad request"}), 400        

        information = Information.query.filter_by(supplier_id=id).first()
        information.business_legal_name = request.json.get('business_legal_name', information.business_legal_name)
        information.business_id = request.json.get('business_id', information.business_id)
        information.card_name = request.json.get('card_name', information.card_name)
        information.card_number = request.json.get('card_number', information.card_number)
        information.cvv = request.json.get('cvv', information.cvv)
        information.year = request.json.get('year', information.year)
        information.address = request.json.get('address', information.address) 
        information.comuna = request.json.get('comuna', information.comuna) 
        information.region = request.json.get('region', information.region)

        db.session.commit()
        return jsonify({"msge": "Actualizacion de pefil realizado"}), 200
    
    if request.method == "GET":
        if id is not None:
            information = Information.query.filter_by(supplier_id=id).first()
            return jsonify(information.serialize()), 200

@app.route('/add_product_business', methods=['POST'])
def postProduct():
    new_product = json.loads(request.data)

    product = Product(
            sku_id=new_product["sku_id"], 
            name=new_product["name"], 
            description=new_product["description"],
            quantity=new_product["quantity"],
            img=new_product["img"],
            price=new_product["price"],
            date=datetime.now(),
            supplier_id=new_product["supplier_id"]
        )
  
    db.session.add(product)
    db.session.commit()
    return jsonify({"exitoso": True}), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
