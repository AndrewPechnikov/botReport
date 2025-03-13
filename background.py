from flask import Flask
from flask import request
from threading import Thread
import time
import requests
import os

app = Flask('')


@app.route('/')
def home():
  return "I'm alive"


def run():
  port = int(os.environ.get('PORT', 80))
  app.run(host='0.0.0.0', port=port)


def keep_alive():
  t = Thread(target=run)
  t.start()
