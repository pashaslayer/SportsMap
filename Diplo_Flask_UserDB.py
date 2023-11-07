import os
import secrets
from datetime import datetime, timedelta
from typing import re

import psycopg2
from flask import Flask, render_template, request, url_for, redirect, flash, abort, jsonify
from flask_cors import CORS
import bcrypt
import jwt

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


def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1)
        # 'username': username,
        # 'firstname': firstname,
        # 'surname': surname,
        # 'birthdate' : birthdate,
        # 'email' : email,
        # 'fav_sports' : fav_sports,
        # 'gender' : gender,
        # 'postal_code' : postal_code,
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token


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

        # Eventuell spätere Passwortverschlüsselung auf Browserebene

        if user and bcrypt.checkpw(password.encode('utf-8'), user[4].encode('utf-8')):
            cur.close()
            conn.close()
            user_id = user[0]
            token = generate_token(user_id)
            #token = generate_token(user_id, user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8])
            user_data = {"id": user[0],  "firstname": user[1], "surname": user[2],  "username": user[3], "birthdate": user[4], "email": user[5],  "fav_sports": user[6], "gender": user[7], "postal_code": user[8]}
            # kein Passwort
            return jsonify({'token': token, 'user': user_data})

        else:
            return abort(404)
        cur.close()

    conn.close()


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
    fav_sports = data.get('fav_sports')
    gender = data.get('gender')
    postal_code = data.get('postal_code')

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

            if re.match(r"^(?=.*\d)(?=.*[A-Z]).{9}$", password):
                return jsonify({'message': 'Das Passwort muss eine Ziffer, einen Großbuchstaben und neun Zeichen lang sein'}), 400

            if not email or '@' not in email:
                return jsonify({'message': 'Vorname muss mindestens 2 Zeichen lang sein'}), 400

            if not postal_code:
                return jsonify({'message': 'Wir benötigen als Sicherheitsmaßnahme ihre Postleizahl'}), 400

            if not fav_sports:
                fav_sports = {}

            if not gender:
                gender = 'o'

            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

            cur.execute(
                'INSERT INTO users (firstname, surname, username, password, birthdate, email, fav_sports, '
                'gender, postal_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (firstname, surname, username, hashed_password.decode('utf-8'), birthdate, email, fav_sports, gender, postal_code))
            conn.commit()

            cur.close()
            conn.close()
            return jsonify({'message': 'Registration successful'}), 201  # Return a success
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


if __name__ == '__main__':
    app.secret_key = secrets.token_hex(16)
    app.run(debug=True)
