#!/usr/bin/python
# _*_ coding:utf-8 _*_
import sys
import random


class Traffic:
    #  1000, 120
    def __init__(self, size, scale):
        self.size = size
        self.scale = scale
        # 单星的文件负载上限
        self.file = 1000
        self.file_list = []
        self.size_list = []
        self.rand = []

    # set_file_list
    def set_file_list(self):
        for sat_id in range(self.scale):
            sat_file = []
            self.file_list.append(sat_file)

    # get_file_list
    def get_file_list(self):
        return self.file_list

    # set_size_list
    def set_size_list(self):
        self.size_list = [self.size for i in range(self.scale)]

    # get_size_list
    def get_size_list(self):
        return self.size_list

    def set_random_pop(self, rand):
        self.rand.append(rand)

    def get_random_pop(self):
        if len(self.rand) != self.scale:
            print("Error in simulating file's popularity: random popularity out of bounds")
            sys.exit()
        return self.rand

    def set_pattern(self):
        self.set_file_list()
        self.set_size_list()
        for sat_id in range(self.scale):
            rand_list = random.sample(range(self.file), self.file)
            self.set_random_pop(rand_list)
