# import psycopg2
# import psycopg2.extras


# DB_HOST = "localhost"
# DB_NAME = "crime"
# DB_USER = "postgres"
# DB_PASS = "winnie"
 
# conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
# cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
# cursor.execute('CREATE TABLE users (id serial PRIMARY KEY,fullname VARCHAR ( 100 ) NOT NULL,username VARCHAR ( 50 ) NOT NULL,password VARCHAR ( 255 ) NOT NULL,email VARCHAR ( 50 ) NOT NULL'))

# # CREATE TABLE users (
# # 	id serial PRIMARY KEY,
# # 	fullname VARCHAR ( 100 ) NOT NULL,
# # 	username VARCHAR ( 50 ) NOT NULL,
# # 	password VARCHAR ( 255 ) NOT NULL,
# # 	email VARCHAR ( 50 ) NOT NULL
# # );