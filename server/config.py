"""Flask configuration."""
# from os import environ, path
# from dotenv import load_dotenv
#
# basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, '.env'))
import random, string


class Config:
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    ASSETS_FOLDER = "assets"
    FLASK_APP = "wsgi.py"
    APPLOGFILE = "logs/app.log"
    APPLOGNAME = "roboLog"
    WERKZEUGLOGFILE = "logs/werkzeug.log"
    DEBUGLOGFILE = "logs/debug.log"
    INFOTAG = "I"
    TELEMETRYTAG = "T"
    LOGFORMAT = "%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s"
    CHECKHARVESTINTERVAL = 86400
    TIMEZONE = "Europe/Zurich"
    LOGIN_DISABLED = True

    # SECRET_KEY = environ.get("SECRET_KEY")

    SECRET_KEY = "".join(
        [
            random.SystemRandom().choice(
                "{}{}{}".format(string.ascii_letters, string.digits, string.punctuation)
            )
            for i in range(100)
        ]
    )
    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Hardware:
    READSERIALINTERVAL = 2
    CHECKLIGHTSINTERVAL = 5
    SERIALPORT = "/dev/ttyACM0"
    SERIALBAUD = 115200


class JSON_Path:
    JSON_PATH = "assets"
    CURRENTPROGRAM = "assets/currentProgram.json"
    PROGRAMS = "assets/programs.json"
    PLANTDB = "assets/plants.json"
    STATUS = "assets/status.json"


class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False
    # DATABASE_URI = environ.get('PROD_DATABASE_URI')


class DevConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    # DATABASE_URI = environ.get('DEV_DATABASE_URI')
