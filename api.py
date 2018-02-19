from flask import request, redirect, url_for, jsonify, g, abort
from flask_httpauth import HTTPBasicAuth
from datetime import datetime, date
import datetime, time, calendar
from statistics import mean
import numpy as np

from app import app, db
from models import User, Goals, DailyTotals, Measurements
from calories_generator import MacrosGenerator


auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username_or_token, password):
    print("In verify password")
    user_id = User.verify_auth_token(username_or_token)
    print(user_id)
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        print(user)
    else:
        user = User.query.filter_by(username=username_or_token).first()
        print(user)
        if (not user) and (not user.verify_password(password)):
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
        username = request.json.get('username')
        password = request.json.get('password')
        if not username or not password:
            abort(400)
        
        # existing_user = User.query.filter_by(username = username).first()
        # if existing_user is not None:
        #     print("existing user")
        #     #FIXME: This should verify password, revisit when building login
        #     return jsonify({'message':'user already exists'}), 200
            
        user = User(username = username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        goal = Goals(user_id = user.id)
        db.session.add(goal)
        db.session.commit()
        return jsonify({'username': user.username, 'user_id': user.id}), 201

@app.route("/token")
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    print(token.decode('ascii'))
    return jsonify({'token': token.decode('ascii')})

@app.route("/user")
@auth.login_required
def user():
    return jsonify({'username': g.user.username, 'user_id': g.user.id}), 200
    
    
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
# @auth.login_required
def generate_macros():
    # Need to format date to int or something that MacrosGenerator can take
    # training cycle still needs to be added to some table
    list_dates = []
    list_weights = []
    list_calories = []
    training_cycle = "bulk"

    macros = DailyTotals.query.filter_by(user_id=1).limit(14).all()
    measurements = Measurements.query.filter_by(user_id=1).limit(14).all() 

    # x = np.append(x, [[40, 50, 60], [70, 80, 90]])

    for m in macros:
        list_dates.append(m.date.toordinal())
        list_calories.append(m.calories)

    for w in measurements:
        list_weights.append(w.weight)

    dates = np.asarray(list_dates)
    weights = np.asarray(list_weights)
    calories = np.asarray(list_calories)

    # print(dates)
    # print(weights)
    # print(calories)
    
    # b = MacrosGenerator(dates, weights, calories, training_cycle).assignment
    # print("This is the generator")
    # print(b)
    return jsonify(MacrosGenerator(dates, weights, calories, training_cycle).assignment)