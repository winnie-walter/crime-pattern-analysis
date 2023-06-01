
import json
import os
from app import app
from flask import Flask, request, session, redirect, url_for, render_template, flash
#import psycopg2 #pip install psycopg2 
#import psycopg2.extras
import re 
import pandas as ps
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

def preprocessings(path,year):
    df = pd.read_excel(path)
    df = pd.DataFrame(df)

    df.columns = df.columns.str.title()
    print(df.columns)
    new_data = df.dropna(axis=1,how='all')
    
    # print(new_data.head())
    new_data = new_data.drop(new_data.index[-1])

    #     new_data = new_data.drop(columns=['Human Trafficking','Child Stealing'], axis=1)


    crime = ['Police Region','Murder','Rape','Child Desertion','Unnatural Offence','Defilement']
    drop = []
    for i in new_data.columns:
        if  i not in crime:
            drop.append(i)
    new_data = new_data.drop(columns=drop,axis=1)  
   
    # for crime in crime:
        
    #     new_data[crime]=new_data[crime].astype(str)
    crime = ['Murder','Rape','Child Desertion','Unnatural Offence','Defilement']
    for j in new_data:
        for i in range(len(new_data)):
            new_data[j][i]=new_data[j][i]

        crime = ['Murder','Rape','Child Desertion','Unnatural Offence','Defilement']
        for crime in crime:
            
            new_data[crime]=new_data[crime].astype(float)

    # print(new_data.head())
    crime = ['Murder','Rape','Child Desertion','Unnatural Offence','Defilement']
    for j in new_data:
        for i in range(len(new_data)):
            new_data[j][i]=new_data[j][i]
            
            new_data[crime]=new_data[crime].astype(int)
            new_data['Total']=0
            #total = 0
            for k in new_data.columns[1:]:
                if k not in crime:
                    pass
                else:

                 new_data['Total'] = new_data['Total'] + new_data[k]
        # crime = ['Murder','Rape','Child Desertion','Unnatural Offence','Defilement']
    
  
   
    
    
    regions = [    'Arusha',    'Dar es Salaam',    'Dodoma',    'Geita',    'Iringa',    'Kagera',    'Katavi',    'Kigoma',    'Kilimanjaro',    'Lindi',    'Manyara',    'Mara',    'Mbeya',    'Morogoro',    'Mtwara',    'Mwanza',    'Njombe',    'Pemba North',    'Pemba South',    'Pwani',    'Rukwa',    'Ruvuma',    'Shinyanga',    'Simiyu',    'Singida',    'Songwe',    'Tabora',    'Tanga',    'Unguja North',    'Unguja South',    'Zanzibar Central/South']


    #     num = random.randint(0, 100) 
    #     #print(new_data['Police Region'])
    #     #new_data.to_csv(f'{num}.csv',index=False)

        

    #     # df = pd.read_csv('2016.csv')
    #     df = new_data
    dar = ['Temeke','Ilala','Kinondoni']
    mask = new_data['Police Region'].isin(['Temeke','Ilala','Kinondoni'])

    # for i in mask:
    #     if i == True:
    #         print(i)
    columns = new_data.columns[1:]

    new_data[columns]  = new_data[columns].apply(pd.to_numeric,errors="coerce")
    
    new_d = new_data[mask].sum().to_frame().T
    
    new_d['Police Region'] = 'Dar-es-salaam'
    #print(new_d) 
    df = pd.concat([new_data[-mask], new_d], ignore_index=True)

    #print(df.head())
    data = df.rename(columns={'Police Region':'STATE_UT','Total':'TOTAL_IPC_CRIMES'})
    # print(data.head()) 
    
    data.columns = data.columns.str.upper()
    print(data.columns)
    data['STATE_UT'] = data['STATE_UT'].str.upper()
    data = data.rename(columns={'CHILD DESERTION': 'CHILD_DESERTION','UNNATURAL OFFENCE':'UNNATURAL_OFFENCE'})
    data = data.sort_values('STATE_UT')
    data.insert(loc=data.columns.get_loc('STATE_UT')+1,column='DISTRICT', value='TOTAL')
    data.insert(loc=data.columns.get_loc('STATE_UT')+2,column='YEAR', value=year)
    data = data.reset_index(drop=True).dropna()
    data.columns = data.columns

    regions = [    'Arusha',    'Dar-es-Salaam',    'Dodoma',    'Geita',    'Iringa',    'Kagera',    'Katavi',    'Kigoma',    'Kilimanjaro',    'Lindi',    'Manyara',    'Mara',    'Mbeya',    'Morogoro',    'Mtwara',    'Mwanza',    'Njombe',    'Pemba North',    'Pemba South',    'Pwani',    'Rukwa',    'Ruvuma',    'Shinyanga',    'Simiyu',    'Singida',    'Songwe',    'Tabora',    'Tanga',    'Unguja North',    'Unguja South',    'Zanzibar Central/South']
    regions = [ s.upper() for s in regions]

    data = data[data['STATE_UT'].isin(regions)]


    # print(data.head())
        
    
    data.to_excel('static/assets/datasets/'+str(year)+'.xlsx',index=False)
    
    dataz = data.to_dict(orient='records')
    
    return dataz



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
     current_year = datetime.datetime.now().year
     return render_template('data.html',uss=uss,location=location,type=type,current_year=current_year)
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
     type = CrimeType.query.all()
     location = Location.query.all()
     pred = PredictData.query.filter_by(user=session['id'])
     return render_template('crime-predictor.html',uss=uss,type=type,location=location,pred=pred)
    return redirect(url_for('login'))

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if 'loggedin' in session:
     uss = session['is_admin']
     
     if request.method == 'POST':
      
      f = request.files['file']
      
      year = request.form['year']
    #   year=2015
      
      folder = 'static/assets/datasets'
      
      path = f'{folder}/{f.filename}'
 
      if os.path.isfile(os.path.join(folder,f.filename)):
          flash('file exists')
          return redirect(url_for('data'))
      else:
        col = ['STATE_UT','DISTRICT','YEAR','MURDER','RAPE','CHILD_DESERTION','UNNATURAL_OFFENCE','DEFILEMENT','TOTAL_IPC_CRIMES']
        
        if f.filename.endswith('.xlsx'):
     
        #  df = ps.read_excel(f)
        
        #  df.insert(loc=df.columns.get_loc('STATE_UT')+1,column='DISTRICT', value='TOTAL')
        #  df.insert(loc=df.columns.get_loc('STATE_UT')+2,column='YEAR', value=f.filename[-9:-5])
        #  print(df)
        #  df = df.rename(columns={'CHILD DESERTION': 'CHILD_DESERTION','UNNATURAL OFFENCE':'UNNATURAL_OFFENCE'})
        #  df = df.sort_values('STATE_UT')
        #  df = df.reset_index(drop=True).dropna()


         dir_path= 'static/assets/datasets/'
         
           
        #  if list(df.columns)!=col:
        #     flash('upload file with same data columns name')
        #     return redirect(url_for('data'))
        #  else:
        #    # print(len(col))
        #     year=df['YEAR'][0]
        #     datas = df.to_dict(orient='records')
            
            #print(year)
         j = f'static/assets/files/{year}.json'
         if len(os.listdir('static/assets/datasets')) == 0:
                 datas = preprocessings(f,year)
                #  df.to_excel('static/assets/datasets/'+f.filename,index=False)
                 csv_files = [file for file in os.listdir('static/assets/datasets') if file.endswith('.xlsx')]
                 dfs = []

