import pytest
import requests
import time
import threading
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
    
    # kolejny port
    server = ServerThread(flask_app, 5003)
    server.start()
    time.sleep(1)
    yield
    server.shutdown()

def test_perf_create_delete_account(server):
    base_url = "http://127.0.0.1:5003/api/accounts"
    
    start_time = time.time()
    
    for i in range(100):
        pesel = f"900101{i:05d}" 
        payload = {"name": "Perf", "surname": "Test", "pesel": pesel}
        resp_create = requests.post(base_url, json=payload)
        assert resp_create.status_code == 201
        resp_delete = requests.delete(f"{base_url}/{pesel}")
        assert resp_delete.status_code == 200
        
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\nTime taken for 100 create+delete: {duration}s")
    # pdf mowi ze 0.5s na request ale my robimy wiecej wiec dam 2 zobaczymy
    assert duration < 2

def test_perf_100_transfers(server):
    base_url = "http://127.0.0.1:5003/api/accounts"
    pesel = "55555555555"
    
    requests.post(base_url, json={"name": "Transfer", "surname": "Perf", "pesel": pesel})

    transfer_url = f"{base_url}/{pesel}/transfer"
    start_time = time.time()
    
    for _ in range(100):
        resp = requests.post(transfer_url, json={"amount": 10, "type": "incoming"})
        assert resp.status_code == 200
        
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\nTime taken for 100 transfers: {duration}s")
    
    acc_resp = requests.get(f"{base_url}/{pesel}")
    assert acc_resp.json()["balance"] == 1000
    
    assert duration < 2.0