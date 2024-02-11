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
import smtp as smtp 

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
        'exp': datetime.utcnow() + timedelta(minutes=15),
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token


def decode_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        raise jwt.ExpiredSignatureError
    except jwt.InvalidTokenError:
        print("Invalid Token")
        return None


def get_user_map_data(data):
    if not data:
        return jsonify({'message': f'Bad Request: Keine Daten'}), 400
    jwt_data = data.get('jwt')
    payload = decode_token(jwt_data)
    dataset = {
        'event_loc': data['coords'],
        'user_id': payload['user_id'],
    }

    event_loc = dataset.get('event_loc')
    event_loc_convert = '{{"latitude": {}, "longitude": {}}}'.format(event_loc[0], event_loc[1])

    user_id = dataset.get('user_id')
    return user_id, event_loc_convert

# Funktion für die Ausgabe von Werten
def printout(data):
    print(data)


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


@app.route('/user', methods=['POST'])
def userprofile():
    data = request.get_json()
    if not data:
        return jsonify({'message': f'Bad Request: Keine Daten'}), 400
    jwt_data = data.get('jwt')
    payload = decode_token(jwt_data)

    user_id = payload.get('user_id')

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
        user = cur.fetchone()  # Fetches the first row from the result
        conn.commit()
        cur.close()
        conn.close()
        if user is None:
            return jsonify({'message': 'User not found'}), 404
        
        userdata = {
        'userid': user[0],
        'firstname': user[1],
        'surname': user[2],
        'username': user[3],
        'birthdate': user[5],
        'email': user[6],
        'sports': user[7],
        'gender': user[8],
        'postalcode': user[9],
        }
        
        return userdata, 200

    except Exception as e:
        print(e)
        return jsonify({'message': f'Internal Server Error: {str(e)}'}), 500


@app.route('/delete/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute('DELETE From event_participants WHERE user_id = %s;'
                    'DELETE FROM event WHERE creator_id = %s;'
                    'DELETE FROM Event_point WHERE creator_id = %s;'
                    'DELETE FROM users WHERE user_id = %s;', (user_id, user_id, user_id, user_id))
        conn.commit()
        return jsonify({'message': f'User {user_id} successfully deleted'}), 201

    return jsonify({'message': 'not deleted'}), 404


