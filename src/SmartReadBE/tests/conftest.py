import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def client_without_managers():
    app = create_app(manager_thread=False, heartbeat_thread=False)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client