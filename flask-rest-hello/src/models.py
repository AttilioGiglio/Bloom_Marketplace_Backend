from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(250))
    role = db.Column(db.String(150))

    order = db.relationship('Order', backref='client', lazy=True, uselist=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # "order": list(map(lambda x: x.serialize(), self.order))
            # do not serialize the password, its a security breach
        }
    
    def serialize_orders(self):
        return{
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "order": list(map(lambda x: x.serialize(), self.order))
        }

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(250))
    role = db.Column(db.String(150))

    information = db.relationship('Information', backref='supplier', uselist=False)
    product = db.relationship('Product', backref='supplier', lazy=True) #uselist=False

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            # "information": list(map(lambda x: x.serialize(), self.information)),
            # "product": list(map(lambda x: x.serialize(), self.product))
            # do not serialize the password, its a security breach
        }

class Information(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_legal_name = db.Column(db.String(150), unique=True)
    business_id = db.Column(db.Integer, unique=True)
    card_name = db.Column(db.String(150))
    card_number = db.Column(db.Integer)
    cvv = db.Column(db.Integer)
    month = db.Column(db.String(50))
    year = db.Column(db.Integer)
    address = db.Column(db.String(200))
    comuna = db.Column(db.String(100))
    region = db.Column(db.String(100))

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'),  nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "business_legal_name": self.business_legal_name,
            "card_name": self.card_name,
            "card_number": self.card_number,
            "cvv": self.cvv,
            "month": self.month,
            "year":self.year,
            "address": self.address,
            "comuna": self.comuna,
            "region": self.region,
            "suppplier_id": self.supplier_id,
        }
        
productorder = db.Table('productorder',
    db.Column("product_id", db.Integer, db.ForeignKey("product.id"), primary_key=True),
    db.Column("order_id", db.Integer, db.ForeignKey("order.id"),  primary_key=True)
)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku_id = db.Column(db.Integer)
    name = db.Column(db.String(150))
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    img = db.Column(db.String(600))
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    orders = db.relationship("Order", secondary=productorder, lazy=True)

    def serialize(self):
        return{
            "id": self.id,
            "sku_id": self.sku_id,
            "name": self.name,
            "description": self.description,
            "quantity": self.quantity,
            "price": self.price,
            "img": self.img,
            "suppplier_id": self.supplier_id,
            "orders": list(map(lambda x: x.serialize(), self.orders))
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.Integer, unique=True)
    payment_id = db.Column(db.Text)
    total = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    sale_tax = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    products = db.relationship('Product', secondary=productorder, lazy=True)

    def serialize(self):
        return{
            "id": self.id, 
            "order_number": self.order_number,
            "payment_id": self.payment_id,
            "total": self.total,
            "date": self.date,
            "status": self.status,
            "sale_tax": self.sale_tax,
            "products": list(map(lambda x: x.serialize(), self.products))
        }
