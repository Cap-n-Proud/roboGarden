"""Flask configuration."""
# from os import environ, path
# from dotenv import load_dotenv
#
# basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, '.env'))
# We are creating a class called Config. This class stores all of the configuration settings for the Flask application. This includes the static folder, templates folder, assets folder, and the Flask application file. We then define a class called Hardware to store the settings related to hardware. This includes the serial port, baud rate, and other settings. We then define a class called JSON_Path to store the paths for the JSON files used by the application. This includes the current program, programs, plant database, and status files. Finally, we define two more classes: ProdConfig and DevConfig. These classes are used to specify the configuration settings for the production and development environments. They are similar to the Config class, but they include additional settings such as the Flask environment, debug mode, and testing mode.

import random
import string


class Config:
    VERSION = "2.0"
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
    DEBUGTAG = "D"
    LOGFORMAT = "%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s"
    CHECKHARVESTINTERVAL = 86400
    TIMEZONE = "Europe/Zurich"
    LOGIN_DISABLED = "True"
    LOGIN = "False"

    # SECRET_KEY = environ.get("SECRET_KEY")

    SECRET_KEY = "".join(
        [
            random.SystemRandom().choice(
                "{}{}{}".format(string.ascii_letters,
                                string.digits, string.punctuation)
            )
            for i in range(100)
        ]
    )
    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Hardware:
    VERSION = "2.0"
    READSERIALINTERVAL = 2
    CHECKLIGHTSINTERVAL = 5
    SERIALPORT = "/dev/ttyACM0"
    SERIALBAUD = 115200
    KEEP_WIFI_ALIVE = True
    HOST_TO_PING = "192.168.1.1"
    NUMBER_OF_PACKETS = 1
    PING_EVERY = 60


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
