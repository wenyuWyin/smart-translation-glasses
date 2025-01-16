from flask import Blueprint, request, jsonify
from firebase_admin import storage
from ..Config import db
import base64

history_bp = Blueprint("history", __name__)


def fetch_history(uid):
    try:
        user_doc = db.collection("users").document(uid).get()
        if not user_doc.exists:
            return jsonify({"error": "User not found"}), 404

        user_data = user_doc.to_dict()
        history = user_data.get("history", {})

        history_with_image = []
        for image_id, result in history.items():
            last_updated, image = fetch_image(uid, image_id)
            if last_updated and image:
                history_with_image.append({
                    "translate_time": last_updated,
                    "image": image,
                    "result": result
                })
            else:
                raise Exception("Cannot fetch image.")

        return history_with_image
    except Exception as e:
        raise Exception(f"Error fetching translation history: {e}")


def fetch_image(uid, image_id):
    try:
        bucket = storage.bucket()
        blob = bucket.blob(f"{uid}/{image_id}.jpg")
        image_bytes = blob.download_as_bytes()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        blob.reload()
        last_updated = blob.updated

        # Format the datetime object
        formatted_date = last_updated.strftime("%Y-%m-%d-%H-%M")

        return formatted_date, image_base64
    except Exception as e:
        print(f"Error fetching image: {e}")
        return None


@history_bp.route("/history", methods=["GET"])
def save_language_preference():
    uid = request.args.get("uid")
    if not uid:
        return jsonify({"error": "UID is required"}), 400

    try:
        user_history = fetch_history(uid)

        return jsonify({"data": user_history}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
