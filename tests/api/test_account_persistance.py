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
    server = ServerThread(flask_app, 5004) # inny port jakis kolejny
    server.start()
    time.sleep(1)
    yield
    server.shutdown()

def test_save_and_load_accounts(server):
    base_url = "http://127.0.0.1:5004/api/accounts"
    
    pesel = "99112233445"
    payload = {"name": "Test", "surname": "Persistance", "pesel": pesel}
    requests.post(base_url, json=payload)
    
    save_resp = requests.post(f"{base_url}/save")
    assert save_resp.status_code == 200
    
    requests.post(base_url, json={"name": "Ghost", "surname": "Account", "pesel": "00000000000"})
    
    load_resp = requests.post(f"{base_url}/load")
    assert load_resp.status_code == 200

    acc_resp = requests.get(f"{base_url}/{pesel}")
    assert acc_resp.status_code == 200
    assert acc_resp.json()["name"] == "Test"
    
    ghost_resp = requests.get(f"{base_url}/00000000000")
    assert ghost_resp.status_code == 404