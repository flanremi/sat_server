#!/usr/bin/python
# _*_ coding:utf-8 _*_
import sys
import math
import random
import numpy as np

# 最少缓存阈值
limit_s = 3

class Algo:

    # 单星文件上限，使用算法，卫星数，各卫星的容量上限
    def __init__(self, file, mode, scale, res):
        self.file = file
        self.mode = mode
        self.scale = scale
        self.res = res

    # result的值仅有traffic/feature中的子数组中元组个数来决定result的维数，因此不妨把traffic填充完毕后再调用该函数
    #
    def linear(self, traffic: list, w1=0.1, w2=0.8, w3=0.1):
        results = []
        for sat in range(self.scale):
            data = traffic[sat]
            file_num = len(data)
            # value measurement
            value = np.zeros(file_num, float)
            if file_num == 0:
                results.append(value)
                continue
            for file_id in range(file_num):
                feature = data[file_id]
                v = w1 * feature[0] + w2 * feature[1] + w3 * feature[2]
                value[file_id] = v
            # cache decision-making
            res_, counter = self.res[sat], self.file
            decision = np.zeros(file_num, int)
            max_index = np.argmax(value)
            while res_ >= (data[max_index])[2] and counter > 0 and file_num > 0:
                res_ -= (data[max_index])[2]
                counter -= (data[max_index])[1]
                file_num -= 1
                value[max_index] = np.min(value) - 1
                limit = data[max_index][1]
                max_index = np.argmax(value)
                # 最小缓存阈值
                if limit < limit_s:
                    continue
                decision[max_index] = 1
            results.append(decision)
            print("Scheduler is working for satellite {0}".format(sat), end="\r")
        return results, traffic

    # machine learning, one approach of unsupervised learning
    def cluster(self, traffic, cluster_num=3):
        results = []
        for sat in range(self.scale):
            data = traffic[sat]
            head_group = random.sample(range(self.file), cluster_num)
            member_group = []
            # divide file into k clusters
            for member_id in range(self.file):
                min_dist, best_head = -1, -1
                feature = data[member_id]
                for head_id in head_group:
                    feature_ = data[head_id]
                    dist = math.sqrt(pow(feature[0] - feature_[0], 2) + pow(feature[1] - feature_[1], 2))
                    if min_dist == -1 or dist < min_dist:
                        min_dist = dist
                        best_head = head_id
                member_group.append(best_head)
            # find the best head
            best_value, best_head = -1, -1
            for head_id in head_group:
                feature = data[head_id]
                value = feature[1] / feature[0]
                if best_value == -1 or value > best_value:
                    best_value = value
                    best_head = head_id
            # cache decision-making
            res_ = self.res[sat]
            decision = np.zeros(self.file, int)
            for file_id in range(self.file):
                if member_group[file_id] == best_head:
                    feature = data[file_id]
                    if res_ > feature[2]:
                        decision[file_id] = 1
                        res_ -= feature[2]
            results.append(decision)
            print("Scheduler is working for satellite {0}".format(sat), end="\r")
        return results

    # GBDT: gradient boosting decision tree
    # machine learning, one approach of supervised learning
    def gbdt(self, traffic, model):
        results = []
        for sat in range(self.scale):
            data = traffic[sat]
            X, size = [], []
            for file_id in range(self.file):
                feature = data[file_id]
                sample = [feature[0], feature[1]]
                X.append(sample)
                size.append(feature[2])
            pop_prediction = [np.float(val) for val in model.predict(X)]
            # cache decision-making
            res_ = self.res[sat]
            counter = self.file
            decision = np.zeros(shape=self.file, dtype=int)
            max_index = np.argmax(pop_prediction)
            while res_ >= size[max_index] and counter > 0:
                res_ -= size[max_index]
                decision[max_index] = 1
                counter -= 1
                pop_prediction[max_index] = np.min(pop_prediction) - 1
                max_index = np.argmax(pop_prediction)
            results.append(decision)
            print("Scheduler is working for satellite {0}".format(sat), end="\r")
        return results
