import time
from firebase_admin import credentials, firestore
import firebase_admin

from TextExtractionModule.TextExtractionManager import TextExtractionManager
from TranslationModule.TranslationManager import TranslationManager

device_heartbeats = {}  # Tracks ESP32 devices and their last heartbeat time
HEARTBEAT_TIMEOUT = 10  # Timeout in seconds for detecting disconnection


extraction_manager = TextExtractionManager()
translation_manager = TranslationManager()


# Initialize Firebase Admin
def initialize_firebase():
    try:
        cred = credentials.Certificate("firebaseAuth.json")
        firebase_admin.initialize_app(
            cred, {"storageBucket": "smartread-270d2.firebasestorage.app"}
        )
        db = firestore.client()
        print("Firebase connection successful!")
        return db
    except Exception as e:
        print(f"Firebase connection failed: {e}")
        return None


db = initialize_firebase()


def initialize_managers():
    print("Initializing managers")
    extraction_manager.initialize()
    translation_manager.initialize()
    print("Managers initialized")


def monitor_heartbeats():
    from .WebSocketHandler import notify_disconnection

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
