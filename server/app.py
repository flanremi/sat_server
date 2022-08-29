import json
import random
import time
from abc import ABC

from flask import Flask, request
from concurrent.futures import ThreadPoolExecutor

from alter.process import TimeCore, CoreInter
import k8s_tools
from time_vary_1 import Time_vary_1


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
    i = 0
    for r in t:
        i += 1
        client_num = int(r.get("sname")[1:len(r.get("sname"))])
        core.addRequest(client_num, name)
        file = core.getfile(client_num, name)
        if not file or file.get("is_cache") == 0:
            url = k8s_tools.pushStream(k8s_tools.sname2ip("master"), k8s_tools.sname2ip(r.get("sname")), name, str(i))
        else:
            url = k8s_tools.pushStream(k8s_tools.sname2ip(r.get("sname")), k8s_tools.sname2ip(r.get("sname")), name, str(i))
        dis_result.append({"url": url, "start": r.get("start"), "lasting": r.get("lasting")})
    return json.dumps(dis_result)

# for i in range(100):
#     t.addRequest(random.randint(0, 119),"aaa" + str(random.randint(0, 20)), 10)
# t.refresh()
# for i in range(5000):
#     t.addRequest(random.randint(0, 119),"aaa" + str(random.randint(0, 20)), 10)
# t.refresh()
# while True:
#     pass
