import os
from flask import Flask
from datetime import timedelta
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

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

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')

    # Configure session cookie settings
    app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are sent over HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Adjust session expiration as needed
    app.config['SESSION_REFRESH_EACH_REQUEST'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Can be 'Strict', 'Lax', or 'None'

    # Register Blueprints
    from .routes.upload import upload_bp
    from .routes.signup import signup_bp
    from .routes.home import home_bp
    from .routes.langPref import lang_pref_bp

    app.register_blueprint(upload_bp)
    app.register_blueprint(signup_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(lang_pref_bp)

    return app