# Loop through each CSV file and read it into a dataframe
                 for file in csv_files:
                    df = pd.read_excel(os.path.join(dir_path, file))
                    dfs.append(df)

                # Concatenate all dataframes into a single dataframe
                 merged_df = pd.concat(dfs, ignore_index=True)
                 
                 merged_df.to_excel('static/assets/fulldata/fulldata.xlsx')
                 dataz = merged_df.to_dict(orient='records')
                 datas = preprocessings(f,year)
                 #print(merged_df)
                 with open(j, 'w') as g:
                    json.dump(datas,g)
                 with open('static/assets/fulldata/fulldata.json', 'w') as g:
                    json.dump(dataz,g)
                
         else:
                 preprocessings(f,year)
                 csv_files = [file for file in os.listdir('static/assets/datasets') if file.endswith('.xlsx')]
                 dfs = []

# Loop through each CSV file and read it into a dataframe
                 for file in csv_files:
                    df = pd.read_excel(os.path.join(dir_path, file))
                    dfs.append(df)

                # Concatenate all dataframes into a single dataframe
                 merged_df = pd.concat(dfs, ignore_index=True)
                 
                 merged_df.to_excel('static/assets/fulldata/fulldata.xlsx')
                 dataz = merged_df.to_dict(orient='records')
                 datas = preprocessings(f,year)
                 #print(merged_df)
                 with open(j, 'w') as g:
                    json.dump(datas,g)
                 with open('static/assets/fulldata/fulldata.json', 'w') as g:
                    json.dump(dataz,g)
         data = CrimeData(year=year,user=session['id'],filename=j)
         d = CrimeData.query.filter_by(year=year).first()
         if d:
                flash('File of that year exists')
                return redirect(url_for('data'))
         else:
                with app.app_context():
                    db.session.add(data)
                    db.session.commit()
                
                 
                flash('file uploaded successfully')
                return redirect(url_for('data'))
        else:
           flash('Excel files only required') 
           return redirect(url_for('data'))
      #return 'file uploaded successfully'
    #   predictfun()
     
    return redirect(url_for('login'))


