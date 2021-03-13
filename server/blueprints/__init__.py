"""Initialize Flask app."""
from flask import Flask
from flask_assets import Environment
from flask_socketio import SocketIO
import config
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# from flask.logging import default_handler

# https://stackoverflow.com/questions/11232230/logging-to-two-files-with-different-settings#11233293
# formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
login_manager = LoginManager()


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    file_handler = logging.FileHandler(log_file)
    stream_handler = logging.StreamHandler()
    stream_formatter = logging.Formatter("%(asctime)-15s %(levelname)-8s %(message)s")
    file_formatter = logging.Formatter(
        '{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"},'
    )
    file_handler.setFormatter(file_formatter)
    # stream_handler.setFormatter(stream_formatter)
    # formatter = jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(message)s")
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    # logger.addHandler(stream_handler)

    return logger


def setupDebugLog(app):
    import sys

    logging.basicConfig(filename="logs/debug.log", level=logging.DEBUG)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(logging.ERROR)
    handler.formatter = logging.Formatter(
        fmt=u"%(asctime)s level=%(levelname)s %(message)s", datefmt="%Y-%m-%dT%H:%M:%SZ"
    )
    app.logger.addHandler(handler)


import sys


def create_app():
    roboG = setup_logger(config.Config.APPLOGNAME, config.Config.APPLOGFILE)
    # log = logging.getLogger("werkzeug")
    # log.setLevel(logging.ERROR)

    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    # setupDebugLog(app)
    # app.config.from_object("config.Config")
    import random, string

    app.config["SECRET_KEY"] = "".join(
        [
            random.SystemRandom().choice(
                "{}{}{}".format(string.ascii_letters, string.digits, string.punctuation)
            )
            for i in range(50)
        ]
    )
    # print(app.config["SECRET_KEY"])
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = "False"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

    del app.logger.handlers[:]
    logging.basicConfig(filename="logs/debug.log", level=logging.ERROR)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(logging.ERROR)
    handler.formatter = logging.Formatter(
        fmt=u"%(asctime)s level=%(levelname)s %(message)s", datefmt="%Y-%m-%dT%H:%M:%SZ"
    )
    app.logger.addHandler(handler)
    # Using a production configuration
    app.config.from_object("config.ProdConfig")
    assets = Environment()  # Create an assets environment
    assets.init_app(app)  # Initialize Flask-Assets
    async_mode = None
    thread = None
    # SocketIO extension
    socketio = SocketIO()
    socketio.init_app(app)
    socketio = SocketIO(app, async_mode=async_mode)

    # https://gist.github.com/lotusirous/9d5c942c154077f845b4b03413d48751
    with app.app_context():
        # Import parts of our application
        # from .assets import compile_static_assets
        from .cmd import cmd
        from .control import control
        from .status import status
        from .telemetry import telemetry
        from .maintenance import maintenance
        from .currentProgram import currentProgram
        from .logtail import logtail
        from .auth import auth

        from blueprints.init import initialize

        initialize()
        # Create Database Models
        # db.create_all()

        app.register_blueprint(status.status_bp)
        app.register_blueprint(control.control_bp)
        app.register_blueprint(cmd.cmd_bp)
        app.register_blueprint(telemetry.telemetry_bp)
        app.register_blueprint(currentProgram.currentProgram_bp)
        app.register_blueprint(maintenance.maintenance_bp)
        app.register_blueprint(logtail.logtail_bp)
        app.register_blueprint(auth.auth_bp)

        db.init_app(app)

        login_manager.login_view = "auth_bp.login"
        login_manager.init_app(app)
        from blueprints.auth.models import User

        @login_manager.user_loader
        def load_user(user_id):
            # since the user_id is just the primary key of our user table, use it in the query for the user
            return User.query.get(int(user_id))

        # app.register_blueprint(main_blueprint)  # Compile static assets
        # # compile_static_assets(assets)  # Execute logic

        return app
