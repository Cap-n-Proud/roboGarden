"""Initialize Flask app."""
from flask import Flask
from flask_assets import Environment
from flask_socketio import SocketIO
import config
import logging
from flask.logging import default_handler

# Globally accessible libraries
# plantsDB = getPLantsDB()
# status = getStatus()
# currentProgram = getCurrentProgram()
# programs = getPrograms()
#  SOCKETS https://gist.github.com/astrolox/445e84068d12ed9fa28f277241edf57b

#
# def configure_logging():
#     # app.logger.removeHandler(default_handler)
#     # register root logging
#     logging.basicConfig(
#         filename=config.Config.WERKZEUGLOGFILE,
#         log=logging.getLogger("werkzeug"),
#         level=logging.ERROR,
#         format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
#     )


formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def create_app():
    roboG = setup_logger(config.Config.APPLOGNAME, config.Config.APPLOGFILE)

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

    # init()
    # Using a development configuration
    # app.config.from_object("config.DevConfig")
    # https://gist.github.com/lotusirous/9d5c942c154077f845b4b03413d48751
    with app.app_context():
        # Import parts of our application
        # from .assets import compile_static_assets
        from .cmd import cmd
        from .control import control
        from .status import status
        from .telemetry import telemetry
        from blueprints.init import init

        init()
        configure_logging()
        # Register Blueprints
        app.register_blueprint(status.status_bp)
        app.register_blueprint(control.control_bp)
        app.register_blueprint(cmd.cmd_bp)
        app.register_blueprint(telemetry.telemetry_bp)

        # Compile static assets
        # compile_static_assets(assets)  # Execute logic

        return app
