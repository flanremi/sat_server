import math
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from abc import ABCMeta, abstractmethod

from algorithm import Algo
from time_vary_2 import Time_vary_2


class CoreInter(metaclass=ABCMeta):

    @abstractmethod
    def timeChangeListener(self, core):
        pass

    # 0 start 1 processing 2 end
    @abstractmethod
    def refreshListener(self, core, period, fin_list: list):
        pass


# 维护一个时间轴来替代频度, 同时维护刷新过程
class TimeCore:

    def __init__(self, client_num: int, tp: ThreadPoolExecutor) -> None:
        super().__init__()
        self.client_num = client_num
        self.client_list = [{} for i in range(client_num)]
        self.client_list_pre = [{} for i in range(client_num)]
        self.sat_num = 120
        self.sat_size = [999999 for i in range(self.sat_num)]
        self.file_limit = 100
        self._Ttime = 0
        self.tp = tp
        self.inRefresh = False
        self.listener = None

    def addRequest(self, client_pos: int, name: str, size: int):
        while self.inRefresh:
            time.sleep(0.5)
        client = self.client_list[client_pos]
        if not client.get(name):
            client.update({name: {"time": 0, "size": size, "is_cache": False}})
        file = client.get(name)
        file.update({"time": file.get("time") + 1})

    def getFeature(self):
        features = []
        for i in range(len(self.client_list)):
            client = self.client_list[i]
            files = []
            for name, value in client.items():
                files.append((self._Ttime / value.get("time"), value.get("time"), value.get("size"), name))
            features.append(files)
        return features

    def getDispatch(self):
        a = Algo(self.file_limit, "", self.sat_num, self.sat_size)
        return a.linear(self.getFeature())

    def getTime(self):
        return self._Ttime

    # todo 处理异步问题，处理传输时更新问题，处理cache冲突问题
    def refresh(self):
        self.inRefresh = True
        if self.listener:
            self.listener.refreshListener(self, 0, self.client_list)
        for i in range(self.client_num):
            client = self.client_list[i]
            client_pre = self.client_list_pre[i]
            for key, value in client.items():
                pass
        # with open("mv2.mp4", "rb") as file:
        #     res = requests.post("http://192.168.50.63:4995/upload", files={"file": file}, data={"name": "cheat1.mp4"})
        #     print(res.text)
        # pass

    def run(self):
        def run_():
            while True:
                time.sleep(1)
                self._Ttime += 1
                if self.listener:
                    self.listener.timeChangeListener(self)
                if self._Ttime % 60 == 0:
                    self.tp.submit(self.refresh)

        self.tp.submit(run_)

    def setListener(self, listener: CoreInter):
        self.listener = listener
