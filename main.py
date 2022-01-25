from flask import Flask, redirect, request
import random
import string
import json
import os
import mysql.connector as database

app = Flask(__name__)


def randStr(chars=string.ascii_uppercase + string.digits, N=10):
    return ''.join(random.choice(chars) for _ in range(N))


@app.route('/', methods=['POST'])
def create_short():
    connection = database.connect(
        user='root',
        password=os.environ['db_password'],
        host=data['db_host'],
        database=os.environ['db_name'])

    cursor = connection.cursor()

    long_url = str(request.headers.get('url'))

    try:
        rand_str = randStr()
        statement = "INSERT INTO url_mapping (long_url, short_url, expire_time) VALUES (%s, %s, DATE_ADD(NOW(), INTERVAL %s MINUTE ))"
        gap = (long_url, rand_str, data['expire_time'],)
        cursor.execute(statement, gap)
        connection.commit()
        return "db-service:8080/" + rand_str
    except database.Error as e:
        return 'error'


@app.route('/<short_url>', methods=['GET'])
def open_short(short_url):
    connection = database.connect(
        user='root',
        password='ZmFyYXo=',
        host="db-service",
        database='dXJs')

    cursor = connection.cursor()
    try:
        statement = "SELECT long_url FROM url_mapping WHERE short_url=%s && expire_time > NOW()"
        gap = (short_url,)
        cursor.execute(statement, gap)
        long_url = cursor.fetchall()
        if len(long_url) == 0:
            return "wrong url"
        redirect_url = str(long_url[-1][0])
        return redirect(redirect_url, code=302)
        
    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")
        return ('error2',data['db_host'])

if __name__ == '__main__':

    try:
        json_config_file = open("config.json")
        data = json.load(json_config_file)
    except:
        json_config_file = open("Local_Config.json")
        data = json.load(json_config_file)
        
            
    #if os.path.exists('config.json'):
    #    with open("config.json") as json_config_file:
    #        data = json.load(json_config_file)
    #else:
    #    with open("Local_Config.json") as json_config_file:
    #        data = json.load(json_config_file)
            

    app.run(host="0.0.0.0", debug=True, port=data['server_port'])
