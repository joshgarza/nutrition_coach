import pymysql
import pymysql.cursors
import requests
import configparser
import receivesms


config = configparser.ConfigParser()

config.read('/Users/JGarza/Desktop/Nutrition_coach/config.cfg')

connection = pymysql.connect(host = config['mysql']['host'],
                             user = config['mysql']['user'],
                             password = config['mysql']['password'],
                             db = config['mysql']['db'],
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT name, phone_number FROM user;"
        cursor.execute(sql)
        result = cursor.fetchall()

for r in result:
    user_dict = {'user_name': r['name'], 'user_number': r['phone_number']}
    requests.get('http://localhost:5000/send', params=user_dict)

      

