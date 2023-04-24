
import json
import os
from app import app
from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2 #pip install psycopg2 
import psycopg2.extras
import re 
import pandas as ps
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import *
@app.route('/crime-charts.html')
def crime_charts():
    if 'loggedin' in session:
     uss = session['is_admin']
     datas = pd.read_csv('fulljsondata2016.csv')
     datas = datas['STATE_UT'][1:-2]
     type = CrimeType.query.all()
     location = Location.query.all()
     data = CrimeData.query.all()
     return render_template('crime-charts.html',data=data,type=type,location=location,uss=uss)
    return redirect(url_for('login'))





@app.route('/crime-locator.html')
def crime_locator():
    if 'loggedin' in session:
     uss = session['is_admin']
     return render_template('crime-locator.html',uss=uss)
    return redirect(url_for('login'))


@app.route('/data')
def data():
    if 'loggedin' in session:
     uss = session['is_admin']
     location = Location.query.all()
     type = CrimeType.query.all()
     return render_template('data.html',uss=uss,location=location,type=type)
    return redirect(url_for('login'))



@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    if 'loggedin' in session:
     uss = session['is_admin']
     if request.method == 'POST':
        fullname = request.form['name']
        username = request.form['email']
        locations = request.form['location']
        phoneNumber = request.form['number']
        is_staff = True
        password = '12345'
        usr = User.query.filter_by(username=username).first()
        if usr:
            flash('User exists')
            return redirect(url_for('adduser'))
        else:
            user = User(fullname=fullname,username=username,location_id=locations,phoneNumber=phoneNumber,is_staff=is_staff)
            user.set_password(password)
            with app.app_context():
                db.session.add(user)
                db.session.commit()
            flash('User created successful')
            return redirect(url_for('adduser'))
        
     else:
      location = Location.query.all()
      return render_template('adduser.html',location=location,uss=uss)
    return redirect(url_for('login'))

from prediction import *
from werkzeug.utils import secure_filename
@app.route('/crime-predictor.html', methods = ['GET', 'POST'])
def crime_predictor():
    if 'loggedin' in session:
     uss = session['is_admin']
     if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        print('file uploaded successfully')
     return render_template('crime-predictor.html',uss=uss)
    return redirect(url_for('login'))

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if 'loggedin' in session:
     uss = session['is_admin']
     if request.method == 'POST':
      f = request.files['file']
      
      folder = 'static/assets/datasets'
      
      path = f'{folder}/{f.filename}'
      if os.path.isfile(os.path.join(folder,f.filename)):
          flash('file exists')
          return redirect(url_for('data'))
      else:
        col = ['STATE_UT','DISTRICT','YEAR','MURDER','RAPE','CHILD_DESERTION','UNNATURAL_OFFENCE','DEFILEMENT','TOTAL_IPC_CRIMES']
        if f.filename.endswith('.xlsx'):
         df = ps.read_excel(f)
         
         df.insert(loc=df.columns.get_loc('STATE_UT')+1,column='DISTRICT', value='TOTAL')
         df = df.sort_values('STATE_UT')
         df = df.reset_index(drop=True).dropna()
         if list(df.columns)!=col:
            flash('upload file with same data columns name')
            return redirect(url_for('data'))
         else:
           # print(len(col))
            year=df['YEAR'][0]
            datas = df.to_dict(orient='records')
            
            #print(year)
            j = f'static/assets/files/{year}.json'
            
            with open(j, 'w') as g:
                json.dump(datas,g)
            data = CrimeData(year=year,filename=j)
            d = CrimeData.query.filter_by(year=year).first()
            if d:
                flash('File of that year exists')
                return redirect(url_for('data'))
            else:
                with app.app_context():
                    db.session.add(data)
                    db.session.commit()
                
                    df.to_excel(f'{folder}/{f.filename}',index=False)
                flash('file uploaded successfully')
                return redirect(url_for('data'))
        else:
           flash('Excel files only required') 
           return redirect(url_for('data'))
      #return 'file uploaded successfully'
    #   predictfun()
     
    return redirect(url_for('login'))
      

@app.route('/feed.html')
def feed():
    if 'loggedin' in session:
     uss = session['is_admin']
     return render_template('feed.html',uss=uss)
    return redirect(url_for('login'))


@app.route('/about.html')
def about():
    if 'loggedin' in session:
     uss = session['is_admin']
     return render_template('about.html',uss=uss)
    return redirect(url_for('login'))

@app.route('/help-page.html')
def helppage():
    if 'loggedin' in session:
     uss = session['is_admin']
     return render_template('help-page.html',uss=uss)
    return redirect(url_for('login'))


from webscapper import *
@app.route('/',methods=['GET','POST'])
@app.route('/index.html')
def index():
    
    if 'loggedin' in session:
        uss = session['is_admin']
        type = CrimeType.query.all()
        location = Location.query.all()
        data = CrimeData.query.all()
        if request.method=='POST':
            webscrappingfun()
        return render_template('index.html',uss=uss,type=type,location=location,data=data)
    return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    #cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['pass']
        # Check if account exists using MySQL
        #cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        # Fetch one record and return result
        #account = cursor.fetchone()
 
        #if account:
            #password_rs = account['password']
         
            # If account exists in users table in out database
        users =  User.query.filter_by(username=username).first()
        # print(user.password)
        # print(len(user.set_password(password)))
        # print(user.check_password(password))
        #print(user and user.check_password(password))
        if users and users.check_password(password):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                # session['id'] = user.id
                
                session['username'] = username
                session['is_admin'] = users.is_admin
               
                # Redirect to home page
                return redirect('/')
        else:
                # Account doesnt exist or username/password incorrect
                print('nooooooooooooooooooooo')
                flash('Incorrect username/password')
                # print('no')
        # else:
        #     # Account doesnt exist or username/password incorrect
        #     flash('Incorrect username/password')
 
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    #cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
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
        # cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        # account = cursor.fetchone()
       
        # If account exists show error and validation checks
        # if account:
            # flash('Account already exists!')
        # elif not re.match(r'[^@]+@[^@]+\.[^@]+', username):
        #     flash('Invalid username address!')
        # elif not re.match(r'[A-Za-z0-9]+', username):
        #     flash('Username must contain only characters and numbers!')
        # elif not username or not password or not username:
        #     flash('Please fill out the form!')
        # else:
        #     # Account doesnt exists and the form data is valid, now insert new account into users table
        #     cursor.execute("INSERT INTO users (username, password) VALUES (%s,%s)", (username, _hashed_password))
        #     conn.commit()
        #     flash('You have successfully registered!')
            # return redirect(url_for('/login'))
            
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

# @app.route('/profile')
# def profile(): 
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
#     # Check if user is loggedin
#     if 'loggedin' in session:
#         cursor.execute('SELECT * FROM users WHERE id = %s', [session['id']])
#         account = cursor.fetchone()
#         # Show the profile page with account info
#         return render_template('profile.html', account=account)
#     # User is not loggedin redirect to login page
#     return redirect(url_for('login'))

@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
    
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))