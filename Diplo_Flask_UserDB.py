import json
import secrets
from datetime import datetime, timedelta
from re import match

import psycopg2
from flask import Flask, render_template, request, url_for, redirect, flash, abort, jsonify
import bcrypt
import jwt
from flask_cors import CORS
from psycopg2.extras import Json

from Captcha.first_main import *

app = Flask(__name__)
cors = CORS(app)


def get_db_connection():
    try:
        conn = psycopg2.connectcon = psycopg2.connect(
            database="SportSpot",
            user="postgres",
            password="htl123",
            host="localhost",
            port='5432'
        )
        return conn
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None


def generate_token(user):
    payload = {
        'user_id': user[0],
        'exp': datetime.utcnow() + timedelta(hours=1),
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token


def decode_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        # Handle expired token
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        # Handle invalid token
        print("Invalid Token")
        return None


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return abort(404)

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return abort(404)

    conn = get_db_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cur.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[4].encode('utf-8')):
            cur.close()
            conn.close()

            token = generate_token(user)

            # kein Passwort
            return jsonify({'token': token})

        else:
            return abort(404)


# Konvertiert das Geschlecht da Auswahl zwischen (male, female, other), aber Speicherung in der Datenbank
# als (m, f, o)
def convert_gender(gender):
    return gender[0].lower() if gender in ['male', 'female'] else 'o'


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return abort(404)
    firstname = data.get('firstname')
    surname = data.get('surname')
    username = data.get('username')
    password = data.get('password')
    birthdate = data.get('birthdate')
    email = data.get('email')
    fav_sports = data.get('sports')
    gender = convert_gender(data.get('gender'))
    postal_code = data.get('postalcode')

    if not username or not password:
        return abort(404)
    conn = get_db_connection()
    if conn is not None:
        cur = conn.cursor()

        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        existing_user = cur.fetchone()

        if existing_user:
            cur.close()
            conn.close()
            return jsonify({'message': 'Username already exists'}), 400  # Return an error
        else:
            # Verifizierung
            if not firstname or len(firstname.strip()) < 2:
                return jsonify({'message': 'Vorname muss mindestens 2 Zeichen lang sein'}), 400

            if not surname or len(surname.strip()) < 2:
                return jsonify({'message': 'Nachname muss mindestens 2 Zeichen lang sein'}), 400

            if not username or len(username.strip()) < 2:
                return jsonify({'message': 'Username muss mindestens 2 Zeichen lang sein'}), 400

            if match(r"^(?=.*\d)(?=.*[A-Z]).{9}$", password):
                return jsonify(
                    {'message': 'Das Passwort muss eine Ziffer, einen Großbuchstaben und neun Zeichen lang sein'}), 400

            if not email or '@' not in email:
                return jsonify({'message': 'Vorname muss mindestens 2 Zeichen lang sein'}), 400

            if not postal_code:
                return jsonify({'message': 'Wir benötigen als Sicherheitsmaßnahme ihre Postleizahl'}), 400

            if not fav_sports:  # nicht mehr benötigt?
                fav_sports = []

            if not gender:
                gender = 'o'

            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

            cur.execute(
                'INSERT INTO users (firstname, surname, username, password, birthdate, email, fav_sports, '
                'gender, postal_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (firstname, surname, username, hashed_password.decode('utf-8'), birthdate, email, fav_sports, gender,
                 postal_code))
            conn.commit()

            cur.close()
            conn.close()
            return jsonify({'message': 'Registration successful'}), 201
    else:
        return abort(404)


@app.route('/allUsers', methods=['GET'])
def get_all_users():
    conn = get_db_connection()
    if conn is not None:
        cur = conn.cursor()

        cur.execute('SELECT * FROM users')
        users = cur.fetchall()

        cur.close()
        conn.close()
        users_json = [{"id": row[0], "username": row[1]} for row in users]
        return jsonify(users_json)
    else:
        return abort(404)


@app.route('/saveSportsToUser', methods=['POST'])
def save_sports_to_user():
    data = request.get_json()
    if not data:
        return abort(404)
    email = data.get('email')
    sports = data.get('selectedSports')

    conn = get_db_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute('UPDATE users SET fav_sports = %s WHERE email = %s;', (sports, email))
        conn.commit()
        return jsonify({'message': f'Sports to user with the email {email} successfully changed'}), 201
    return jsonify({'message': 'sports could not be added'}), 404


