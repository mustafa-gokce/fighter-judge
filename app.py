from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_restful import Api, Resource
from datetime import datetime
import json
import os

from urllib3 import response

from config import *
from utils.parser import *
from utils.data import *
from utils.logger import *

app = Flask(__name__)
app.config.from_pyfile('config.py')

api = Api(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

response = Response()
logger = Logger()

"""
    * Database user model
    * Schema (id, username, password)
"""


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)


"""
    * Necessary function to keep track user session.
"""


@login_manager.user_loader
def load_user(user_id):
    id_pk = int(user_id)
    return User.query.get(id_pk)


"""
    * Content-type : application/json
    * kadi and sifre required fields
    * Only support POST requests.
    * To log in user should be registered to login.db
"""


class Login(Resource):
    def post(self):
        args = login_parser.parse_args()
        user = User.query.filter_by(username=args['kadi'], password=args['sifre']).first()

        if current_user.is_anonymous:
            if user is not None:
                login_user(user)
                logger.write(user.username.upper() + " logged in", type="POST", link="api/giris", status=200)
                return {"messsage": f"{args['kadi']} logged in !"}, 200

            else:
                logger.write("Username or password incorrect !", type="POST", link="api/giris", status=400)
                return {"messsage": "Username or password incorrect !"}, 400


"""
    * Get server hour,minute,second,milis
    * Login required
    * Only support GET requests
"""


class GetServerTime(Resource):
    @login_required
    def get(self):
        current = datetime.now()
        response = {"saat": current.hour,
                    "dakika": current.minute,
                    "saniye": current.second,
                    "milisaniye": round(current.microsecond / 1000)}
        logger.write("\n" + json.dumps(response, indent=4),
                     type="GET",
                     link="api/sunucusaati",
                     status=200)
        return response, 200


"""
    * Login required
    * Only support POST requests
    * It returns other teams locations info
"""


class PostTelemetry(Resource):
    @login_required
    def post(self):
        args = telemetry_parser.parse_args()
        response.setArgs(args)
        if args is not None:
            logger.write("\n" + f" * Delay: {response.get_delay()}ms\n" + json.dumps(args, indent=4),
                         type="POST",
                         link="api/telemetri_gonder",
                         status=200)
            return response.getData(), 200
        else:
            logger.write("Data is incomplete",
                         type="POST",
                         link="api/telemetri_gonder",
                         status=400)
            return {"message": "Data is incomplete"}, 400


"""
    * Login required
    * Only support POST requests
"""


class PostLockOn(Resource):
    @login_required
    def post(self):
        args = lock_on_parser.parse_args()

        if args is not None:
            logger.write("\n" + json.dumps(args, indent=4), type="POST", link="api/kilitlenme_bilgisi", status=200)
            return {"message": "Data is received"}, 200
        else:
            logger.write("Data is incomplete", type="POST", link="api/kilitlenme_bilgisi", status=400)
            return {"message": "Data is incomplete"}, 400


"""
    * Only support GET requests.
    * To log out send GET request once
"""


class Logout(Resource):
    @login_required
    def get(self):
        username = current_user.username
        logout_user()
        logger.write(f"{username} logged out!", type="GET", link="api/cikis", status=200)
        return {"messsage": f"{username} logged out!"}, 200


"""
    * Endpoints field
"""
api.add_resource(Login, '/api/giris')
api.add_resource(GetServerTime, '/api/sunucusaati')
api.add_resource(PostTelemetry, '/api/telemetri_gonder')
api.add_resource(PostLockOn, '/api/kilitlenme_bilgisi')
api.add_resource(Logout, '/api/cikis')

if __name__ == "__main__":

    if os.path.exists("./database/login.db"):
        pass
    else:
        """
            * Create database if not already exist
            * Create user table
            * Insert an entry to db who can access API
            * Default estu & "1234" can be changed config.py
            * More entry can be added
        """
        os.mkdir("./database")
        record = User(id=1, username=VALID_USERNAME, password=VALID_PASSWORD)
        db.create_all()
        db.session.add(record)
        db.session.commit()
        print(" * Database is created !")

    app.run("0.0.0.0", port=5000)
