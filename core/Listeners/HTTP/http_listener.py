import sys
from termcolor import colored
from flask import Flask
from waitress import serve
from database.db import initialize_db
from pymongo import ReadPreference

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from core.Listeners.HTTP.database.models import Listeners
from core.Listeners.HTTP.database.models import Tasks
from core.Listeners.HTTP.database.models import Particles
import string, random
import mongoengine
from flask_bcrypt import generate_password_hash

def start_listener(apiHost, apiPort, databaseHost, databasePort, databaseName):
    app = Flask(__name__)
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)

    jwt_token = ''.join(
        random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(32))
    app.config['JWT_SECRET_KEY'] = jwt_token

    try:
        app.config['MONGODB_DB'] = databaseName
        app.config['MONGODB_HOST'] = databaseHost
        app.config['MONGODB_PORT'] = databasePort
        app.config['MONGODB_CONNECT'] = False

        initialize_db(app)

        #app.register_blueprint(task_blueprint)

        serve(app, host=apiHost, port=apiPort)
    except:
        e = sys.exc_info()
        if e == None or e == "":
            exit()
        else:
            print(colored("[*] {}".format(e), "red"))
            exit()