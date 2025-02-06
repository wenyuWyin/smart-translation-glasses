from flask import Blueprint, request, jsonify
from app.Config import db

signup_bp = Blueprint("signup", __name__)


@signup_bp.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()
        uid = data.get("uid")
        username = data.get("username")

        if not uid:
            return jsonify({"error": "Missing user ID"}), 400

        user_data = {
            "username": username,
            "source-lang": "",
            "target-lang": "",
            "history": {},
        }

        doc_ref = db.collection("users").document(uid)
        doc = doc_ref.get()

        if doc.exists:
            return jsonify({"error": "User ID already exists"}), 400
        else:
            doc_ref.set(user_data)

        return jsonify({"message": "User signed up successfully"}), 200
    except Exception as e:
        print(f"Error creating document for new user: {e}")
        return jsonify({"error": str(e)}), 500
