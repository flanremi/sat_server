import time

from flask import Flask
from concurrent.futures import ThreadPoolExecutor

from alter.process import TimeCore

theard_pool = ThreadPoolExecutor(max_workers=4)

# app = Flask(__name__)


# CDN
# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

# TimeCore(120, theard_pool).run()
# while True:
#     pass