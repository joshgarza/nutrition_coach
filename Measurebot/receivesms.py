import configparser
from twilio.rest import Client
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import re
import pymysql
import pymysql.cursors
from datetime import date


config.read('/Users/JGarza/Desktop/Nutrition_coach/config.cfg')

config.read('config.cfg')


ACCT_SID = config['twilio']['acct_sid']
AUTH_TOKEN = config['twilio']['auth_token']
TWILIO_NUMBER = config['twilio']['phone_number']

app = Flask(__name__)

@app.route("/send")
def send_question():
    user_name = request.args['user_name']
    user_number = request.args['user_number']
    client = Client(ACCT_SID, AUTH_TOKEN)
    message = client.messages.create(
        to=user_number,
        from_=TWILIO_NUMBER,
        body="Hey " + user_name + ", Josh here. What's your weight today?")
    return(message.sid)

@app.route("/receive", methods=['GET', 'POST'])
def user_response():
    """Respond to incoming calls with a simple text message."""
    user_response = request.form['Body']
    resp = MessagingResponse()
    matches = re.findall('\d+\.\d+', user_response)
    if not matches:
        matches = re.findall('\d+', user_response)
    """write conditional if more than one number is sent
    for instance: 'hey josh, i weighed 200 yesterday and today i weigh 201.'"""
    if matches:
        # weight, phone_number
        weight = matches[0]
        phone_number = request.form['From']
        if insert_measurement(weight, phone_number):
            resp.message("Thanks! Your weight has been logged.")
        else:
            resp.message("Something went wrong. Try again.")
    else:
        resp.message("Invalid response. Please enter a valid weight.")
    return str(resp)

def insert_measurement(weight, phone_number):
    try:
        connection = pymysql.connect(host = config['mysql']['host'],
                                 user = config['mysql']['user'],
                                 password = config['mysql']['password'],
                                 db = config['mysql']['db'],
                                 cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT id FROM user WHERE phone_number = '{}';".format(phone_number)
            cursor.execute(sql)
            result = cursor.fetchone()
            user_id = result['id']
            measurement_date = str(date.today())
            insert_sql = "INSERT INTO measurements (user_id, date, weight)\
                          VALUES ('{0}', '{1}', '{2}')\
                          ON DUPLICATE KEY UPDATE weight = '{2}';"\
                          .format(str(user_id), measurement_date, str(weight))
                          # TO DO: 
                            # triple quotes
                            # format sql variable
            cursor.execute(insert_sql)
            connection.commit()
            return True
    except Exception as e:
        print(e)
        return False
    finally:
        connection.close()



if __name__ == "__main__":
    app.run(debug=True)


