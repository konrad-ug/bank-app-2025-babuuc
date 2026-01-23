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
    
    # jeszcze inny port
    server = ServerThread(flask_app, 5002)
    server.start()
    time.sleep(1)
    yield
    server.shutdown()

def test_transfer_api(server):
    base_url = "http://127.0.0.1:5002/api/accounts"
    pesel = "88888888888"
    
    requests.post(base_url, json={"name": "Kasa", "surname": "Test", "pesel": pesel})
    
    transfer_url = f"{base_url}/{pesel}/transfer"
    response = requests.post(transfer_url, json={"amount": 100, "type": "incoming"})
    assert response.status_code == 200
    assert response.json()["message"] == "Transfer processed"

    acc_response = requests.get(f"{base_url}/{pesel}")
    assert acc_response.json()["balance"] == 100

    response = requests.post(transfer_url, json={"amount": 50, "type": "outgoing"})
    assert response.status_code == 200

    acc_response = requests.get(f"{base_url}/{pesel}")
    assert acc_response.json()["balance"] == 50

def test_transfer_fail_insufficient_funds(server):
    base_url = "http://127.0.0.1:5002/api/accounts"
    pesel = "88888888888"
    
    transfer_url = f"{base_url}/{pesel}/transfer"
    response = requests.post(transfer_url, json={"amount": 1000, "type": "outgoing"})
    
    assert response.status_code == 422
    assert response.json()["message"] == "Insufficient funds"