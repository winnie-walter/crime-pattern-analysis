from app import app
from flask import jsonify, request, abort,render_template, url_for,json
import flask
import os
import re
import json
from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2 #pip install psycopg2 
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash

DB_HOST = "localhost"
DB_NAME = "crime"
DB_USER = "postgres"
DB_PASS = "raphael"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route('/crime-charts.html')
def crime_charts():
    if 'loggedin' in session:
     return render_template('crime-charts.html')
    return redirect(url_for('login'))


@app.route('/crime-locator.html')
def crime_locator():
    if 'loggedin' in session:
     return render_template('crime-locator.html')
    return redirect(url_for('login'))


from prediction import *
from werkzeug.utils import secure_filename
@app.route('/crime-predictor.html', methods = ['GET', 'POST'])
def crime_predictor():
    if 'loggedin' in session:
     if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        print('file uploaded successfully')
     return render_template('crime-predictor.html')
    return redirect(url_for('login'))

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if 'loggedin' in session:
     if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      #return 'file uploaded successfully'
    #   predictfun()
     return render_template('crime-predictor.html')
    return redirect(url_for('login'))
      

@app.route('/feed.html')
def feed():
    if 'loggedin' in session:
     return render_template('feed.html')
    return redirect(url_for('login'))


@app.route('/about.html')
def about():
    if 'loggedin' in session:
     return render_template('about.html')
    return redirect(url_for('login'))

@app.route('/help-page.html')
def helppage():
    if 'loggedin' in session:
     return render_template('help-page.html')
    return redirect(url_for('login'))


from webscapper import *
@app.route('/',methods=['GET','POST'])
@app.route('/index.html')
def index():
    request_method=request.method
    if 'loggedin' in session:
        if request.method=='POST':
            webscrappingfun()
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['pass']
        
 
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        # Fetch one record and return result
        account = cursor.fetchone()
 
        if account:
            password_rs = account['password']
            
            # If account exists in users table in out database
            if check_password_hash(password_rs, password):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                # Redirect to home page
                return redirect('/')
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect username/password')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password')
 
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print('yes')
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST':
        # Create variables for easy access
        # fullname = request.form['fullname']
        # username = request.form['username']
        password = request.form['pass']
        username = request.form['email']
        
        _hashed_password = generate_password_hash(password)
 
        #Check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
       
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        # elif not re.match(r'[^@]+@[^@]+\.[^@]+', username):
        #     flash('Invalid username address!')
        # elif not re.match(r'[A-Za-z0-9]+', username):
        #     flash('Username must contain only characters and numbers!')
        # elif not username or not password or not username:
        #     flash('Please fill out the form!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            cursor.execute("INSERT INTO users (username, password) VALUES (%s,%s)", (username, _hashed_password))
            conn.commit()
            flash('You have successfully registered!')
            return redirect(url_for('/login'))
            
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('register.html')
   
   
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/profile')
def profile(): 
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM users WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
    
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))