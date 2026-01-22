import requests
import pytest
import threading
import time
from werkzeug.serving import make_server
from app.api import app

class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

@pytest.fixture(scope="module")
def server():
    server = ServerThread(app)
    server.start()
    time.sleep(1)
    yield
    server.shutdown()

def test_create_and_get_account(server):
    base_url = "http://127.0.0.1:5000/api/accounts"
    
    payload = {
        "name": "Test",
        "surname": "User",
        "pesel": "11111111111"
    }
    response = requests.post(base_url, json=payload)
    assert response.status_code == 201
    assert response.json() == {"message": "Account created"}

    response = requests.get(f"{base_url}/11111111111")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test"
    assert data["pesel"] == "11111111111"

    response = requests.get(f"{base_url}/count")
    assert response.status_code == 200
    assert response.json()["count"] > 0