from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    role = db.Column(db.String(150), nullable=False)

    order = db.relationship('Order', backref='client', lazy=True) #uselist=False

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            # "id": self.id,
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
        
    def _generateId(self):
        return randint(0, 99999999)

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    role = db.Column(db.String(150), nullable=False)

    address_business = db.relationship('Address_business', backref='supplier', uselist=False)
    billing_card_business = db.relationship('Billing_card_business', backref='supplier', uselist=False)
    billing_info_business = db.relationship('Billing_info_business', backref='supplier', uselist=False)
    product = db.relationship('Product', backref='supplier', lazy=True) #uselist=False

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "address_business": list(map(lambda x: x.serialize(), self.address_business)),
            "billing_card_business": list(map(lambda x: x.serialize(), self.billing_card_business)),
            "billing_info_business": list(map(lambda x: x.serialize(), self.billing_info_business)),
            "product": list(map(lambda x: x.serialize(), self.product))
            # do not serialize the password, its a security breach
        }
    
    def _generateId(self):
        return randint(0, 99999999)

class Billing_info_business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_legal_name = db.Column(db.String(150), nullable=False)
    business_id = db.Column(db.Integer, nullable=False)

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'),  nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "business_legal_name": self.business_legal_name,
            "business_id": self.business_id
        }
    
    def _generateId(self):
        return randint(0, 99999999)

class Billing_card_business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_name = db.Column(db.String(150), nullable=False)
    card_number = db.Column(db.Integer, nullable=False)
    cvv = db.Column(db.Integer, nullable=False)
    month = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'),  nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "card_name": self.card_name,
            "card_number": self.cardNumber,
            "cvv": self.cvv,
            "month": self.month,
            "year":self.year
         
        }
    
    def _generateId(self):
        return randint(0, 99999999)


class Address_business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), unique=True, nullable=False)
    comuna = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'),  nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "address": self.name_address,
            "comuna": self.comuna,
            "region": self.region
        }
    
    def _generateId(self):
        return randint(0, 99999999)
        
product_order = db.Table('product_order',
    db.Column("product_id", db.Integer, db.ForeignKey("product.id"), primary_key=True),
    db.Column("order_id", db.Integer, db.ForeignKey("order.id"),  primary_key=True)
)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku_id = db.Column(db.Integer, unique=True, nullable=False )
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False )
    price = db.Column(db.Integer, nullable=False )
    img = db.Column(db.LargeBinary, nullable=False )
    date = db.Column(db.DateTime, nullable=False)
    
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    orders = db.relationship("Order", secondary=product_order, lazy=True)

    def serialize(self):
        return{
            "id": self.id,
            "sku_id": self.sku_id,
            "name": self.name,
            "description": self.description,
            "quantity": self.quantity,
            "price": self.price,
            "img": self.img,
            "date": self.date,
            "orders": list(map(lambda x: x.serialize(), self.orders))
        }
    
    def _generateId(self): 
        return randint(0, 99999999)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.Integer, unique=True, nullable=False )
    payment_id = db.Column(db.Text, nullable=False)
    total = db.Column(db.Integer, nullable=False )
    status = db.Column(db.Boolean, nullable=False )
    sale_tax = db.Column(db.Integer, nullable=False )
    date = db.Column(db.DateTime, nullable=False)
    
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    products = db.relationship('Product', secondary=product_order, lazy=True)

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
    
    def _generateId(self): 
        return randint(0, 99999999)