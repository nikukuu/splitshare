from flask import Flask, render_template, url_for, redirect, request, session
import os
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'uwu'

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "splitshare"

mysql = MySQL(app)

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute(f"select username, password from user where username = {username}")
        user = cur.fetchone()
        cur.close()
        if user is None:
            return render_template('base.html', error ='You do not have an account')
        elif username and password == user[1]:
            session['username'] = user[0]
            return render_template('home.html')
        else:
            return render_template('base.html', error ='Invalid or wrong password')
    return render_template('base.html')

@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO register (email, username, password) VALUES (%s, %s, %s)", (email, username, password))

        mysql.connection.commit() 

        cur.close()
    return render_template('sign_up.html')

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
