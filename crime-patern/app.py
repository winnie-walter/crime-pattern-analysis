1# Flask Setup
import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db
#from flask_ngrok import run_with_ngrok
app = Flask(__name__)
app.secret_key = 'cairocoders-ednalan'
app.config.from_pyfile('config.py')
#app = Flask(__name__, static_url_path='')

db.init_app(app)
Migrate(app, db)
with app.app_context():
	db.create_all()
# Google Sheets API Setup
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
#run_with_ngrok(app)   

print("test")

# Connects our google sheet to app
# credential = ServiceAccountCredentials.from_json_keyfile_name("CrimeAnalysis-a804da08d954.json",["https://spreadsheets.google.com/feeds",                             "https://www.googleapis.com/auth/spreadsheets",                                                        "https://www.googleapis.com/auth/drive.file",                                                        "https://www.googleapis.com/auth/drive"])
# client = gspread.authorize(credential)
# gsheet = client.open("crime data project").sheet1

# importing routes
from routes import *
# runs app
if __name__ == "__main__":
    #app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 80))
    app.run(debug=True)
    #app.run()
