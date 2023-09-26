import os
import secrets

import psycopg2
from flask import Flask, render_template, request, url_for, redirect, flash
import bcrypt

app = Flask(__name__)


def get_db_connection():
    try:
        conn = psycopg2.connect(host="localhost",
                                database="users",
                                user=os.environ['John'],
                                password=os.environ['_{>95kfAx5mne&U('])
        return conn
    except psycopg2.Error as e:
        return 404


@app.route('/login/', methods=['POST'])
def login():
    username = request.form['Username']
    password = request.form['Password']

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
            return 404

        cur.close()
        conn.close()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    conn = get_db_connection()
    if conn is not None:
        cur = conn.cursor()

        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        existing_user = cur.fetchone()

        if existing_user:
            return 403  # Http Status
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
            conn.commit()
            return 200  # ?
            return redirect(url_for('login'))

        cur.close()
        conn.close()

    else:

        return 404


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
        return 404


if __name__ == '__main__':
    app.secret_key = secrets.token_hex(16)
    app.run(debug=True)
