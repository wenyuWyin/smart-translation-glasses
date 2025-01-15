from flask import Blueprint, request
from app.Config import db

signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        uid = data.get('uid')
        username = data.get('username')

        user_data = {
            "username": username,
            "source-language": "",
            "target_language": "",
            "history": []
        }

        db.collection("users").document(uid).set(user_data)
    except Exception as e:
        print(f"Error creating document for new user: {e}")
        return "Failed to create a new document", 400

    return "New user created", 200