@app.route('/delete/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute('DELETE FROM users WHERE id = %s;', (user_id,))
        conn.commit()
        return jsonify({'message': f'User {user_id} successfully deleted'}), 201

    return jsonify({'message': 'not deleted'}), 404


@app.route('/maps/add', methods=['POST'])
def event_hinzuegen():
    data = request.get_json()
    if not data:
        return jsonify({'message': f'Bad Request: Keine Daten'}), 400
    print(data)
    jwt_data = data.get('jwt')
    payload = decode_token(jwt_data)

    dataset = {
        'event_loc': data['coords'],
        'sport': data['sport'],
        'user_id': payload["user_id"],
        'event_date': data['startdate'],
        'event_name': "Event name",
        'info': data['description'],
        'difficulty': data['difficulty'],
        'participants': data['participants'],
        'duration': data['duration'],
    }

    event_loc = dataset.get('event_loc')
    sport = dataset.get('sport')
    creator_id = dataset.get('user_id')
    event_date = dataset.get('event_date')
    type = "p"  # am Anfang nur 'p'
    event_name = dataset.get('event_name')
    info = dataset.get('info')
    max_participants = dataset.get('max_participants')
    duration = dataset.get('duration')
    difficulty = dataset.get('difficulty')

    print(dataset)

    if None in [event_loc, sport, creator_id, event_date, type, event_name]:
        return jsonify({'message': 'Bad Request: Fehlende Daten'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        if type == 'p':
            eventPoint = data.get('eventPoint')
            #jsonstring = json.dumps(eventPoint)
            #ElJson = json.dumps(event_loc)
            #print(event_loc)
            #print(ElJson)
            json_string_in_quotes = str(event_loc).replace('[', '{').replace(']', '}')
            event_loc_convert = '{{"latitude": {}, "longitude": {}}}'.format(event_loc[0], event_loc[1])

            info = "Test"
            print(event_loc_convert)
            print(json_string_in_quotes)
            cur.execute(
                'SELECT insert_event_point(%s::jsonb,%s, %s, %s, %s, %s, %s, %s, %s, %s);',
                (
                    event_loc_convert, sport, creator_id, event_date, type, event_name, info,
                    max_participants, duration, difficulty
                )
            )
            conn.commit()
            return jsonify({'message': f'Sucessful'}), 201
        elif type == 'r':
            eventRoute = data.get('eventRoute')
            cur.execute(
                'INSERT INTO event_route (event_loc, sport, creator_id, event_date, type, event_name, eventRoute, '
                'info, max_participants) VALUES (ST_GeomFromGeoJSON(%s), %s, %s, %s, %s, %s, ST_GeogFromGeoJSON(%s), '
                '%s, %s)',
                (
                    Json(event_loc), sport, creator_id, event_date, type, event_name, Json(eventRoute), info,
                    max_participants))
            return jsonify({'message': f'Sucessful'}), 201
        else:
            return jsonify({'message': f'Not Found: Eventtyp nicht gefunden'}), 404

    except Exception as e:
        print(e)
        return jsonify({'message': f'Internal Server Error: {str(e)}'}), 500
    finally:
        cur.close()
        conn.close()


@app.route('/maps/anzeigen', methods=['POST'])
def event_anzeigen():
    data = request.get_json()
    event_id = data.get('event_id')
    if not event_id:
        return jsonify({'message': f'Bad Request'}), 400
    else:
        conn = get_db_connection()
        if conn is not None:
            cur = conn.cursor()
            cur.execute("SELECT type FROM event WHERE event_id = %s;", (event_id,))
            result = cur.fetchone()
            if result is not None:
                v_event_type = result[0]
                if v_event_type == 'p':
                    cur.execute("SELECT * FROM event_point WHERE event_id = %s;", (event_id,))

                elif v_event_type == 'r':
                    cur.execute("SELECT * FROM event_route WHERE event_id = %s;", (event_id,))
                event = cur.fetchone()
                return jsonify({'message': f'Sucessful'}, event), 201
            else:
                return jsonify({'message': f'Bad Request'}), 400

        else:
            return jsonify({'message': f'Internal Server Error'}), 500


@app.route('/maps', methods=['GET'])
def all_events():
    conn = get_db_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute('SELECT event_id, event_loc, sport FROM event')
        events = cur.fetchall()
        cur.close()
        conn.close()
        event_json = [{"event_id": row[0], "event_loc": row[1], "sport": row[2]} for row in events]
        return jsonify(event_json)
    else:
        return abort(404)


@app.route('/map/test', methods=['POST'])
def test_point_data():
    data = request.get_json()
    jwt_data = data.get('jwt')
    payload = decode_token(jwt_data)
    print(payload["user_id"])

    print("data")
    print(data)

    dataset = {
        'event_loc': data['coords'],
        'sport': data['sport'],
        'user_id': payload["user_id"],
        'event_date': data['startdate'],
        'event_name': "Event name",
        'info': data['description'],
        'difficulty': data['difficulty'],
        'participants': data['participants'],
        'duration': data['duration'],
    }

    print("dataset")
    print(dataset)

    if not data:
        return jsonify({'message': f'Bad Request: Keine Daten'}), 400


##########
# Captcha
##########
@app.route("/getCaptcha", methods=["GET"])
def get_captcha_data():
    svg_path = 'Captcha/captcha.svg'

    text_captcha = generate_captcha_text(5)
    create_captcha_svg(text_captcha)

    with open(svg_path, 'r') as svg_file:
        svg_content = svg_file.read()

    conn = get_db_connection()

    # Saving the SVG content and creating an ID
    if conn is not None:
        cur = conn.cursor()
        cur.execute('INSERT INTO captcha (text) VALUES (%s) RETURNING id', (text_captcha,))
        last_captcha_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    else:
        print("Not possible to save captcha")

    response_data = {
        'captcha_id': last_captcha_id,
        'svg': svg_content
    }

    return jsonify(response_data)


@app.route("/compareInput", methods=["POST"])
def compare_captcha_input():
    data = request.get_json()
    if not data:
        return abort(404)
    captcha_id = data.get('id')
    captcha_input = data.get('input')

    conn = get_db_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute('SELECT * FROM captcha WHERE id = %s and text = %s', (captcha_id, captcha_input))
        found = cur.fetchone()

        if found:
            return jsonify({'message': f'Captcha successfully passed'}), 201


###########
# JWT TOKEN
###########
'''
@app.route("/getUserFromJWT", methods=["GET"])
def get_user_from_jwt():
    data = request.get_json()
'''

# Muss fertiggemacht werden
'''
@app.route("/getExpirationTime", methods=["POST"])
def getExpirationTime():
    data = request.get_json()
    if not data:
        return abort(404)
    jwt = data.get('token')

'''

if __name__ == '__main__':
    # Dieser Secret Key sollte aus Sicherheitsgründen außerhalb vom Code liegen
    app.secret_key = secrets.token_hex(16)
    app.run(debug=True)
