import os
import secrets
from datetime import datetime

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
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
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

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            cur.close()
            conn.close()
            user_id = user[0]
            token = generate_token(user_id)
            user_data = {"id": user[0],  "firstname": user[1], "surname": user[2],  "username": user[3], "birthdate": user[4], "email": user[5],  "fav_sports": user[6], "gender": user[7], "postal_code": user[8]}
            #kein Passwort
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
            return abort(404)
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            cur.execute(
                'INSERT INTO users (firstname, surname, username, password, birthdate, email, fav_sports, gender, postal_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (firstname, surname, username, hashed_password, birthdate, email, fav_sports, gender, postal_code))
            conn.commit()

            cur.close()
            conn.close()

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


if __name__ == '_main_':
    app.secret_key = secrets.token_hex(16)
    app.run(debug=True)