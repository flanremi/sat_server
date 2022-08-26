import math
import random
import sys
import time

from algorithm import Algo
from time_vary_2 import Time_vary_2


# 维护一个时间轴来替代频度
class TimeCore:

    def __init__(self, client_num: int) -> None:
        super().__init__()
        self.client_num = client_num
        self.client_list = [[] for i in range(client_num)]
        self.client_time_list = [0 for i in range(client_num)]
        self.sat_num = 120
        self.sat_size = [999999 for i in range(self.sat_num)]
        self.file_limit = 100

    def notifyTime(self, client_pos: int, name: str, size: int):
        self.client_time_list[client_pos] += 1
        client = self.client_list[client_pos]
        for file in client:
            if file.get("name") == name:
                file.update({"time": file.get("time") + 1})
                return
        client.append({"name": name, "time": 1, "size": size})

    def getFeature(self):
        features = []
        for i in range(len(self.client_list)):
            client = self.client_list[i]
            Ttime = self.client_time_list[i]
            files = []
            for file in client:
                files.append((Ttime / file.get("time"), file.get("time"), file.get("size")))
            features.append(files)
        return

    def getDispatch(self):
        a = Algo(self.file_limit, "", self.sat_num, self.sat_size)
        return a.linear(self.getFeature())
