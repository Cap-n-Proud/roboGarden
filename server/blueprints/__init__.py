import sys
import logging
from flask import Flask
from flask_assets import Environment
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import config
from threading import Lock

# Initialize SQLAlchemy and LoginManager objects
db = SQLAlchemy()
login_manager = LoginManager()

# Function to set up custom loggers with file and console handlers


def setup_logger(name, log_file, level=logging.INFO):
    # Set up file handler
    file_handler = logging.FileHandler(log_file)
    file_formatter = logging.Formatter(
        '{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"},')
    file_handler.setFormatter(file_formatter)

    # Set up console handler (commented out for now)
    # stream_handler = logging.StreamHandler()
    # stream_formatter = logging.Formatter("%(asctime)-15s %(levelname)-8s %(message)s")
    # stream_handler.setFormatter(stream_formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    # logger.addHandler(stream_handler)

    return logger

# Function to set up debug log for Flask app


def setupDebugLog(app):
    logging.basicConfig(filename="logs/debug.log", level=logging.DEBUG)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(logging.ERROR)
    handler.formatter = logging.Formatter(
        fmt=u"%(asctime)s level=%(levelname)s %(message)s", datefmt="%Y-%m-%dT%H:%M:%SZ")
    app.logger.addHandler(handler)

# Function to create the Flask app and register blueprints and extensions


def create_app():
    # Set up custom logger for the app
    roboG = setup_logger(config.Config.APPLOGNAME, config.Config.APPLOGFILE)

    # Create Flask application
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    # Set up custom debug log for app (commented out for now)
    # setupDebugLog(app)

    # Set up SQLAlchemy configurations
    app.config["SECRET_KEY"] = config.Config.SECRET_KEY
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.Config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["SQLALCHEMY_DATABASE_URI"] = config.Config.SQLALCHEMY_DATABASE_URI

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Set up custom error log for Flask app
    del app.logger.handlers[:]  # Remove default log handlers
    logging.basicConfig(filename="logs/debug.log", level=logging.ERROR)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(logging.ERROR)
    handler.formatter = logging.Formatter(
        fmt=u"%(asctime)s level=%(levelname)s %(message)s", datefmt="%Y-%m-%dT%H:%M:%SZ")
    app.logger.addHandler(handler)

    # Set up Flask-Assets environment
    assets = Environment()
    assets.init_app(app)

    # Initialize SocketIO
    socketio = SocketIO(app)

    # Import blueprints and initialize the app context
    with app.app_context():
        from .cmd import cmd
        from .control import control
        from .status import status
        from .telemetry import telemetry
        from .maintenance import maintenance
        from .currentProgram import currentProgram
        from .logtail import logtail
        from .auth import auth
        from blueprints.init import initialize

        # Initialize the system (assuming this function exists in the "initialize" blueprint)
        initialize()

        # Register blueprints with the app
        app.register_blueprint(status.status_bp)
        app.register_blueprint(control.control_bp)
        app.register_blueprint(cmd.cmd_bp)
        app.register_blueprint(telemetry.telemetry_bp)
        app.register_blueprint(currentProgram.currentProgram_bp)
        app.register_blueprint(maintenance.maintenance_bp)
        app.register_blueprint(logtail.logtail_bp)
        app.register_blueprint(auth.auth_bp)

        # Set up login manager and user_loader function
        login_manager.login_view = "auth_bp.login"
        login_manager.init_app(app)
        app.config["LOGIN_DISABLED"] = config.Config.LOGIN_DISABLED
        from blueprints.auth.models import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        return app
