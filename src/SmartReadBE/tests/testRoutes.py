from unittest.mock import patch


# test for signup.py
@patch("app.routes.signup.db")
def test_signup_success(mock_db, client_without_managers):
    mock_db.collection().document().get().exists = False
    mock_db.collection().document().set.return_value = None

    payload = {"uid": "test_uid", "username": "test_user"}
    response = client_without_managers.post("/signup", json=payload)

    assert response.status_code == 200
    assert response.json["message"] == "User signed up successfully"


def test_signup_missing_uid(client_without_managers):
    payload = {"uid": "", "username": "test_user"}
    response = client_without_managers.post("/signup", json=payload)

    assert response.status_code == 400
    assert response.json["error"] == "Missing user ID"


@patch("app.routes.signup.db")
def test_signup_duplicate_uid(mock_db, client_without_managers):
    mock_db.collection().document().get().exists = True

    payload = {"uid": "test_uid", "username": "test_user"}
    response = client_without_managers.post("/signup", json=payload)

    assert response.status_code == 400
    assert response.json["error"] == "User ID already exists"


# test for langPref.py
@patch("app.routes.langPref.db")
def test_save_language_preference_post_success(mock_db, client_without_managers):
    mock_db.collection().document().set.return_value = None

    payload = {"uid": "test_uid", "sourceLang": "French", "targetLang": "Chinese"}
    response = client_without_managers.post("/lang-pref", json=payload)

    assert response.status_code == 200
    assert response.json["message"] == "Language preference saved successfully"


def test_save_language_preference_post_missing_uid(client_without_managers):
    payload = {"uid": "", "sourceLang": "French", "targetLang": "Chinese"}
    response = client_without_managers.post("/lang-pref", json=payload)

    assert response.status_code == 400
    assert response.json["error"] == "Missing user ID"


@patch("app.routes.langPref.db")
def test_fetch_language_preference_get_success(mock_db, client_without_managers):
    mock_db.collection().document().get().to_dict.return_value = {
        "source-lang": "French",
        "target-lang": "Chinese",
    }
    response = client_without_managers.get("/lang-pref?uid=test_uid")

    assert response.status_code == 200
    assert response.json["source-lang"] == "French"
    assert response.json["target-lang"] == "Chinese"


def test_save_language_preference_get_missing_uid(client_without_managers):
    response = client_without_managers.get("/lang-pref")

    assert response.status_code == 400
    assert response.json["error"] == "Missing user ID"


# test for history.py
@patch("app.routes.history.db")
@patch("app.routes.history.fetch_image")
def test_fetch_history_success(mock_fetch_image, mock_db, client_without_managers):
    mock_db.collection().document().get().to_dict.return_value = {
        "history": {"image1": "result1"}
    }
    mock_fetch_image.return_value = ("2023-01-01-12-00", "base64image")

    response = client_without_managers.get("/history?uid=test_uid")

    expected_response = {
        "data": [
            {
                "image": "base64image",
                "result": "result1",
                "translate_time": "2023-01-01-12-00",
            }
        ]
    }

    assert response.status_code == 200
    assert "data" in response.json
    assert response.json == expected_response


@patch("app.routes.history.db")
def test_fetch_empty_history(mock_db, client_without_managers):
    mock_db.collection().document().get().to_dict.return_value = {"history": {}}

    response = client_without_managers.get("/history?uid=test_uid")

    expected_response = {"data": []}

    assert response.status_code == 200
    assert "data" in response.json
    assert response.json == expected_response


