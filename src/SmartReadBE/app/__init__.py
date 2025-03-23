import os
from flask import Flask
from threading import Thread
from datetime import timedelta
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

from .Config import monitor_heartbeats, initialize_managers
from .WebSocketHandler import socketio

load_dotenv()

# Suppress logging warnings
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"


def create_app(heartbeat_thread=True):
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
    from .routes.history import history_bp

    app.register_blueprint(upload_bp)
    app.register_blueprint(signup_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(lang_pref_bp)
    app.register_blueprint(history_bp)

    # Initialize socket IO
    socketio.init_app(app)

    # Initialize the ThreadPoolExecutor
    app.executor = ThreadPoolExecutor(max_workers=4)

    initialize_managers()

    # Shutdown the executor when the app stops
    @app.teardown_appcontext
    def shutdown_executor(exception=None):
        if hasattr(app, "executor"):
            app.executor.shutdown(wait=True)

    if heartbeat_thread:
        # Monitor heartbeat signals of each device on a separate thread
        Thread(target=monitor_heartbeats, daemon=True).start()
        
    return app
