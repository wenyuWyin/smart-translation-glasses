import time
from flask import Blueprint, request, jsonify
from app.Config import device_heartbeats
from app.WebSocketHandler import send_status_update
from app.Task import Task
from app.Config import task_manager, extraction_manager, translation_manager
from .langPref import fetch_language_preference
import os
import cv2
import numpy as np

UPLOAD_FOLDER = "TEMP"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

upload_bp = Blueprint("upload", __name__)

HEARTBEAT_TIMEOUT = 8


# Handler for receiving an captured image
@upload_bp.route("/upload/image", methods=["POST"])
def upload_image():
    if "file" not in request.files and not request.data:
        return "No file part", 400

    try:
        account_number = request.headers.get("Account-Number")

        image_data = request.data
        filename = os.path.join(UPLOAD_FOLDER, "image.jpg")
        with open(filename, "wb") as f:
            f.write(image_data)
        print(f"Image is saved to {filename} for {account_number}")

        # image = cv2.imread(filename)
        nparr = np.frombuffer(image_data, np.uint8)
        # Decode the numpy array into an OpenCV image
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        user_data = fetch_language_preference(account_number)
        source_lang = user_data["source-lang"]
        target_lang = user_data["target-lang"]

        task = Task(
            account_number,
            len(task_manager.task_queue) + 1,
            extraction_manager,
            image,
            translation_manager,
            target_lang,
            source_lang,
        )
        task.initialize()

        task_manager.add_task(task)

        return "Image received", 200
    except Exception as e:
        print(f"Error saving image: {e}")
        return "Failed to save image", 500


# Handler for receiving device status
@upload_bp.route("/upload/status", methods=["POST"])
def upload_status():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        user_id = data.get("account")
        battery = data.get("battery")
        temperature = data.get("temperature")
        connection_status = data.get("wifiStatus")

        # Send device status to front-end through WebSocket
        send_status_update(user_id, battery, temperature, connection_status)
        return "Status updated", 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to process  request"}), 400


# Handler for receiving heartbeat messages
@upload_bp.route("/upload/heartbeat", methods=["POST"])
def upload_heartbeat():
    try:
        data = request.get_json()
        user_id = data.get("account")

        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        # Update last active from for the corresponding device
        device_heartbeats[user_id] = time.time()
        print(f"Heartbeat received from device {user_id}")

        return jsonify({"message": "Heartbeat received"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to process heartbeat"}), 500
