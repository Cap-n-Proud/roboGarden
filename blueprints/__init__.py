"""Initialize Flask app."""
from flask import Flask
from flask_assets import Environment
import config
# Globally accessible libraries
# plantsDB = getPLantsDB()
# status = getStatus()
# currentProgram = getCurrentProgram()
# programs = getPrograms()


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
    
    with app.app_context():
        # Import parts of ou    r application
        # from .assets import compile_static_assets
        from .cmd import cmd
        from .control import control
        from .status import status
        from blueprints.threads import init
        init()
        # Register Blueprints
        app.register_blueprint(status.status_bp)
        app.register_blueprint(control.control_bp)
        app.register_blueprint(cmd.cmd_bp)

        # Compile static assets
        # compile_static_assets(assets)  # Execute logic

        return app
