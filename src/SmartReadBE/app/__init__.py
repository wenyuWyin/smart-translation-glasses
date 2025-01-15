import os
from flask import Flask
from threading import Thread
from datetime import timedelta
from dotenv import load_dotenv

from .Config import monitor_heartbeats, run_task_manager, initialize_managers
from .WebSocketHandler import socketio

load_dotenv()

# Suppress logging warnings
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"





def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")

    # Configure session cookie settings
    app.config["SESSION_COOKIE_SECURE"] = True  # Ensure cookies are sent over HTTPS
    app.config["SESSION_COOKIE_HTTPONLY"] = True  # Prevent JavaScript access to cookies
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(
        days=1
    )  # Adjust session expiration as needed
    app.config["SESSION_REFRESH_EACH_REQUEST"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # Can be 'Strict', 'Lax', or 'None'

    # Register Blueprints
    from .routes.upload import upload_bp
    from .routes.signup import signup_bp
    from .routes.home import home_bp
    from .routes.langPref import lang_pref_bp

    app.register_blueprint(upload_bp)
    app.register_blueprint(signup_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(lang_pref_bp)

    # Initialize socket IO
    socketio.init_app(app)

    initialize_managers()

    # Monitor heartbeat signals of each device on a separate thread
    Thread(target=monitor_heartbeats, daemon=True).start()
    Thread(target=run_task_manager, daemon=True).start()

    return app
