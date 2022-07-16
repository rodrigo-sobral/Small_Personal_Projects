from flask import Flask
from threading import Thread

class WebServer:
    app = Flask(__name__)

    def __init__(self, port: int = 8080):
        self.PORT = port

    def runServerInstance(self):
        Thread(target=self.runWebServer).start()

    @app.route('/')
    def home():
        return "Hello, I am alive!"

    def runWebServer(self):
        print('Running WebServer...')
        self.app.run('0.0.0.0', self.PORT)
