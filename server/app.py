import json
import random
import time
from abc import ABC
import os

import requests as requests
from threading import Lock
from flask import Flask, request
from concurrent.futures import ThreadPoolExecutor

from alter.process import TimeCore, CoreInter
import k8s_tools
from time_vary_1 import Time_vary_1

lock = Lock()
lock_camera = Lock()


class Listener(CoreInter, ABC):

    def initListener(self, core):
        from server.pycode.leslie_sysinfo_code import get_all_node_name_ip
        node = get_all_node_name_ip()
        result = []
        for name, ip in node:
            res = requests.post("http://" + ip + ":4995/query")
            result.append({"name": name, "cache": json.loads(res.text.replace("\'", "\""))})
        for i in range(len(core.client_list_pre)):
            caches = result[i % 2 + 1].get("cache")
            client = core.client_list_pre[i]
            for cache in caches:
                client.update({cache: {"time": 0, "size": os.stat("file/" + cache).st_size / 1024, "is_cache": 1}})

    def timeChangeListener(self, core):
        # print(core.getTime())
        pass

    # 已是异步的环境
    def refreshListener(self, core, period, fin_list: list, now_s_pos: int, now_file: dict):
        if period == 11:
            with open("file/" + now_file.get("name"), "rb") as file:
                res = requests.post("http://" + k8s_tools.sname2Node(k8s_tools.pos2sname(now_s_pos)).Ip
                                    + ":4995/upload", files={"file": file},
                                    data={"name": now_file.get("name")})
                print(res.text)
        elif period == 12:
            res = requests.post("http://" + k8s_tools.sname2Node(k8s_tools.pos2sname(now_s_pos)).Ip
                                + ":4995/delete",
                                data={"name": now_file.get("name")})
            print(res.text)
        # self.initListener(core)


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
k8s_tools.deployFileServer()
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
    satellites = Time_vary_1(lat, lng, dur).result()
    print(satellites)
    dis_result = []
    i = 0
    for satellite in satellites:
        i += 1
        client_num = k8s_tools.sname2Pos(satellite.get("sname"))
        core.addRequest(client_num, name)
        file = core.getfile(client_num, name)

        if not file or file.get("is_cache") == 0:
            url = k8s_tools.pushStream(k8s_tools.nodeName2Node("d02"), k8s_tools.sname2Node(satellite.get("sname")),
                                       name, str(random.randint(0, 100)))
            # time.sleep(random.randint(4500, 6000) / 1000)
        else:
            url = k8s_tools.pushStream(k8s_tools.sname2Node(satellite.get("sname")),
                                       k8s_tools.sname2Node(satellite.get("sname")), name,
                                       str(random.randint(0, 100) + 100))
        dis_result.append({"url": url, "start": satellite.get("start"), "lasting": satellite.get("lasting")})
    return json.dumps(dis_result)


@app.route("/cdn_show", methods=['POST'])
def cdn_show():
    host = request.form.get("host")
    if not host == "cache":
        time.sleep(random.randint(4500, 6000) / 1000)
        url = k8s_tools.pushStream(k8s_tools.nodeName2Node("d02"), k8s_tools.nodeName2Node("d03"), "time.mp4",
                                   str(10))
    else:
        url = k8s_tools.pushStream(k8s_tools.nodeName2Node("d03"), k8s_tools.nodeName2Node("d03"), "time.mp4",
                                   str(101))
    return url


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


@app.route("/yolo_notify", methods=['POST'])
def yolo_notify():
    box = request.form.get("box")
    camera = request.form.get("name")
    lock.acquire()
    with open("camera" + str(camera) + ".txt", "w") as file:
        file.write(str(box))
    lock.release()
    return "OK"


@app.route("/yolo_get", methods=['POST'])
def yolo_get():
    camera = request.form.get("camera")
    with open("camera" + str(camera) + ".txt", "r") as file:
        result = file.read()
    return result


@app.route("/count_move", methods=['POST'])
def count_move():
    k8s_tools.deployYolo()
    return "ok"


@app.route("/count_move_2", methods=['POST'])
def count_move2():
    pos = request.form.get("pos")
    k8s_tools.deployYolo2(int(pos))
    return "ok"


@app.route("/count_move_del_2", methods=['POST'])
def count_move_del2():
    pos = request.form.get("pos")
    k8s_tools.deleteYolo(int(pos))
    return "ok"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
