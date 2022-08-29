import random
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

# t = TimeCore(120, theard_pool)
# t.run()
# for i in range(50000):
#     t.addRequest(random.randint(0, 119),"aaa" + str(random.randint(0, 20)), 10)
# t.dispatch()
# while True:
#     pass

a = {}
b = a.get("aaa")
print(b)