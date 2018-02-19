from app import db
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from datetime import date
import random, string


secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True)
    password_hash = db.Column(db.String(256))
    phone_number = db.Column(db.String(20), unique=True)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=60000):
        s = Serializer(secret_key, expires_in = expiration)
        return s.dumps({'id': self.id })

    @staticmethod
    def verify_auth_token(token):
    	s = Serializer(secret_key)
    	try:
    		data = s.loads(token)
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