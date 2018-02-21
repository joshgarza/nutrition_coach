from app import db
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import(URLSafeTimedSerializer as Serializer, BadSignature, SignatureExpired)
from datetime import date
import random, string
from email_validator import validate_email, EmailNotValidError


auth_secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
activate_secret_key = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(32))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, index=True)
    password_hash = db.Column(db.String(256))
    phone_number = db.Column(db.String(20), unique=True)
    account_activated = db.Column(db.Boolean, default=False)
    activated_at = db.Column(db.DateTime)

    def __init__(self, email, password):
        try:
            v = validate_email(email) # validate and get info
            self.email = v["email"] # replace with normalized form
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            raise(e)

        self.password_hash = self.hash_password(password)

    def hash_password(self, password):
        return pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self):
        s1 = Serializer(auth_secret_key)
        return s1.dumps({'id': self.id })

    def generate_activation_key(self):
        s2 = Serializer(activate_secret_key)
        activation_key = s2.dumps({'id': self.id })
        # print(activation_key + "generate")
        return activation_key

    @staticmethod
    def verify_activation_key(activation_key):
        s2 = Serializer(activate_secret_key)
        # print(s.loads(activation_key))
        # print(s2.loads(activation_key))
        try:
            print(activation_key + " verify")
            data = s2.loads(activation_key, max_age=86400)

        except SignatureExpired as e:
            print("SignatureExpired")
            print(e)
            #Valid Token, but expired
            return None
        except BadSignature as e:
            print("BadSignature")
            print(e)
            #Invalid Token
            return None
        user_id = data['id']
        return user_id

    @staticmethod
    def verify_auth_token(token):
    	s1 = Serializer(auth_secret_key)
    	try:
    		data = s1.loads(token, max_age=86400)
    	except SignatureExpired as e:
            print(e)
            #Valid Token, but expired
            return None
    	except BadSignature as e:
            print(e)
            #Invalid Token
            return None
    	user_id = data['id']
    	return user_id


class Goals(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, primary_key=True, default=None)
    protein = db.Column(db.Integer, nullable=False, default=0)
    carbs = db.Column(db.Integer, nullable=False, default=0)
    fat = db.Column(db.Integer, nullable=False, default=0)
    calories = db.Column(db.Integer, default=0)
    
    def __init__(self, user_id, protein=0, carbs=0, fat=0):
        self.user_id = user_id
        self.date = date.today()
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self.calories = protein*4 + carbs*4 + fat*9
        
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def calc_calories(self):
        self.calories = self.protein*4 + self.carbs*4 + self.fat*9

class DailyTotals(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, primary_key=True, default=None)
    protein = db.Column(db.Integer, nullable=False, default=0)
    carbs = db.Column(db.Integer, nullable=False, default=0)
    fat = db.Column(db.Integer, nullable=False, default=0)
    calories = db.Column(db.Integer, default=0)    

    def __init__(self, user_id, date, protein=0, carbs=0, fat=0):
        self.user_id = user_id
        self.date = date
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self.calories = protein*4 + carbs*4 + fat*9
        
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def calc_calories(self):
        self.calories = self.protein*4 + self.carbs*4 + self.fat*9

class Measurements(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, primary_key=True, default=None)
    weight = db.Column(db.Integer, nullable=False, default=0)  

    def __init__(self, user_id, date, weight=0):
        self.user_id = user_id
        self.date = date
        self.weight = weight