"""Initialize Flask app."""
from flask import Flask
from flask_assets import Environment
import config
import logging
# Globally accessible libraries
# plantsDB = getPLantsDB()
# status = getStatus()
# currentProgram = getCurrentProgram()
# programs = getPrograms()
#  SOCKETS https://gist.github.com/astrolox/445e84068d12ed9fa28f277241edf57b
# DOES NOT WORK
def configure_logging():
    # register root logging
    logging.basicConfig(
        filename=config.Config.LOGFILE,
        level=logging.DEBUG,

        format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
    )

def create_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object("config.Config")
    # Using a production configuration
    app.config.from_object("config.ProdConfig")
    assets = Environment()  # Create an assets environment
    assets.init_app(app)  # Initialize Flask-Assets
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
        from blueprints.init import init
        init()
        # configure_logging()
        # Register Blueprints
        app.register_blueprint(status.status_bp)
        app.register_blueprint(control.control_bp)
        app.register_blueprint(cmd.cmd_bp)

        # Compile static assets
        # compile_static_assets(assets)  # Execute logic

        return app
