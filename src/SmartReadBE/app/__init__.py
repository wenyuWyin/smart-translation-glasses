import os
import time
from flask import Flask
from threading import Thread
from datetime import timedelta
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from flask_socketio import SocketIO

load_dotenv()


# Initialize Firebase Admin
def initialize_firebase():
    try:
        cred = credentials.Certificate("firebaseAuth.json")
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Firebase connection successful!")
        return db
    except Exception as e:
        print(f"Firebase connection failed: {e}")
        return None


db = initialize_firebase()

# Initialize Flask app and SocketIO
socketio = SocketIO(cors_allowed_origins="*")
device_heartbeats = {}  # Tracks ESP32 devices and their last heartbeat time
HEARTBEAT_TIMEOUT = 10  # Timeout in seconds for detecting disconnection


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

    # Monitor heartbeat signals of each device on a separate thread
    Thread(target=monitor_heartbeats, daemon=True).start()

    return app


def monitor_heartbeats():
    from .webSocketHandler import notify_disconnection

    # Keep monitoring all active devices
    while True:
        current_time = time.time()
        inactive_devices = []

        # Devices are considered inactive if they have not sent a heartbeat message in HEARTBEAT_TIMEOUT
        for user_id, last_seen in device_heartbeats.items():
            if current_time - last_seen > HEARTBEAT_TIMEOUT:
                inactive_devices.append(user_id)

        # Notify the apps that the devices are inactive
        for user_id in inactive_devices:
            del device_heartbeats[user_id]
            print(f"User {user_id} is disconnected due to timeout")
            notify_disconnection(user_id)