@app.route('/uploads', methods = ['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
      f = request.files['file']
      f.save(f.filename)
      #return 'file uploaded successfully'
      #predictfun()
    return render_template('crime-predictor.html')   

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
        data = CrimeData.query.order_by(CrimeData.year.desc()).first()
        current_year = datetime.datetime.now().year
        if request.method=='POST':
            webscrappingfun()
        return render_template('index.html',uss=uss,type=type,location=location,data=data,current_year=current_year)
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
                session['id'] = users.id
                
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
   flash('logout successful')
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


@app.route('/delete_user/<int:user_id>', methods=['POST','GET'])
def delete_user(user_id):
    if 'loggedin' in session:  
        if request.method == 'POST':
         user = User.query.filter_by(id=user_id).first()
         if user:
                db.session.delete(user)
                db.session.commit()
                
                flash('user deleted successful')
                return redirect('/user')
    else:
        return redirect('/login')


@app.route('/update_user/<int:user_id>/', methods=['POST','GET'])
def update_user(user_id):
  if 'loggedin' in session:  
    if request.method == 'POST':
            user = User.query.filter_by(id=user_id).first()
            user.username = request.form['email']
            # user.email = request.form['email']
            user.fullname = request.form['name']
            user.phoneNumber = request.form['number']
            user.location_id = request.form['location']
            with app.app_context():
                        
                        db.session.commit()
            flash('user edicted successful')
            return redirect('/user')
    else:
        location = Location.query.all()
        user = User.query.filter_by(id=user_id).first()
        
        return render_template('edituser.html',location=location,user=user)
  return redirect(url_for('login')) 


@app.route('/user', methods=['GET'])
def user():
    if 'loggedin' in session:
     user= User.query.join(Location).all()
     return render_template('user.html',user=user)
    else:
        return redirect(url_for('login'))
    

@app.route('/predict', methods=['POST','GET'])
def prediction():
#   try:  
    if request.method == 'POST':
        type = request.form['type']
        from_year = request.form['from']
        loc = request.form['location']
        if '-'in from_year:
            y1,y2 = from_year.split("-")
            
            d = PredictData.query.filter_by(user=session['id']).first()
            if d:
                db.session.delete(d)
                db.session.commit()
            
            pred = predict_range(loc,int(y1),int(y2),type)
            p = PredictData(image=pred,user=session['id'])
            with app.app_context():
                db.session.add(p)
                db.session.commit()
            redirect('crime-predictor.html')
        
        else:
            
            d = PredictData.query.filter_by(user=session['id']).first()
            print(d)
            if d:
                db.session.delete(d)
                db.session.commit()
            
            pred = predict(loc,from_year,type)
            p = PredictData(image=pred,user=session['id'])
            with app.app_context():
                db.session.add(p)
                db.session.commit()
            redirect('crime-predictor.html')
        
            
        return redirect('crime-predictor.html')
#   except:
#      flash('user edicted successful')
#      return redirect('crime-predictor.html')