import os
import secrets

import psycopg2
from flask import Flask, render_template, request, url_for, redirect, flash, abort
import bcrypt

app = Flask(__name__)


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
            users_json = {"id": user[0], "username": user[1], "password": user[2]}
            return jsonify(users_json)

        else:
            return abort(404)
        cur.close()

    conn.close()


@app.route('/register', methods=['POST'])
def register():
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
        existing_user = cur.fetchone()

        if existing_user:
            return abort(404)
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
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


if __name__ == '__main__':
    app.secret_key = secrets.token_hex(16)
    app.run(debug=True)
