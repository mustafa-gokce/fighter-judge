import os
import sys
import logging
import datetime
import random
import string
import flask
import flask_login
import flask_restful
import flask_sqlalchemy
import response
import parsers

from judge import *

# logger settings
file_name = "fighter-judge"
log_name = "fighter-judge"
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# create log file path
full_path = file_name + ".log"

# basic configs for logger
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format=log_format)

# create logger and set level
logger = logging.getLogger(log_name)
logger.setLevel(logging.DEBUG)

# try to remove the previous manager command log if exist
try:
    os.remove(full_path)
except Exception as e:
    pass

# create a file handler
handler = logging.FileHandler(full_path)
handler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)

# add the file handler to the logger
logger.addHandler(handler)

# configure server
app = flask.Flask(__name__)
app.secret_key = "".join(random.sample(string.ascii_letters + string.digits, 40))
api = flask_restful.Api(app)
db = flask_sqlalchemy.SQLAlchemy(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# get response object
response = response.Response()

# active users list
active_users = []

class User(flask_login.UserMixin, db.Model):
    """
        Database user model
    """

    # generate database user model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    """
        Keep track user session
    """

    # get user id
    user_id = int(user_id)

    # get user
    return User.query.get(user_id)


def get_server_time():
    # get server time
    server_time = datetime.datetime.now()

    return {"saat": server_time.hour,
            "dakika": server_time.minute,
            "saniye": server_time.second,
            "milisaniye": round(server_time.microsecond / 1000)}


class Login(flask_restful.Resource):
    """
        Login endpoint
        Allowed request types: POST
        Login required: false
        Description: Login to server, for permission to logging in, user should be registered in database
    """

    def post(self):
        """
        Content-type : application/json
        Required fields: kadi (str), sifre (str)
        """

        # get arguments
        args = parsers.login_parser.parse_args()

        # get user
        user = User.query.filter_by(username=args["kadi"], password=args["sifre"]).first()

        # requested individual must be anonymous to be logged in
        if flask_login.current_user.is_anonymous:

            # check if user is valid
            if user is not None:

                # give permissions to user to be logged in
                flask_login.login_user(user)
                active_users.append(user)

                # register user to judge
                Judge.register_user(user, get_server_time())

                # write logs that user has logged in
                logger.debug(user.username + " successfully logged into judge server")

                # generate response
                login_post_response_content = {"result": "success"}
                login_post_response_code = 200

            # user is not valid
            else:

                # write logs that user failed to log in
                logger.debug(args["kadi"] + " failed to log into judge server")

                # generate response
                login_post_response_content = {"result": "failure"}
                login_post_response_code = 400

        # user already logged in
        else:

            # write logs that user has logged in before
            logger.debug(user.username + " logged in before")

            # generate response
            login_post_response_content = {"result": "unnecessary"}
            login_post_response_code = 400

        # return to response
        return login_post_response_content, login_post_response_code


class GetServerTime(flask_restful.Resource):
    """
        Server time endpoint
        Allowed request types: GET
        Login required: true
        Description: Get server time in hour, minute, second, milliseconds
    """

    @flask_login.login_required
    def get(self):
        """
            Content-type : application/json
            Required fields: none
        """

        # generate response
        time_get_response_content = get_server_time()
        time_get_response_code = 200

        # log the request
        logger.debug(str(time_get_response_content))

        # return to response
        return time_get_response_content, time_get_response_code


class PostTelemetry(flask_restful.Resource):
    """
        Telemetry data endpoint
        Allowed request types: POST
        Login required: true
        Description: Get foe and send team telemetry data
    """

    @flask_login.login_required
    def post(self):
        """
            Content-type : application/json
            Required fields: dict
        """

        # get arguments from team
        args = parsers.telemetry_parser.parse_args()

        # save telemetry data of the team
        response.set_args(args)

        # save telemetry data for judge
        Judge.register_telem_data(args)

        # telemetry data is not empty
        if args is not None:

            # log the telemetry data
            logger.debug(str(args))

            # generate response
            telemetry_post_response_content = response.get_data()
            telemetry_post_response_code = 200

        # telemetry data is empty
        else:

            # log the error
            logger.debug("incomplete telemetry data from team")

            # generate response
            telemetry_post_response_content = {"result": "failure"}
            telemetry_post_response_code = 400

        # return to response content and code
        return telemetry_post_response_content, telemetry_post_response_code


class PostLockOn(flask_restful.Resource):
    """
        Target lock data endpoint
        Allowed request types: POST
        Login required: true
        Description: Send target lock data to judge
    """

    @flask_login.login_required
    def post(self):
        """
            Content-type : application/json
            Required fields: dict
        """

        # get target lock data from team
        args = parsers.lock_on_parser.parse_args()

        # target lock data is not empty
        if args is not None:

            # log the target lock data
            logger.debug(str(args))

            # generate response
            target_post_response_content = {"result": "success"}
            target_post_response_code = 200

        # target lock data is empty
        else:

            # log the error
            logger.debug("incomplete target lock data from team")

            # generate response
            target_post_response_content = {"result": "failure"}
            target_post_response_code = 400

        # return to response content and code
        return target_post_response_content, target_post_response_code


class GetScoreTable(flask_restful.Resource):
    """
        Get score table endpoint
        Allowed request types: GET
        Login required: false
        Description: Get current scores of teams
    """

    def get(self):
        scores = Judge.get_scores()
        logger.debug(str(scores))
        return scores, 200


class GetDelayTable(flask_restful.Resource):
    """
        Get delay table endpoint
        Allowed request types: GET
        Login required: false
        Description: Get current delay of teams
    """

    def get(self):
        delays = Judge.get_delays()
        logger.debug(str(delays))
        return delays, 200


class GetActiveUsers(flask_restful.Resource):
    """
        Get active users endpoint
        Allowed request types: GET
        Login required: false
        Description: Get current delay of teams
    """

    def get(self):
        active_users_dict = {user.id: user.username for user in active_users}

        # log the action
        logger.debug(str(active_users_dict) + " successfully logged out from judge server")

        return active_users_dict, 200


class Logout(flask_restful.Resource):
    """
        Logout endpoint
        Allowed request types: GET
        Login required: true
        Description: Logout from server, user must be logged in
    """

    @flask_login.login_required
    def get(self):
        """
            Content-type : application/json
            Required fields: none
        """

        # get usr name
        user_name = flask_login.current_user.username

        # judge remove user
        Judge.remove_user(flask_login.current_user)

        # kick user from the server
        flask_login.logout_user()

        # log the action
        logger.debug(user_name + " successfully logged out from judge server")

        # generate response
        logout_get_response_content = {"result": "success"}
        logout_get_response_code = 200

        # return to response
        return logout_get_response_content, logout_get_response_code


@app.before_first_request
def create_tables():
    """
        Create users before first request
    """

    # create database and users
    db.create_all()
    records = [User(id=26, username="TestUcusu", password="ZurnaGonnaGetYouDown"),
               User(id=10, username="DummyTeam1", password="AdimCaferBoyumBirOn"),
               User(id=41, username="DummyTeam2", password="YouHaveNoIdeaHowHighCanIFly"),
               User(id=58, username="DummyTeam3", password="PleaseLeaveMeAlone"),
               User(id=117, username="DummyTeam4", password="MyEnemiesAreAfterMe")]
    for record in records:
        db.session.add(record)
    db.session.commit()


@app.before_first_request
def server_start():
    """
        Server starting procedures and initial configurations
    """

    # log the server has started
    logger.debug("started judge server")

    # log the secret key
    logger.debug(app.secret_key + " is the judge server secret key")


# add endpoints
api.add_resource(Login, '/api/giris')
api.add_resource(GetServerTime, '/api/sunucusaati')
api.add_resource(PostTelemetry, '/api/telemetri_gonder')
api.add_resource(PostLockOn, '/api/kilitlenme_bilgisi')
api.add_resource(GetScoreTable, '/api/puan_tablosu')
api.add_resource(GetDelayTable, '/api/gecikme_tablosu')
api.add_resource(GetActiveUsers, '/api/aktif_kullanicilar')
api.add_resource(Logout, '/api/cikis')

if __name__ == "__main__":
    # start the server
    app.run("0.0.0.0", port=5000)
