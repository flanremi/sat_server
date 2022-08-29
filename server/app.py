import json
import random
import time
from abc import ABC

from flask import Flask, request
from concurrent.futures import ThreadPoolExecutor

from alter.process import TimeCore, CoreInter
from server.time_vary_1 import Time_vary_1


class Listener(CoreInter, ABC):

    def timeChangeListener(self, core):
        pass

    def refreshListener(self, core, period, fin_list: list):
        pass


theard_pool = ThreadPoolExecutor(max_workers=4)
core = TimeCore(120, theard_pool)
# t.setListener()
core.run()

app = Flask(__name__)


# CDN
@app.route("/cdn", methods=['POST'])
def cdn():
    lat = request.form.get("lat")
    lng = request.form.get("lng")
    dur = request.form.get("dur")
    name = request.form.get("name")
    t = Time_vary_1(lat, lng, dur).result()
    dis_result = []
    for r in t:
        client_num = int(r.get("sname")[1:len(r.get("sname"))])
        core.addRequest(client_num, name)
        file = core.getfile(client_num, name)
        if file.get("is_cache") == 0:
            pass
        else:
            pass
        dis_result.append({"url": "", "start": r.get("start"), "lasting": r.get("lasting")})
    return json.dumps(dis_result)

# for i in range(100):
#     t.addRequest(random.randint(0, 119),"aaa" + str(random.randint(0, 20)), 10)
# t.refresh()
# for i in range(5000):
#     t.addRequest(random.randint(0, 119),"aaa" + str(random.randint(0, 20)), 10)
# t.refresh()
# while True:
#     pass
