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

    user = Client.query.filter_by(email=email, role="client").first()

    if user is None:
        return jsonify({"msg": "No existe usuario con ese correo"}), 404

    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        access_token = create_access_token(identity={"email":email})
        return {"access_token":access_token}, 200
    else:
        return 'Password erronea'

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

    user = Supplier.query.filter_by(email=email, password=password, role="business").first()

    if user is None:
        return jsonify({"msg": "No existe usuario con ese correo"}), 404
    
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        access_token = create_access_token(identity={"email":email})
        return {"access_token":access_token}, 200
    else:
        return 'Password erronea'

    return jsonify(user.serialize()), 200

@app.route('/token_business', methods=['GET'])
@jwt_required
def token_supplier():
    user = Supplier.query.get(get_jwt_identity())
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
        db.session.add(information)
        db.session.commit()
        return jsonify({"msge": "Actualizacion de pefil realizado"}), 200
    
    if request.method == "GET":
        if id is not None:
            information = Information.query.filter_by(supplier_id=id).first()
            return jsonify(information.serialize()), 200

@app.route('/add_product_business/<id>', methods=['POST'])
def postProduct(id):

    new_product = json.loads(request.data)
    sku_id=new_product["sku_id"]
    product_old = Product.query.filter_by(sku_id=sku_id).filter_by(supplier_id=id).first()

    if product_old is None:
        product = Product(
            sku_id=sku_id, 
            name=new_product["name"], 
            description=new_product["description"],
            quantity=new_product['quantity'],
            price=new_product["price"],
            supplier_id=new_product["supplier_id"]
        )
        
        db.session.add(product)
        db.session.commit()
        return jsonify(product.serialize()), 200

    product_old.sku_id = sku_id
    product_old.name = new_product['name']
    product_old.description = new_product["description"]
    product_old.quantity = product_old.quantity + new_product['quantity']
    product_old.price = new_product["price"]
    product_old.supplier_id = new_product["supplier_id"]
    db.session.add(product_old)
    db.session.commit()
    return jsonify(product_old.serialize()), 200

@app.route('/product_cards', methods=['GET'])
def getAllProduct():
    products = Product.query.all()
    all_products = list(map(lambda product: product.serialize(), products))
    imgs = Img.query.all()
    all_img = list(map(lambda img: img.serialize(), imgs))
    return jsonify(all_products, all_img)

@app.route('/checkout_step_one', methods=['POST'])
def postShoppingCart():

    new_order = json.loads(request.data)
    sales_tax =  new_order["total"] * 0.05
    order_number = random.randint(1, 99999999)
    payment_id = random.randint(1, 99999999)

    order = Order(
            order_number = order_number,
            payment_id = payment_id,
            total = new_order["total"],
            sale_tax = sales_tax,
            status = True,
            client_id = new_order["client_id"]
        )
  
    db.session.add(order)
    db.session.commit()
    
    id_list = list(map(lambda item: item["sku_id"], new_order["products"]))
    product_list = db.session.query(Product).filter(Product.sku_id.in_(id_list))
    order_query = Order.query.filter_by(id=order.id).first()

    for product in product_list:
        order_query.products.append(product)
        stock_old = Inventory.query.filter_by(product_id=product.id).first()
        if stock_old is not None:
            quantity=list(map(lambda item: item.id == product.id, new_order['products']))
            stock_old.total_supplier_stock = stock_old.total_supplier_stock - quantity['quantity']
            db.session.add(stock_old)
            db.session.commit()
            return jsonify({"exitoso": stock_old.serialize()}), 200
    return jsonify({"msg":"Ningun producto tiene inventario"}), 400
        

@app.route('/orders_list_business', methods=['GET'])
def getOrders():
    order_query_all = Order.query.all()
    
    if order_query_all is not None:
    
        all_orders = list(map(lambda order: order.serialize(), order_query_all))

        id_tuple = list(map(lambda item: item.client_id, order_query_all))
        client_order = db.session.query(Client).filter(Client.id.in_(id_tuple))
        all_clients = list(map(lambda order_client: order_client.serialize(), client_order))

        return jsonify({"response": all_clients},{"response": all_orders}), 200

@app.route('/products_list_business/<id>', methods=['GET'])
def getProductsByOrder(id):
 
    order_filter = Order.query.filter_by(id=id).first()
    products = list(map(lambda item: item.serialize(), order_filter.products))
    
    return jsonify({"exitoso": products}), 200

@app.route('/summary_business/<id>', methods=['GET'])
def getStock(id):

    supplier_product_list = Product.query.filter_by(supplier_id=id)
    products = list(map(lambda item: item.serialize(), supplier_product_list))

    total_supplier_stock = 0
    for product in supplier_product_list:
        total_supplier_stock += product.quantity
    
    inventory = Inventory(
        total_supplier_stock = total_supplier_stock
    )

    return jsonify({"exitoso":total_supplier_stock}), 200
    
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT, debug=False)