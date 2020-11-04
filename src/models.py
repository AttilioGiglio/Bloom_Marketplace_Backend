from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(250))
    role = db.Column(db.String(150))

    order = db.relationship('Order', backref='client', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(250))
    role = db.Column(db.String(150))

    information = db.relationship('Information', backref='supplier', uselist=False)
    product = db.relationship('Product', backref='supplier', lazy=True)

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
        }

class Information(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_legal_name = db.Column(db.String(150), unique=True)
    business_id = db.Column(db.Integer, unique=True)
    card_name = db.Column(db.String(150))
    card_number = db.Column(db.Integer)
    cvv = db.Column(db.Integer)
    date= db.Column(db.String(150))
    address = db.Column(db.String(200))
    comuna = db.Column(db.String(100))
    region = db.Column(db.String(100))

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'),  nullable=False)

    def serialize(self):
        return{
            "business_legal_name": self.business_legal_name,
            "card_name": self.card_name,
            "card_number": self.card_number,
            "cvv": self.cvv,
            "date":self.date,
            "address": self.address,
            "comuna": self.comuna,
            "region": self.region,
            "suppplier_id": self.supplier_id,
        }

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_supplier_stock = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)  

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def serialize(self):
       return{
           "total_supplier_stock": self.total_supplier_stock,
           "product_id": self.product_id
       }       

productorder = db.Table('productorder',
    db.Column("product_id", db.Integer, db.ForeignKey("product.id"), primary_key=True),
    db.Column("order_id", db.Integer, db.ForeignKey("order.id"),  primary_key=True)
)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(150))
    sku_id = db.Column(db.String(300))
    name = db.Column(db.String(150))
    description = db.Column(db.Text)
    quantity_in = db.Column(db.Integer)
    quantity_out = db.Column(db.Integer)
    price = db.Column(db.Integer)
    img = db.Column(db.String(500))
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)  
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    
    inventory = db.relationship('Inventory', backref='product', lazy=True, uselist=False)
    orders = db.relationship("Order", secondary=productorder, lazy=True)

    def serialize(self):
        return{
            "id": self.id,
            "category": self.category,
            "sku_id": self.sku_id,
            "name": self.name,
            "description": self.description,
            "quantity_in": self.quantity_in,
            "quantity_out": self.quantity_out,
            "price": self.price,
            "img": self.img,
            "suppplier_id": self.supplier_id
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.Integer, unique=True)
    payment_id = db.Column(db.Integer, unique=True)
    total = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    sale_tax = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    
    products = db.relationship('Product', secondary=productorder, lazy=True)

    def serialize(self):
        products = list(map(lambda product: product.serialize(), self.products))
        return{
            "id": self.id,
            "order_number": self.order_number,
            "payment_id": self.payment_id,
            "total": self.total,
            "status": self.status,
            "sale_tax": self.sale_tax,
            "date": self.date,
            "client_id":self.client_id,
            'client':self.client.name,
            "products": products
        }

    def serialize_by_supplier(self, supplier_id):
        # products = list(filter(lambda product: product if product.supplier_id == supplier_id else None, self.products ))
        products = list(map(lambda product: product.serialize(), self.products))
        return{
            "id": self.id,
            "order_number": self.order_number,
            "payment_id": self.payment_id,
            "total": self.total,
            "status": self.status,
            "sale_tax": self.sale_tax,
            "date": self.date,
            "client_id":self.client_id,
            'client':self.client.name,
            "products": products
        }

class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary)
    name = db.Column(db.String(300))
    
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "data": self.data,
            "name": self.name,
        }