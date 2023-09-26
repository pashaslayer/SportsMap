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
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cur.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            cur.close()
            conn.close()
            return redirect(url_for('index'))
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
            return abort(404)  # Return an appropriate response indicating that the user already exists.
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
            conn.commit()  # Commit the transaction to save the changes to the database.

            cur.close()
            conn.close()

            return "User registered successfully"  # Return a success message or a redirect if needed.

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

        return users

    else:
        return abort(404)


if __name__ == '__main__':
    app.secret_key = secrets.token_hex(16)
    app.run(debug=True)
