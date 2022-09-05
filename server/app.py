import json
import random
import time
from abc import ABC

import requests as requests
from threading import Lock
from flask import Flask, request
from concurrent.futures import ThreadPoolExecutor

from alter.process import TimeCore, CoreInter
import k8s_tools
from time_vary_1 import Time_vary_1

lock = Lock()


class Listener(CoreInter, ABC):

    def timeChangeListener(self, core):
        # print(core.getTime())
        pass

    # 已是异步的环境
    def refreshListener(self, core, period, fin_list: list, now_s_pos: int, now_file: dict):
        if period == 11:
            with open("file/" + now_file.get("name"), "rb") as file:
                res = requests.post("http://" + core.pos2Ip(now_s_pos).Ip + ":4995/upload", files={"file": file},
                                    data={"name": now_file.get("name")})
                print(res.text)
        elif period == 12:
            res = requests.post("http://" + core.pos2Ip(now_s_pos).Ip + ":4995/delete",
                                data={"name": now_file.get("name")})
            print(res.text)


theard_pool = ThreadPoolExecutor(max_workers=4)
core = TimeCore(120, theard_pool)
core.setListener(Listener())
core.run()
# core.addRequest(1, "name1.txt")
# core.addRequest(1, "name1.txt")
# core.addRequest(1, "name1.txt")
# core.addRequest(1, "name1.txt")
# core.addRequest(1, "name1.txt")
# core.addRequest(1, "name1.txt")
# while True:
#     pass
k8s_tools.deploySys()
import player

iplayer = player.Player()

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
            url = k8s_tools.pushStream(k8s_tools.sname2ip("k8s-master"), k8s_tools.sname2ip(r.get("sname")), name,
                                       str(i))
            time.sleep(random.randint(2500, 5000) / 1000)
        else:
            url = k8s_tools.pushStream(k8s_tools.sname2ip(r.get("sname")), k8s_tools.sname2ip(r.get("sname")), name,
                                       str(i))
        dis_result.append({"url": url, "start": r.get("start"), "lasting": r.get("lasting")})
    return json.dumps(dis_result)


@app.route("/time_v", methods=['POST'])
def time_v():
    lat = request.form.get("lat")
    lng = request.form.get("lng")
    dur = request.form.get("dur")
    t = Time_vary_1(lat, lng, dur).result()
    # dis_result = []
    # # test
    # i = 0
    # for r in t:
    #     if i % 2 == 0:
    return json.dumps(t)


@app.route("/get_cache", methods=['POST'])
def get_cache():
    from server.pycode.leslie_sysinfo_code import get_all_node_name_ip
    node = get_all_node_name_ip()
    result = []

    def get_client_cache(n: str, url: str):
        global lock
        res = requests.post("http://" + url + ":4995/query")
        lock.acquire()
        result.append({"name": n, "cache": res.text})
        lock.release()

    for name, ip in node:
        theard_pool.submit(get_client_cache, name, ip)

    while True:
        time.sleep(0.5)
        if len(result) == len(node):
            break
    return json.dumps(result)


@app.route("/remove_sys", methods=['POST'])
def remove_sys():
    return k8s_tools.deleteSysDeploy()


@app.route("/remove_video", methods=['POST'])
def remove_video():
    return k8s_tools.deleteVideoDeploy()


@app.route("/play_video", methods=['POST'])
def play_video():
    url = request.form.get("url")
    iplayer.play(url)
    return "OK"


@app.route("/stop_video", methods=['POST'])
def stop_video():
    iplayer.stop()
    # iplayer.release()
    return "OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
