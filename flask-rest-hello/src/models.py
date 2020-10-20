from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    role = db.Column(db.Boolean(), nullable=False.)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
    def _generateId(self):
        return randint(0, 99999999)

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    cellphone = db.Column(db.Integer, unique=True, nullable=False)
    role = db.Column(db.Boolean(), nullable=False.)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "cellphone": self.cellphone
        }
    
    def _generateId(self):
        return randint(0, 99999999)


class Billing_details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cardNumber = db.Column(db.Integer, nullable=False)
    cvv = db.Column(db.Integer, nullable=False)
    month = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    #user_email = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=True)

    def serialize(self):
        return{
            "id": self.id,
            "cardNumber": self.cardNumber,
            "cvv": self.cvv,
            "month": self.month,
            "year":self.year,
         
        }
    
    def _generateId(self):
        return randint(0, 99999999)


class Billing_details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cardNumber = db.Column(db.Integer, nullable=False)
    cvv = db.Column(db.Integer, nullable=False)
    month = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    #user_email = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=True)

    def serialize(self):
        return{
            "id": self.id,
            "cardNumber": self.cardNumber,
            "cvv": self.cvv,
            "month": self.month,
            "year":self.year,
         
        }
    
    def _generateId(self):
        return randint(0, 99999999)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(50), nullable=False) #se agrega ya que está en el formulario de "create order".
    streetAddress = db.Column(db.String(50), nullable=False)
    commune = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    invoice_id = db.Column(db.Integer, nullable=False)
    office_id = db.Column(db.Integer, nullable=False)
    products = db.Column(db.String(50), nullable=False)
    courrier = db.Column(db.String(50), nullable=False) #se agrega courrier.
    client_email = db.Column(db.String(50), nullable=False)
    cellphone = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False)
    #user_email = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=True)

    def serialize(self):
        return{
            "id": self.id,
            "client_name": self.client_name,
            "streetAddress": self.streetAddress,
            "commune": self.commune,
            "city": self.city,
            "invoice_id": self.invoice_id,
            "office_id": self.office_id,
            "products": self.products,
            "courrier": self.courrier,
            "client_email": self.client_email,
            "cellphone": self.cellphone,
            "confirmed": self.confirmed,
            #"user_email": self.user_email,
        }
    
    def _generateId(self): 
        return randint(0, 99999999)



