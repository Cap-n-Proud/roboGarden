"""Initialize Flask app."""
from flask import Flask
from flask_assets import Environment
from flask_socketio import SocketIO
import config
import logging

from flask.logging import default_handler

# https://stackoverflow.com/questions/11232230/logging-to-two-files-with-different-settings#11233293
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")


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


def create_app():
    roboG = setup_logger(config.Config.APPLOGNAME, config.Config.APPLOGFILE)
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)

    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object("config.Config")
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

        from blueprints.init import initialize

        initialize()

        app.register_blueprint(status.status_bp)
        app.register_blueprint(control.control_bp)
        app.register_blueprint(cmd.cmd_bp)
        app.register_blueprint(telemetry.telemetry_bp)
        app.register_blueprint(currentProgram.currentProgram_bp)
        app.register_blueprint(maintenance.maintenance_bp)
        app.register_blueprint(logtail.logtail_bp)

        # Compile static assets
        # compile_static_assets(assets)  # Execute logic

        return app
