from flask import request, redirect, url_for, jsonify, g, abort
from flask_httpauth import HTTPBasicAuth
from datetime import datetime, date
import datetime, time, calendar
from statistics import mean
import numpy as np
from flask_mail import Message

from app import app, db, mail
from models import User, Goals, DailyTotals, Measurements
from calories_generator import MacrosGenerator


auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email_or_token, password):
    user_id = User.verify_auth_token(email_or_token)
    print(user_id)
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        print(user)
    else:
        user = User.query.filter_by(email=email_or_token).first()
        print(user)
        if (not user) and (not user.verify_password(password)):
            return False
    if not user.account_activated:
        return False
    g.user = user
    print(g.user)
    return True
    

@app.route("/")
def home():
    return jsonify({'message': 'Welcome'})

@app.route("/users", methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')

        if not email or not password:
            abort(400)
        
        try:
            user = User(email=email, password=password)
            # user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            activation_key = user.generate_activation_key()
            activation_url = "http://localhost:8081/activate/" + activation_key
            msg = Message(
                              sender=app.config['MAIL_USERNAME'],
                              subject='testing',
                              body='Activation URL: ' + activation_url,
                              recipients=["josh@sf-iron.com"])
            mail.send(msg)
            goal = Goals(user_id = user.id)
            db.session.add(goal)
            db.session.commit()
            return jsonify({'email': user.email, 'user_id': user.id, 'activation_url': activation_url}), 201
        except Exception as e:
            print(e)
            abort(422)

@app.route("/activate/<activation_key>")
def activate_user(activation_key):
    user_id = User.verify_activation_key(activation_key)
    # print(user_id)
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        user.account_activated = True
        user.activated_at = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        print(user)
        return jsonify({'user_id': user.id})
    else:
        abort(400)



@app.route("/token")
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token})

@app.route("/user")
@auth.login_required
def user():
    return jsonify({'email': g.user.email, 'user_id': g.user.id}), 200
    
    
@app.route("/goals")
@auth.login_required
def goals():
    goals = Goals.query.filter_by(user_id=g.user.id).order_by(Goals.date.desc()).limit(1).all()
    # print(goal)
    return jsonify([g.as_dict() for g in goals]), 200
    
@app.route("/goals", methods=['POST'])
@auth.login_required    
def set_macros():
    existing_goal = Goals.query.filter_by(user_id=g.user.id).filter_by(date=date.today()).first()
    # print(existing_goal.date)
    # print(date.today())
    goal_protein = int(request.json.get('protein'))
    goal_carbs = int(request.json.get('carbs'))
    goal_fat = int(request.json.get('fat'))
    if existing_goal:
        # existing_goal = Goals(g.user.id, goal_protein, goal_carbs, goal_fat)
        existing_goal.protein = goal_protein
        existing_goal.carbs = goal_carbs
        existing_goal.fat = goal_fat
        existing_goal.calc_calories()
    else:
        new_goal = Goals(g.user.id, goal_protein, goal_carbs, goal_fat)
        db.session.add(new_goal)
    db.session.commit()
    #     create new goals row
    return jsonify({'message':'POST Received'}), 200
        
        
@app.route("/macros")
@auth.login_required
def macros():
    macros = DailyTotals.query.filter_by(user_id=g.user.id).limit(7).all()
    print(macros)

    return jsonify([m.as_dict() for m in macros]), 200  

@app.route("/generator", methods=['POST'])     
@auth.login_required
def generate_macros():
    list_dates = []
    list_weights = []
    list_calories = []
    training_cycle = "bulk"

    macros = DailyTotals.query.filter_by(user_id=1).limit(14).all()
    measurements = Measurements.query.filter_by(user_id=1).limit(14).all() 

    for m in macros:
        list_dates.append(m.date.toordinal())
        list_calories.append(m.calories)

    for w in measurements:
        list_weights.append(w.weight)

    dates = np.asarray(list_dates)
    weights = np.asarray(list_weights)
    calories = np.asarray(list_calories)

    return jsonify(MacrosGenerator(dates, weights, calories, training_cycle).assignment)