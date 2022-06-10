

from flask import Flask
import os




db_username = os.environ['DB_USER']
db_password = os.environ['DB_PASSW']
db_address = os.environ['DB_ADDRESS']
db_name = os.environ['DB_NAME']
#autoplayback_db
app = Flask(__name__)
#Databas
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_username}:{db_password}@{db_address}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.run(host='localhost', debug=True, threaded=True, use_reloader=False)



