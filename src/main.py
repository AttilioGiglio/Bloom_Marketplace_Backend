"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import json
import bcrypt
import re
import random
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Client, Supplier, Information, Product, Order, Img, Inventory
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)


app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
app.config['JWT_SECRET_KEY'] = 'fuckyou!!Youcan/tstolemy1password!bitch123456789987654321'
jwt = JWTManager(app)


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
        password = request.json.get('password', None)
        email = request.json.get('email', None)
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        client = Client(
            name=new_client["name"], 
            email=new_client["email"], 
            password=hashed,
            role=new_client["role"]
        )

        db.session.add(client)
        db.session.commit()
        return jsonify(client.serialize()), 200

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
    role = request.json.get('role', None)

    if not email:
        return jsonify({"msg": "No existe email"}), 400
    if not password:
        return jsonify({"msg": "No existe clave"}), 400

    user = Client.query.filter_by(email=email).first()
    print(user)

    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        access_token = create_access_token(identity=user.id, expires_delta=False)
        return {"access_token":access_token}, 200
    else:
        return 'Password erronea!'

    return jsonify(user.serialize()), 200

@app.route('/token_client', methods=['GET'])
@jwt_required
def token_client():
    user = Client.query.get(get_jwt_identity())
    return jsonify(user.serialize()), 200

@app.route("/signup_business", methods=["POST", "GET"])
def signupSupplier():
    if request.method == "POST":
        new_supplier = json.loads(request.data)
        password = request.json.get('password', None)
        email = request.json.get('email', None)
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        supplier = Supplier(
            name=new_supplier["name"], 
            email=new_supplier["email"], 
            password=hashed,
            role=new_supplier["role"]
        )
        db.session.add(supplier)
        db.session.commit()
        return jsonify(supplier.serialize()), 200

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
    role = request.json.get('role', None)

    if not email:
        return jsonify({"msg": "No existe email"}), 400
    if not password:
        return jsonify({"msg": "No existe clave"}), 400

    user = Supplier.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"msg": "No existe usuario con ese correo"}), 404
    
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        access_token = create_access_token(identity=user.id, expires_delta=False)
        return {"access_token":access_token}, 200
    else:
        return 'Password erronea'

    return jsonify(user.serialize()), 200

@app.route('/token_business', methods=['GET'])
@jwt_required
def token_supplier():
    user = Supplier.query.get(get_jwt_identity())
    return jsonify(user.serialize()), 200

@app.route("/profile_business/<id>", methods=["POST"])
def postProfileBusiness(id):
    info_supplier = json.loads(request.data)
    info_old = Information.query.filter_by(business_id=info_supplier["business_id"], business_legal_name=info_supplier["business_legal_name"]).filter_by(supplier_id=id).first()
    if info_old is None:
        information = Information(
            business_legal_name=info_supplier["business_legal_name"], 
            business_id=info_supplier["business_id"],
            card_name=info_supplier["card_name"], 
            card_number=info_supplier["card_number"], 
            cvv=info_supplier["cvv"],
            date=info_supplier['date'],
            address=info_supplier["address"], 
            comuna=info_supplier["comuna"],
            region=info_supplier["region"],
            supplier_id=id
        )
        db.session.add(information)
        db.session.commit()
        return jsonify({"exitoso": True}), 200
    if info_old is not None:
        info_old = Information.query.filter_by(supplier_id=id).first()
        info_old.business_legal_name = request.json.get('business_legal_name', info_old.business_legal_name)
        info_old.business_id = request.json.get('business_id', info_old.business_id)
        info_old.card_name = request.json.get('card_name', info_old.card_name)
        info_old.card_number = request.json.get('card_number', info_old.card_number)
        info_old.cvv = request.json.get('cvv', info_old.cvv)
        info_old.date = request.json.get('year', info_old.date)
        info_old.address = request.json.get('address', info_old.address) 
        info_old.comuna = request.json.get('comuna', info_old.comuna) 
        info_old.region = request.json.get('region', info_old.region)
        db.session.commit()
        return jsonify({"msge": "Actualizacion de pefil realizado"}), 200

@app.route("/profile_business/<id>", methods=["GET"])
def putProfileBusiness(id):
    if request.method == "GET":
        if id is not None:
            information = Information.query.filter_by(supplier_id=id).first()
            return jsonify(information.serialize()), 200

