import random
from datetime import datetime

from geopy.distance import geodesic
import math

list = []


# use
# t = Time_vary_1(self.file_path, user_latitude, user_longitude, service_duration)
# message_out = t.produce()
# print(message_out)

class Time_vary_1:
    # para_list file_path, user_latitude, user_longitude, service_duration(min)
    def __init__(self, u_lat, u_lon, s_dur):
        self.file_path = "sat-bit-o1s120.txt"
        self.u_lat = float(u_lat)
        self.u_lon = float(u_lon)
        self.s_dur = int(s_dur)

    def readtxt(self):
        filename = self.file_path  # 给定文件路径
        lines = ''  # 用于将存储行的变量提前声明为string格式，避免编译器自动声明时可能由于第一行的特殊情况造成的数据类型错误
        time = -1.0
        sat = []
        with open(filename, 'r') as file_to_read:  # 打开文件
            while True:
                lines = file_to_read.readline()  # 整行读取数据
                if not lines:
                    break
                else:
                    if lines[0] == 'r':
                        this_lines = lines.split()  # 根据空格对字符串进行切割，由于切割后的数据类型有所改变(str-array)建议新建变量进行存储
                        sat_send = [this_lines[2], float(this_lines[12]), float(this_lines[13])]
                        sat_recv = [this_lines[3], float(this_lines[14]), float(this_lines[15])]
                        if this_lines[1] != time and this_lines[1] != '0.0150' and this_lines[2] == '0':
                            # if this_lines[1] != time and this_lines[1] != '0.0162' and this_lines[2] == '0':
                            list.append(sat)
                            sat = []
                            time = this_lines[1]
                            sat.append(sat_send)
                            sat.append(sat_recv)
                        elif this_lines[1] == '86340.0150' and this_lines[2] == '118':
                            # elif this_lines[1] == '3599.0162' and this_lines[2] == '8':
                            sat.append(sat_send)
                            sat.append(sat_recv)
                            list.append(sat)
                        else:
                            sat.append(sat_send)
                            sat.append(sat_recv)

    def distance(self, lat1, lon1, lat2, lon2):
        use = self.LLA_to_XYZ(lat1, lon1, 0)
        lro = self.LLA_to_XYZ(lat2, lon2, 880)
        dis = math.sqrt((lro[0] - use[0]) ** 2 + (lro[1] - use[1]) ** 2 + (lro[2] - use[2]) ** 2)
        return dis

    def LLA_to_XYZ(self, latitude, longitude, altitude):
        # 经纬度的余弦值
        cosLat = math.cos(latitude * math.pi / 180)
        sinLat = math.sin(latitude * math.pi / 180)
        cosLon = math.cos(longitude * math.pi / 180)
        sinLon = math.sin(longitude * math.pi / 180)

        # WGS84坐标系的参数
        rad = 6378.1370  # 地球赤道平均半径（椭球长半轴：a）
        f = 1.0 / 298.257224  # WGS84椭球扁率 :f = (a-b)/a
        C = 1.0 / math.sqrt(cosLat * cosLat + (1 - f) * (1 - f) * sinLat * sinLat)
        S = (1 - f) * (1 - f) * C
        h = altitude

        # 计算XYZ坐标
        X = (rad * C + h) * cosLat * cosLon
        Y = (rad * C + h) * cosLat * sinLon
        Z = (rad * S + h) * sinLat
        XYZ = [X, Y, Z]
        return XYZ

    def time_c(self, s):
        return str(s)
        # hour = int(s / 60)
        # minute = s % 60
        # if minute < 10:
        #     time = str(hour) + ":0" + str(minute)
        # else:
        #     time = str(hour) + ":" + str(minute)
        # return time

    def change(self, i):
        if i < 10:
            name = "L0" + str(i)
        else:
            name = "L" + str(i)
        return name

    def get_l(self, time, lat, lon):
        # t = datetime.now().hour * 60 + datetime.now().minute
        t = 0
        for i in range(t, (t + time)):
            each_time = list[i]
            dis = 13622
            lr0 = 0
            for s_sat in range(120):
                each_l = each_time[s_sat]
                dis_c = self.distance(lat, lon, float(each_l[1]), float(each_l[2]))
                if dis > dis_c:
                    dis = dis_c
                    lr0 = each_l[0]
            if i == t:
                res = "CDN Satellite Service\tStart time\tEnd time:\n"
                res += self.change(int(lr0)) + '\t' + self.time_c(i)
            else:
                res_sp = res.split()
                if (self.change(int(lr0))) != res_sp[len(res_sp) - 2]:
                    res += '\t' + self.time_c((i - 1)) + '\n'
                    res += self.change(int(lr0)) + '\t' + self.time_c(i)
                    if i == t + time - 1:
                        res += '\t' + self.time_c(i)
                elif i == t + time - 1:
                    res += '\t' + self.time_c(i)
        return res

    def produce(self):
        self.readtxt()
        m_out = self.get_l(self.s_dur, float(self.u_lat), float(self.u_lon))
        return m_out

    def result(self):
        r = []
        message_out = self.produce().split("\n")
        for i in range(1, len(message_out)):
            message = message_out[i].split("	")
            r.append({"sname": message[0], "start": int(message[1]),
                      "lasting": int(message[2]) - int(message[1]) + 1})
        return r
