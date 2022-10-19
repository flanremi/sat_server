import json

import requests
from importlib_metadata import Deprecated

from leslie_sysinfo_code import *
from leslie_temporary_info import *
import random
import Node
from utils import log


def select_one_node(all_node_names, demands: dict):
    memorys = json.loads(
        requests.get("http://192.168.50.140:30000/api/v1/query?query=node_memory_MemAvailable_bytes").text)
    datas = []
    for name in all_node_names:
        datas.append(Node.nodeCreate(get_node_info(name)))
    i = 0
    while i < len(datas):
        if not datas[i].canUse():
            datas.remove(datas[i])
            continue
        if datas[i].Name == "201" or datas[i].Name == "202":
            datas.remove(datas[i])
            continue
        i += 1
    scopes = []
    names = []
    maxScope = 0
    maxPos = 0
    for i in range(len(datas)):
        data = datas[i]
        for memory in memorys.get("data").get("result"):
            if memory.get("metric").get("instance").find(getIIpByAnno(data)) != -1 and \
                    memory.get("metric").get("job").find("kubernetes-service-endpoints") != -1:
                scope = getNodeScope(datas[i], memory, {})
                scopes.append(scope)
                if scope > maxScope:
                    maxScope = scope
                    maxPos = i
        names.append(datas[i].Name)
    log(str(scopes) + "\t" + str(names))
    return datas[maxPos]


def getSequence(lat, lon, dur):
    seqs = json.loads(requests.get("http://192.168.2.102:5000/startime", {"lat": lat, "lon": lon, "during": dur}).text)
    for i in range(len(seqs)):
        seq = seqs[i]
        seq.update({"name": nodeNameByL(seq.get("name"))})
    return seqs


def getNodeScope(node: Node.Node, memory, demamds: dict):
    scope = 0
    if node.Name.find("z") != -1:
        scope += 0.5
    if node.Name.find("s") != -1:
        scope -= 3.5
    if node.Name.find("d09") != -1:
        scope -= 1.8
    scope += int(memory.get("value")[1]) / 1024 / 1024 / 1024
    return round(scope, 4)


def getIIpByAnno(node: Node):
    anno = node.Annotations
    for s in anno:
        if "VXLAN" in s:
            result = s.split(": ")[1].split(".")
            return result[0] + "." + result[1] + "." + result[2]
    return ''
