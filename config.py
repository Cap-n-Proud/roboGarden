"""Flask configuration."""
# from os import environ, path
# from dotenv import load_dotenv
#
# basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, '.env'))


class Config:
    SECRET_KEY = "GDtfDCFYjD"
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    ASSETS_FOLDER = "assets"
    FLASK_APP = "wsgi.py"

class Hardware:
    READSERIALINTERVAL = 2
    CHECKLIGHTSINTERVAL = 5
    SERIALPORT = "/dev/ttyACM0"
    SERIALBAUD = 115200

class JSON_Path:
    JSON_PATH = "assets"
    CURRENTPROGRAM = "assets/currentProgram.json"
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
