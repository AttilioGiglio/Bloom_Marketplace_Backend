from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
            # do not serialize the password, its a security breach
        }
    
    def _generateId(self):
        return randint(0, 99999999)

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)

    address_business = db.relationship('Address_business', backref='supplier', uselist=False)
    billing_card_business = db.relationship('Billing_card_business', backref='supplier', uselist=False)
    billing_info_business = db.relationship('Billing_info_business', backref='supplier', uselist=False)
    product = db.relationship('Product', backref='supplier')

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "email": self.email
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
            "card_name": 
            "card_number": self.cardNumber,
            "cvv": self.cvv,
            "month": self.month,
            "year":self.year
         
        }
    
    def _generateId(self):
        return randint(0, 99999999)


class Address_business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.Integer, unique=True, nullable=False)
    comuna = db.Column(db.Integer, nullable=False)
    region = db.Column(db.String(50), nullable=False)

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


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku_id = db.Column(db.Integer, unique=True, nullable=False )
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text(), length=None, nullable=False)
    quantity = db.Column(db.Integer, nullable=False )
    price = db.Column(db.Integer, nullable=False )
    img = db.Column(db.LargeBinary, nullable=False )
    date = db.Column(db.DateTime, nullable=False)
    
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)

    def serialize(self):
        return{
            "id" = self.id 
            "sku_id" = self.sku_id
            "name" = self.name
            "description" = self.description
            "quantity" = self.quantity
            "price" = self.price
            "img" = self.img
            "date" = self.date
        }
    
    def _generateId(self): 
        return randint(0, 99999999)


class Product_Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)

    def serialize(self):
        return{

        }
    
    def _generateId(self): 
        return randint(0, 99999999)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.Integer, unique=True, nullable=False )
    payment_id = db.Column(db.Text(), length=None, nullable=False)
    total = db.Column(db.Integer, nullable=False )
    date = db.Column(db.String(150), nullable=False)
    status = db.Column(db.Integer, nullable=False )
    sale_tax = db.Column(db.Integer, nullable=False )
    
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

    def serialize(self):
        return{
            "id" = self.id 
            "order_number" = self.order_number
            "payment_id" = self.payment_id
            "total" = self.total
            "date" = self.date
            "status" = self.status
            "sale_tax" = self.sale_tax
        }
    
    def _generateId(self): 
        return randint(0, 99999999)