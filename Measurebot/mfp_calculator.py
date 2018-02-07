import pymysql.cursors
import requests
import configparser
from datetime import timedelta, date
import datetime

config = configparser.ConfigParser()

"""Change to relative path"""
config.read('/Users/JGarza/Desktop/Nutrition_coach/config.cfg')

connection = pymysql.connect(host = config['mysql']['host'],
                             user = config['mysql']['user'],
                             password = config['mysql']['password'],
                             db = config['mysql']['db'],
                             cursorclass=pymysql.cursors.DictCursor)

yesterday = date.today() - timedelta(1)
two_days_ago = date.today() - timedelta(2)

with connection.cursor() as cursor:
    sql = "SELECT * FROM daily_totals WHERE user_id=1 AND date BETWEEN CAST('{0}' AS DATE) AND CAST('{1}' AS DATE);".format(two_days_ago, yesterday)
    cursor.execute(sql)
    result = cursor.fetchall()

carb_total = 0
carb_counter = 0
protein_total = 0
protein_counter = 0
fat_total = 0
fat_counter = 0
    
for r in result:
    carb_total = carb_total + r['carbs']
    protein_total = protein_total + r['protein']
    fat_total = fat_total + r['fat']

    carb_counter += 1
    protein_counter += 1
    fat_counter += 1

carb_average = carb_total/carb_counter
protein_average = protein_total/protein_counter
fat_average = fat_total/fat_counter
calorie_average = carb_average*4 + protein_average*4 + fat_average*9



print(carb_average)
print(protein_average)
print(fat_average)
print(calorie_average)