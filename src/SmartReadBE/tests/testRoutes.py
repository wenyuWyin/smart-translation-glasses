from unittest.mock import patch


# test for signup.py
def test_signup_success(client):
    payload = {"uid": "test_uid", "username": "test_user"}
    response = client.post("/signup", json=payload)

    assert response.status_code == 200
    assert response.data.decode() == "New user created"


# test for langPref.py
def test_save_language_preference_post_success(client):
    payload = {"uid": "test_uid", "sourceLang": "French", "targetLang": "Chinese"}
    response = client.post("/lang-pref", json=payload)

    assert response.status_code == 200
    assert response.json["message"] == "Language preference saved successfully"

def test_save_language_preference_post_missing_uid(client):
    payload = {"uid": "", "sourceLang": "French", "targetLang": "Chinese"}
    response = client.post("/lang-pref", json=payload)

    assert response.status_code == 400

def test_fetch_language_preference_get_success(client):
    with patch("app.routes.langPref.db") as mock_db:
        mock_db.collection().document().get().to_dict.return_value = {
            "source-lang": "French",
            "target-lang": "Chinese",
        }
        response = client.get("/lang-pref?uid=test_uid")

        assert response.status_code == 200
        assert response.json["source-lang"] == "French"
        assert response.json["target-lang"] == "Chinese"

def test_save_language_preference_get_missing_uid(client):
    response = client.get("/lang-pref")
    assert response.status_code == 400


# test for history.py
def test_fetch_history_success(client):
    with (
        patch("app.routes.history.db") as mock_db,
        patch("app.routes.history.fetch_image") as mock_fetch_image,
    ):
        mock_db.collection().document().get().to_dict.return_value = {
            "history": {"image1": "result1"}
        }
        mock_fetch_image.return_value = ("2023-01-01-12-00", "base64image")

        response = client.get("/history?uid=test_uid")

        expected_response = {
            "data": [{
                "image": "base64image",
                "result": "result1",
                "translate_time": "2023-01-01-12-00",
            }]
        }

        assert response.status_code == 200
        assert "data" in response.json
        assert response.json == expected_response
