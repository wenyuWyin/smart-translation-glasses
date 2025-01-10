from flask import Blueprint, request, jsonify
from .. import db

lang_pref_bp = Blueprint("lang_pref", __name__)


@lang_pref_bp.route("/lang-pref", methods=["POST", "GET"])
def save_language_preference():
    if request.method == "POST":
        data = request.get_json()
        uid = data.get("uid")
        source_lang = data.get("sourceLang")
        target_lang = data.get("targetLang")
        print(f'{uid} - {source_lang} - {target_lang}')

        if not uid or not source_lang or not target_lang:
            return jsonify({"error": "Missing required fields"}), 400

        try:
            db.collection("users").document(uid).set(
                {
                    "source-lang": source_lang,
                    "target-lang": target_lang,
                },
                merge=True,
            )
            return jsonify({"message": "Language preference saved successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == "GET":
        uid = request.args.get("uid")
        if not uid:
            return jsonify({"error": "UID is required"}), 400

        try:
            user_doc = db.collection("users").document(uid).get()
            if not user_doc.exists:
                return jsonify({"error": "User not found"}), 404

            user_data = user_doc.to_dict()
            return jsonify(
                {
                    "source-lang": user_data["source-lang"],
                    "target-lang": user_data["target-lang"],
                }
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