@app.route('/add_product_business/<id>', methods=['POST'])
def postProduct(id):

    new_product = json.loads(request.data)
    product_name = None
    # start new code to fix to discriminate between new and old product.. I am doing with the name because if not I will need to set de sku_id on the front to the backend.
    # I think this code for name I should do it on models
    name_by_product = Product.query.filter_by(supplier_id=id).all()
    for item in name_by_product:
        if item.name == new_product["name"]:
            product_name = item.name
        else:
            product_name = new_product["name"]
    
    # finish new code to fix to discriminate between new and old product

    sku_id = new_product['sku_id'] if product_name == new_product["name"] else random.randint(1,999999) 
    
    # sku_id = new_product['sku_id'] if "sku_id" in new_product else random.randint(1,999999) 

    product_old = Product.query.filter_by(sku_id=sku_id).filter_by(supplier_id=id).first()

    if product_old is None:
        product = Product(
            category=new_product['category'],
            sku_id=sku_id, 
            name=new_product["name"], 
            description=new_product["description"],
            quantity_in=new_product['quantity_in'],
            price=new_product["price"],
            supplier_id=id
        )
        
        inventory = Inventory()
        inventory['total_supplier_stock'] = new_product['quantity_in']
        db.session.add(product)
        db.session.commit()
        return jsonify(product.serialize()), 200

    if product_old is not None:
        stock_old_product= product_old.quantity_in + new_product['quantity_in']
        inventory_query = Inventory.query.filter_by(product_id=product_old.id).first()
        inventory_query.total_supplier_stock = stock_old_product
        db.session.commit()
        return jsonify(inventory_query.serialize()), 200

@app.route('/product_cards', methods=['GET'])
def getAllProduct():
    products = Product.query.all()
    all_products = list(map(lambda product: product.serialize(), products))
    return jsonify(all_products)

# Create order (adding all products from checkout to initialization new object from class Order) + Update Stock from Inventory Table.
@app.route('/checkout_step_one/<id>', methods=['POST'])
def postShoppingCart(id):
# bring from endpoint json data post it from client-side and turn it from json data to python code.
    new_order = json.loads(request.data)

    sales_tax =  new_order["total"] * 0.05

    order_number = random.randint(1, 99999999)

    payment_id = random.randint(1, 99999999)
# Initialitate a new object from class Order
    order = Order(
            order_number = order_number,
            payment_id = payment_id,
            total = new_order["total"],
            sale_tax = sales_tax,
            status = True,
            client_id = id
        )
        

    db.session.add(order)

    db.session.commit()

    id_list = list(map(lambda item: item["id"], new_order["products"]))

    product_list = db.session.query(Product).filter(Product.id.in_(id_list)).all()
    print(product_list)

    order_query = Order.query.filter_by(id=order.id).first()
 
    for product in product_list:
        order_query.products.append(product)
        db.session.commit()
        
    for product in new_order['products']:
        product_old = Product.query.filter_by(id=product['id']).first()
        if stock_old is not None:
            product_old.quantity_out = product['quantity_out']
            db.session.commit()
        stock_old = Inventory.query.filter_by(product_id=product['id']).first()
        if stock_old is not None:
            stock_old.total_supplier_stock = stock_old.total_supplier_stock - product['quantity_out']
            db.session.commit()
        return jsonify({"exitoso": True}), 200             

@app.route('/orders_list_business/<id>', methods=['GET'])
def getOrders(id):

    order_query = Order.query.filter(Order.products.any(Supplier.id == id)).all()
    order_list = list(map(lambda order: order.serialize_by_supplier(id), order_query))

    return jsonify({"response": order_list}),200


@app.route('/products_list_business/<id>', methods=['GET'])
def getProductsByOrder(id):
 
    order_filter = Order.query.filter_by(id=id).first()
    products = list(map(lambda item: item.serialize(), order_filter.products))
    
    return jsonify({"exitoso": products}), 200

@app.route('/summary_business/<id>', methods=['GET'])
# supplier id
def getSummaryBusinessData(id):

    # supplier_product_list = Product.query.filter_by(supplier_id=id)
    # # products = list(map(lambda item: item.serialize(), supplier_product_list))

    # totale_supplier_stock = 0
    # for product in supplier_product_list:
    #     totale_supplier_stock += product.quantity
    
    # inventory = Inventory(
    #     total_supplier_stock = totale_supplier_stock
    # )

    

    return jsonify({"stock":total_supplier_stock}), 200
    
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=PORT, debug=False)