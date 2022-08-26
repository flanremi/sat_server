import math
import random
import sys
import time

from algorithm import Algo
from time_vary_2 import Time_vary_2


class Process:
    def __init__(self, file_list, size_list, rand_list, scale, file_path):
        self.file_list = file_list
        self.size_list = size_list
        self.scale = scale
        self.file_path = file_path
        self.rand_list = rand_list

        self.file = 1000
        self.alpha = 0.7
        self.req = 100000
        self.time = 3600
        self.algo = "linear"
        self.proc_time = 0
        self.hit_count = 0
        self.total_count = 0
        self.filename_list = []
        self.file_size = []
        self.req_prop = []
        # （间隔，请求数，文件大小）
        self.feature_list = []
        self.results = []


    def set_size(self, min_size=100.0, max_size=1024.0):
        self.file_size.append(random.uniform(min_size, max_size))

    def get_size(self):
        return self.file_size

    def set_req_prop(self):
        # request' probability should obey zipf distribution 奇普夫分布（长尾分布）
        # f(x,n) = 1 / x^alpha * y(n) (x is rank of request' probability, x > 1)
        # y(n) = 1/1 + 1/2 + ... + 1/n (n is the total number of files)
        y = 0
        self.req_prop = []
        for rank in range(1, self.file + 1):
            y += pow(1 / rank, self.alpha)
        for rank in range(1, self.file + 1):
            f = 1 / (pow(rank, self.alpha) * y)
            self.req_prop.append(f)

    def get_req_count(self, index, rand):
        count = self.req * self.req_prop[rand[index]]
        if count >= self.req:
            print("Error is simulating file's request count: file's request count out of bounds")
        return count

    def get_req_interval(self, count):
        inr = self.time / count
        interval = math.fmod(self.time, inr)
        return interval

    def get_feature(self, index, sat_id):
        size = self.file_size[index]
        count = self.get_req_count(index, self.rand_list[sat_id])
        inr = self.get_req_interval(count)
        return inr, count, size

    def get_results(self):
        return self.results

    def get_file(self):
        return len(self.filename_list)

    def get_req_prop(self):
        return self.req_prop

    def get_feature_list(self):
        return self.feature_list

    def get_filename_list(self):
        return self.filename_list

    def get_proc_time(self):
        return self.proc_time

    def get_hit_count(self):
        return self.hit_count

    def get_total_count(self):
        return self.total_count

    def proc(self, file_name, user_longitude, user_latitude):
        # is_exist
        if file_name in self.filename_list:
            # to do
            # aim_fileNumber = self.filename_list.index(file_name)
            pass
        else:
            self.set_size()
            self.filename_list.append(file_name)
            aim_fileNumber = self.filename_list.index(file_name)
            # schedule:
            for sat_id in range(self.scale):
                self.feature_list[sat_id].append(self.get_feature(aim_fileNumber, sat_id))

            a = Algo(self.file, self.algo, self.scale, self.size_list)
            start_time = time.time()
            self.results = a.linear(self.feature_list, aim_fileNumber+1)
            end_time = time.time()
            self.proc_time = end_time - start_time
            print("The file " + file_name + " has been cached on the satellite")

    def request(self, file_name, user_longitude, user_latitude):
        self.total_count += 1
        # is_exist
        if file_name in self.filename_list:
            # to do
            # aim_fileNumber = self.filename_list.index(file_name)
            self.hit_count += 1
            t = Time_vary_2(self.file_path, user_longitude, user_latitude, self.scale)
            message_out = t.produce()
            print(message_out)
        else:
            self.set_size()
            self.filename_list.append(file_name)
            aim_fileNumber = self.filename_list.index(file_name)
            # schedule:
            for sat_id in range(self.scale):
                self.feature_list[sat_id].append(self.get_feature(aim_fileNumber, sat_id))
            a = Algo(self.file, self.algo, self.scale, self.size_list)
            start_time = time.time()
            self.results = a.linear(self.feature_list, aim_fileNumber+1)
            end_time = time.time()
            self.proc_time = end_time - start_time
            print("The file " + file_name + " is not on the satellite, now has been cached on the satellite")

    def init(self):
        for sat_id in range(self.scale):
            f_list = []
            self.feature_list.append(f_list)
        self.set_req_prop()
