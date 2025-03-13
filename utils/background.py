
from flask import Flask
from flask import request
from threading import Thread
import time
import requests
import os

# Створення Flask додатку для запобігання "засинанню" сервера на безкоштовних хостингах
app = Flask('')

@app.route('/')
def home():
    """
    Головний маршрут, який повертає просту відповідь для перевірки, що сервер працює
    """
    return "I'm alive"

def run():
    """
    Функція запуску Flask сервера на вказаному порту
    """
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    """
    Функція, яка запускає Flask сервер у окремому потоці
    Це дозволяє боту працювати постійно на безкоштовних хостингах
    """
    t = Thread(target=run)
    t.start()
