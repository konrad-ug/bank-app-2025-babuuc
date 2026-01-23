import requests
import pytest
import threading
import time
from werkzeug.serving import make_server
from src.account_registry import AccountRegistry
from app.api import app as flask_app
import app.api

class ServerThread(threading.Thread):
    def __init__(self, app, port):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

@pytest.fixture(scope="module")
def server():
    app.api.registry = AccountRegistry()
    server = ServerThread(flask_app, 5001)
    server.start()
    time.sleep(1)
    yield
    server.shutdown()

def test_create_duplicate_account(server):
    base_url = "http://127.0.0.1:5001/api/accounts"
    payload = {"name": "Test", "surname": "Unique", "pesel": "99999999999"}
    
    response = requests.post(base_url, json=payload)
    assert response.status_code == 201

    response = requests.post(base_url, json=payload)
    assert response.status_code == 409
    assert response.json()["message"] == "Account with this pesel already exists"