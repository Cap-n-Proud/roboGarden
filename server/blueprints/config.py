"""Flask configuration."""
# from os import environ, path
# from dotenv import load_dotenv


class Config:
    # SECRET_KEY = "GDtfDCFYjD"
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
    # SECRET_KEY = environ.get("SECRET_KEY")
    import random, string

    SECRET_KEY = "".join(
        [
            random.SystemRandom().choice(
                "{}{}{}".format(string.ascii_letters, string.digits, string.punctuation)
            )
            for i in range(100)
        ]
    )
    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Hardware:
    READSERIALINTERVAL = 5
    CHECKLIGHTSINTERVAL = 10
    SERIALPORT = "/dev/ttyACM0"
    SERIALBAUD = 115200


class JSON_Path:
    MSCHEDULE = "assets/maintSchedule.json"
    JSON_BASE_PATH = "assets"
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
