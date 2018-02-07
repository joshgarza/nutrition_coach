import myfitnesspal
import pymysql.cursors
import requests
import configparser
from datetime import timedelta, date
import datetime
from mfp_client_class import NoPasswordClient
from mfp_client_class import FriendClient

config = configparser.ConfigParser()

config.read('/Users/JGarza/Desktop/Nutrition_coach/config.cfg')

connection = pymysql.connect(host = config['mysql']['host'],
                             user = config['mysql']['user'],
                             password = config['mysql']['password'],
                             db = config['mysql']['db'],
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
    sql = "SELECT mfp_username, share_type FROM user;"
    cursor.execute(sql)
    result = cursor.fetchall()

for r in result:
    friend_dict = {'user_name': r['mfp_username'], 'share_type': r['share_type']}
    app_username = config['mfp']['user_name']
    app_password = config['mfp']['password']
    yesterday = date.today() - timedelta(1)
    try:
        """
        Public = Public mfp account
        Private = Friend of app
        App = Application's account
        Else = Null, unknown or unupdated account status
        Sets client to appropriate sharing status or skips them if null.
        """
        if r['share_type'] == 'public':
            client = NoPasswordClient(friend_dict['user_name'])
        elif r['share_type'] == 'private':
            client = FriendClient(friend_dict['user_name'], app_username, app_password)
        elif r['share_type'] == 'app':
            client = myfitnesspal.Client(app_username, app_password)
        else:
            continue
        dy = client.get_date(yesterday)
        total = dy.totals
        """
        Sets correct id in database and inserts mfp totals from yesterday.
        If a client didn't update mfp, a KeyError will appear and cause the app to skip client.
        In the future, we'll set an alert for client/coach when exception KeyError appears.
        """
        with connection.cursor() as cursor:
            sql = "SELECT id FROM user WHERE mfp_username = '{}';".format(friend_dict['user_name'])
            cursor.execute(sql)
            result = cursor.fetchone()
            user_id = result['id']
            # If any KeyErrors pop up, move on to the next user.
            try:
                insert_sql = "INSERT INTO daily_totals (user_id, date, carbs, fat, protein, calories)\
                      VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')\
                      ON DUPLICATE KEY UPDATE carbs = '{2}', fat = '{3}', protein = '{4}', calories = '{5}';"\
                      .format(str(user_id), yesterday, total['carbohydrates'], total['fat'], total['protein'], total['calories'])
                print('Successful')
            except KeyError:
                print('KeyError')
                continue
            cursor.execute(insert_sql)
            connection.commit()
    except ValueError:
        continue
    