@app.route('/maps/add', methods=['POST'])
def event_hinzuegen():
    data = request.get_json()
    if not data:
        return jsonify({'message': f'Bad Request: Keine Daten'}), 400
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
    max_participants = dataset.get('participants')
    duration = dataset.get('duration')
    difficulty = dataset.get('difficulty')

    if None in [event_loc, sport, creator_id, event_date, type, event_name]:
        return jsonify({'message': 'Bad Request: Fehlende Daten'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        if type == 'p':
            eventPoint = data.get('eventPoint')
            # jsonstring = json.dumps(eventPoint)
            # ElJson = json.dumps(event_loc)
            # print(event_loc)
            # print(ElJson)
            json_string_in_quotes = str(event_loc).replace('[', '{').replace(']', '}')
            event_loc_convert = '{{"latitude": {}, "longitude": {}}}'.format(event_loc[0], event_loc[1])

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
def event_anzeigen(): #jetzt auch mit jwt
    data = request.get_json()
    user_id, event_loc_convert = get_user_map_data(data)
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT type, event_id FROM event WHERE event_loc = %s;", (event_loc_convert,))
        result = cur.fetchone()
        # TheMap.vue =>  320
        if result is not None:
            v_event_type = result[0]
            event_id = result[1]
            cur.execute("SELECT * FROM event_participants WHERE event_id = %s AND user_id = %s",
                        (event_id, user_id))
            teilgenommen = cur.fetchone()
            if teilgenommen:
                teilgenommen = True
            else :
                teilgenommen = False

            if v_event_type == 'p':
                cur.execute("SELECT e.event_id, e.event_loc AS event_loc, e.sport AS sport, e.event_date, "
                            "e.type, e.difficulty, e.duration, e.info, e.max_participants, "
                            "e.creator_id AS creator_id, u.firstname AS creator_firstname,"
                            "u.surname AS creator_surname, u.username AS creator_username, EXTRACT(YEAR FROM "
                            "CURRENT_DATE) - EXTRACT(YEAR FROM u.birthdate) AS birthdate, u.email AS "
                            "creator_email, COUNT(ep.user_id) AS participants FROM event_point e JOIN users u "
                            "ON e.creator_id = u.user_id LEFT JOIN event_participants ep ON e.event_id = "
                            "ep.event_id LEFT JOIN users up ON ep.user_id = up.user_id WHERE e.event_loc = %s "
                            "GROUP BY e.event_id, e.event_loc, e.sport, e.event_date, e.type, e.difficulty, "
                            "e.duration, e.info, e.max_participants, e.creator_id,"
                            "u.firstname, u.surname, u.username, u.email, u.user_id; ", (event_loc_convert,))
                event = cur.fetchone()
                if event:
                    event = list(event)
                    output_dict = {
                        "event_id": event[0],
                        "event_loc": event[1],
                        "sport": event[2],
                        "event_date": event[3],
                        "type": event[4],
                        "difficulty": event[5],
                        "duration": event[6],
                        "description": event[7],
                        "max_participants": event[8],
                        "creator_id": event[9],
                        "creator_firstname": event[10],
                        "creator_surname": event[11],
                        "creator_username": event[12],
                        "age": event[13],
                        "creator_email": event[14],
                        "participants": event[15]
                    }

                else:
                    return jsonify({"message": "Event not found"}), 404

            elif v_event_type == 'r':
                cur.execute("SELECT * FROM event_route WHERE event_loc = %s;", (event_loc_convert,))
                event = cur.fetchone()

            return jsonify(output_dict, teilgenommen), 201
        else:
            return jsonify({'message': f'Bad Request'}), 400
    except Exception as e:
        print(e)


@app.route('/maps/anzeigen/teilnehmer', methods=['POST'])
def show_participants():
    data = request.get_json()
    if not data:
        return jsonify({'message': f'Bad Request: Keine Daten'}), 400

    event_loc = data.get('coords')
    event_loc_convert = '{{"latitude": {}, "longitude": {}}}'.format(event_loc[0], event_loc[1])

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT event_id FROM event WHERE event_loc = %s", event_loc_convert)
        event_id = cur.fetchone()

        cur.execute("SELECT * FROM event_participants WHERE event_id = %s", event_id)

        conn.commit()
        return jsonify({'message': 'Successful'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Internal Server Error'}), 500


@app.route('/maps/anzeigen/teilnehmen', methods=['POST'])
def take_part():
    data = request.get_json()
    user_id, event_loc_convert = get_user_map_data(data)
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT event_id FROM event WHERE event_loc = %s", (event_loc_convert,))
        event_id = cur.fetchone()
        cur.execute("SELECT e.max_participants, COUNT(ep.user_id) AS participants FROM event_point e JOIN "
                    "event_participants ep ON e.event_id = ep.event_id WHERE e.event_id = %s GROUP BY "
                    "e.max_participants HAVING COUNT(ep.user_id) = e.max_participants;", event_id)
        full = cur.fetchall()
        if full:
            return jsonify({'message': 'Event ist Voll'}), 404
        
        cur.execute("INSERT INTO public.event_participants(event_id, user_id) VALUES (%s, %s);",
            (event_id, user_id))

        cur.execute("SELECT u.firstname, u.surname, u.Email, e.event_date, e.sport, e.duration, c.firstname, c.surname "
                    "FROM event_participants ep "
                    "JOIN Users u ON ep.user_id = u.user_id "
                    "RIGHT JOIN event_point e ON ep.event_id = e.event_id "
                    "RIGHT JOIN users c ON e.creator_id = c.user_id "
                    "WHERE ep.event_id = %s AND ep.user_id = %s "
                    "GROUP BY u.firstname, u.surname, u.Email, e.event_date, e.sport, e.duration, c.firstname, c.surname;"
                    , (event_id, user_id))
        smtp_data = cur.fetchone()

        # Verschicken einer Email
        email, subject, body = smtp.prepare_mail_enter_event(smtp_data)
        smtp.send_mail(email, body, subject)

        # Email data
        printout(email)
        printout(body)


        conn.commit()
        return jsonify({'message': 'Successful'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Internal Server Error'}), 500


@app.route('/map/anzeigen/verlassen', methods=['POST'])
def delete_particpant():
    data = request.get_json()
    user_id, event_loc_convert = get_user_map_data(data)

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT event_id FROM event WHERE event_loc = %s", (event_loc_convert,))
        event_id = cur.fetchone()


        cur.execute("SELECT u.firstname, u.surname, u.Email, e.event_date, e.sport, e.duration, c.firstname, c.surname "
            "FROM event_participants ep "
            "JOIN Users u ON ep.user_id = u.user_id "
            "RIGHT JOIN event_point e ON ep.event_id = e.event_id "
            "RIGHT JOIN users c ON e.creator_id = c.user_id "
            "WHERE ep.event_id = %s AND ep.user_id = %s "
            "GROUP BY u.firstname, u.surname, u.Email, e.event_date, e.sport, e.duration, c.firstname, c.surname;"
            , (event_id, user_id))
        
        smtp_data = cur.fetchone()

        cur.execute("DELETE FROM event_participants WHERE event_id = %s AND user_id = %s;", (event_id, user_id))

        # Verschicken einer Email
        email, subject, body = smtp.prepare_mail_leave_event(smtp_data)
        smtp.send_mail(email, body, subject)

        conn.commit()

        return jsonify({'message': 'Successful'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Internal Server Error'}), 500


@app.route('/map/anzeigen/delete', methods=['POST'])
def delete_event(): #jetzt auch mit jwt
    data = request.get_json()
    user_id, event_loc_convert = get_user_map_data(data)
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT event_id FROM event WHERE event_loc = %s;", (event_loc_convert,))
        event_id_result = cur.fetchone()

        event_id = event_id_result[0]

        cur.execute("SELECT * FROM event WHERE event_id = %s AND creator_id = %s",
                    (event_id, user_id))
        created = cur.fetchone()
        if created:
             # Execute each DELETE statement separately
            cur.execute("DELETE FROM event_participants WHERE event_id = %s;", (event_id,))
            cur.execute("DELETE FROM event_point WHERE event_id = %s;", (event_id,))
            cur.execute("DELETE FROM event WHERE event_id = %s;", (event_id,))

            conn.commit()  # Don't forget to commit your changes to the database

            return jsonify({'message': 'Successful'}), 200  # Using 200 OK for successful deletion
        else:
            return jsonify({'message': 'No Permission'}), 505
    except Exception as e:
        print(e)
        return jsonify({'message': 'Internal Server Error'}), 500  # Return a 500 Internal Server Error on exception


@app.route('/maps', methods=['POST'])
def all_events():
    data = request.get_json()
    if not data:
        return jsonify({'message': f'Bad Request: Keine Daten'}), 400
    jwt_data = data.get('jwt')
    payload = decode_token(jwt_data)

    creator_id = payload.get('user_id')

    conn = get_db_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute("SELECT event_id, event_loc, sport FROM event WHERE creator_id != %s;", (creator_id,))
        events = cur.fetchall()
        cur.execute("SELECT event_id, event_loc, sport FROM event WHERE creator_id = %s;", (creator_id,))
        my_events = cur.fetchall()
        cur.close()
        conn.close()
        event_json = [{"event_id": row[0], "event_loc": row[1], "sport": row[2]} for row in events]
        my_event_json = [{"event_id": row[0], "event_loc": row[1], "sport": row[2]} for row in my_events]
        event_dict = {"events": event_json, "my_events": my_event_json}
        return jsonify(event_dict)
    else:
        return abort(404)


@app.route('/maps/change', methods=['POST'])
def change_point():
    data = request.get_json()
    if not data:
        return jsonify({'message': f'Bad Request: Keine Daten'}), 400

    dataset = {
        'event_loc': data['coords'],
        'event_date': data['startdate'],
        'info': data['description'],
        'difficulty': data['difficulty'],
        'participants': data['participants'],
        'duration': data['duration'],
    }

    event_id = data['event_id']

    event_loc = dataset.get('event_loc')
    event_date = dataset.get('event_date')
    info = dataset.get('info')
    max_participants = dataset.get('participants')
    duration = dataset.get('duration')
    difficulty = dataset.get('difficulty')

    event_loc = data.get('coords')
    if not event_loc:
        return jsonify({'message': 'Bad Request: Fehlende Koordinaten'}), 400

    event_loc_convert = '{{"latitude": {}, "longitude": {}}}'.format(event_loc[0], event_loc[1])

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE event_point SET event_date = %s, duration = %s, difficulty = %s, max_participants = %s, "
                    "info = %s  WHERE event_loc = %s;", (event_date, duration, difficulty, max_participants, info,
                                                         event_loc_convert,))
        cur.execute("UPDATE event SET event_date = %s WHERE event_loc = %s;", (event_date, event_loc_convert,))

        cur.execute(
            "SELECT u.firstname, u.surname, u.Email, e.sport, c.firstname, c.surname "
            "FROM event_point e "
            "JOIN event_participants ep ON e.event_id = ep.event_id "
            "JOIN users u ON ep.user_id = u.user_id "
            "JOIN users c ON e.creator_id = c.user_id "
            "WHERE e.event_id = %s",
            (event_id,)
        )
        participants = cur.fetchall()

        for participant in participants:
            email, subject, body = smtp.prepare_mail_change_event(participant, event_date, duration)  
            smtp.send_mail(email, body, subject)
          
        conn.commit()
        return jsonify({'message': 'Successful'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Internal Server Error'}), 500


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

@app.route("/jwt/isExpired", methods=["POST"])
def get_expired():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Bad Request: Keine Daten'}), 400
    jwt_data = data.get('jwt')
    try:
        # Assuming you have a method decode_token that correctly validates the token
        decode_token(jwt_data)
    except jwt.ExpiredSignatureError:
        return jsonify({'expired': True}), 401  # 401 Unauthorized
    except Exception as e:  # General exception handling
        return jsonify({'error': str(e)}), 500
    return jsonify({'expired': False}), 200


if __name__ == '__main__':
    # Dieser Secret Key sollte aus Sicherheitsgründen außerhalb vom Code liegen
    app.secret_key = secrets.token_hex(16)
    app.run(debug=True)
