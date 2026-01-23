import threading
import time
from werkzeug.serving import make_server
from src.account_registry import AccountRegistry
from app.api import app as flask_app
import app.api

class ServerThread(threading.Thread):
    def __init__(self, application):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', 5000, application)
        self.ctx = application.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

def before_all(context):
    context.server = ServerThread(flask_app)
    context.server.start()
    time.sleep(1)
    context.base_url = "http://127.0.0.1:5000/api/accounts"

def after_all(context):
    if hasattr(context, 'server'):
        context.server.shutdown()

def before_scenario(context, scenario):
    app.api.registry = AccountRegistry()