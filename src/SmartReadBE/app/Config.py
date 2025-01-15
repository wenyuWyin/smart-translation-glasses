import time
from firebase_admin import credentials, firestore
import firebase_admin

from .TaskManager import TaskManager
from TextExtractionModule.TextExtractionManager import TextExtractionManager
from TranslationModule.TranslationManager import TranslationManager

device_heartbeats = {}  # Tracks ESP32 devices and their last heartbeat time
HEARTBEAT_TIMEOUT = 10  # Timeout in seconds for detecting disconnection


task_manager = TaskManager()
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
    task_manager.initialize()
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


def run_task_manager():
    task_manager.activate_queue()
    while True:
        if task_manager.task_queue:
            print(f"{len(task_manager.task_queue)} tasks left in the queue")
            task = task_manager.task_queue[0]
            if task.get_status():
                print(f"Exceuting Task {task.task_id}")
                success = task.execute_task()
                if success:
                    print(f"Task {task.task_id} executed successfully")
                    task_manager.remove_task(task.task_id)
                else:
                    print(f"Task {task.task_id} failed")
            else:
                print(f"Task {task.task_id} is not active")
