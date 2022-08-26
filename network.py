#!/usr/bin/python
# _*_ coding:utf-8 _*_
import random
import sys
import math

EARTH_RADIUS = 6378
PI = 3.1415926535897

# 构建网络
# para: sat_num, plane_num, altitude, incli
class Network:
    def __init__(self, sat_num, plane_num, altitude, incl):
        self.sat_num = sat_num
        self.plane_num = plane_num
        self.altitude = altitude
        self.incl = incl
        self.inclination = None

    def get_inter_plane(self, sat_id):
        inter_plane_id = sat_id % self.plane_num
        if inter_plane_id >= self.plane_num or inter_plane_id < 0:
            print("Error in setting topology: plane id out of bounds")
        return inter_plane_id

    def get_intra_plane(self, sat_id):
        intra_plane_id = sat_id // self.plane_num
        if intra_plane_id < 0:
            print("Error in setting topology: plane ind out of bounds")
        return intra_plane_id

    def get_sat_id(self, inter_plane_id, intra_plane_id):
        sat_id = intra_plane_id * self.plane_num + inter_plane_id
        if sat_id >= self.sat_num:
            print("Error in setting topology: satellite id out of bounds")
            sys.exit()
        return sat_id

    def get_lon(self, plane_id):
        # plane_id should be inter_plane_id
        lon = 180 / self.plane_num * plane_id
        if lon < -180 or lon > 180:
            print("Error in setting topology: lon out of bounds")
            sys.exit()
        return lon

    def get_alpha(self, intra_plane_id, inter_plane_id):
        if inter_plane_id % 2 == 0:
            alpha = 0 + 360 / (self.sat_num // self.plane_num) * intra_plane_id
        else:
            alpha = 360 / (self.sat_num // self.plane_num * 2) + 360 / (self.sat_num // self.plane_num) * intra_plane_id
        if alpha < 0 or alpha >= 360:
            print("Error in setting topology: alpha out of bounds")
            sys.exit()
        return alpha

    def get_inclination(self):
        inclination = self.incl * PI / 180
        if inclination >= PI:
            print("Error in calculating spherical theta: inclination out of bounds")
            sys.exit()
        return inclination

    def get_r(self):
        r = self.altitude + EARTH_RADIUS
        return r

    def get_theta_orbit(self, alpha):
        theta_orbit = alpha * PI / 180
        return theta_orbit

    def get_theta(self, theta_):
        theta = PI / 2 - math.asin(math.sin(self.inclination)) * math.sin(theta_)
        return theta

    def get_phi(self, lon, theta):
        if lon < 0:
            phi_orbit = (360 + lon) * PI / 180
        else:
            phi_orbit = lon * PI / 180
        if PI / 2 < theta < 3 * PI / 2:
            phi = math.atan(math.cos(self.inclination) * math.tan(theta)) + phi_orbit + PI
        else:
            phi = math.atan(math.cos(self.inclination) * math.tan(theta)) + phi_orbit
        return phi

    def get_sat_loc(self, sat_id):
        inter_plane_id, intra_plane_id = self.get_inter_plane(sat_id), self.get_intra_plane(sat_id)
        lon, alpha = self.get_lon(inter_plane_id), self.get_alpha(intra_plane_id, inter_plane_id)

        theta_orbit = self.get_theta_orbit(alpha)

        r = self.altitude + EARTH_RADIUS
        theta = self.get_theta(theta_orbit)
        phi = self.get_phi(lon, theta_orbit)

        x = r * math.sin(theta) * math.cos(phi)
        y = r * math.sin(theta) * math.sin(phi)
        z = r * math.cos(phi)
        return x, y, z

    def get_net_loc(self):
        location = []
        self.inclination = self.get_inclination()
        for sat_id in range(self.sat_num):
            location.append(self.get_sat_loc(sat_id))
        return location

    def get_controller(self):
        controller = random.randint(0, self.sat_num - 1)
        return controller

    def get_2nodes_delay(self, loc1, loc2):
        light_speed = 3 * pow(10, 8)
        delay = math.sqrt( pow(loc1[0] - loc2[0], 2) + pow(loc1[1] - loc2[1], 2) + pow(loc1[2] * 1000 - loc2[2] * 1000, 2)) / light_speed
        return delay

    def get_delay(self):
        loc = self.get_net_loc()
        sendr = self.get_controller()

        max_delay = -1
        threshold = self.plane_num / 2

        for recvr in range(self.sat_num):
            delay = 0
            node1 = sendr
            r_id, r_id_ = self.get_inter_plane(recvr), self.get_intra_plane(recvr)
            n_id, n_id_ = self.get_inter_plane(node1), self.get_intra_plane(node1)
            # delay in intra-plane route
            while n_id_ != r_id_:
                if n_id_ > r_id_:
                    node2 = self.get_sat_id(n_id, n_id_ - 1)
                else:
                    node2 = self.get_sat_id(n_id, n_id_ + 1)
                delay += self.get_2nodes_delay(loc[node1], loc[node2])
                node1 = node2
                n_id, n_id_ = self.get_inter_plane(node1), self.get_intra_plane(node1)
            # delay in inter-plane route
            while n_id != r_id:
                if n_id > r_id + threshold:
                    if n_id == self.plane_num - 1:
                        node2 = self.get_sat_id(0, n_id_)
                    else:
                        node2 = self.get_sat_id(n_id + 1, n_id_)
                elif r_id < n_id <= r_id + threshold:
                    node2 = self.get_sat_id(n_id - 1, n_id_)
                elif r_id - threshold <= n_id < r_id:
                    node2 = self.get_sat_id(n_id + 1, n_id_)
                else:
                    if n_id == 0:
                        node2 = self.get_sat_id(self.plane_num - 1, n_id_)
                    else:
                        node2 = self.get_sat_id(n_id - 1, n_id_)
                delay += self.get_2nodes_delay(loc[node1], loc[node2])
                node1 = node2
                n_id, n_id_ = self.get_inter_plane(node1), self.get_intra_plane(node1)
            if node1 == recvr:
                if max_delay == -1 or delay > max_delay:
                    max_delay = delay
            else:
                print("Error: satellite %d cant route to %d" % (sendr, recvr))
                sys.exit()
        return max_delay
