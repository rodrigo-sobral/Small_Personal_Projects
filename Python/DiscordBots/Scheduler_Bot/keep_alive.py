from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home(): return "Hello, I am alive!"

def runWebServer():
    print('Running WebServer...')
    app.run('0.0.0.0', 8080)

def keep_alive(): Thread(target=runWebServer).start()