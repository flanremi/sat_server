#!/usr/bin/python
# _*_ coding:utf-8 _*_
import sys


class Ana:
    def __init__(self, file, scale, prob, rand, size, dec, res):
        self.file = file
        self.prob = prob
        self.scale = scale
        self.rand = rand
        self.size = size
        self.dec = dec
        self.res = res

    # cache_eff  命中
    def cache_eff(self):
        ch_eff = []
        counter = 0
        for sat in range(self.scale):
            hit = 0
            dec_, rand_ = self.dec[sat], self.rand[sat]
            for file_id in range(self.file):
                if dec_[file_id] == 1:
                    hit += self.prob[rand_[file_id]] * 100
            counter += hit
            ch_eff.append(hit)
        avr_ch_eff = counter / self.scale
        return ch_eff, avr_ch_eff

    def res_eff(self):
        r_eff = []
        counter = 0
        for sat in range(self.scale):
            used_res = 0
            dec_arr = self.dec[sat]
            rand_ = self.rand[sat]
            for file_id in range(self.file):
                if dec_arr[file_id] == 1:
                    used_res += self.size[rand_[file_id]]
            if used_res >= self.res[sat]:
                print("Error: It is beyond the storage space.")
                sys.exit()
            else:
                r_eff.append(used_res / self.res[sat] * 100)
            counter += used_res / self.res[sat] * 100
        avr_r_eff = counter / self.scale
        return r_eff, avr_r_eff

    def file_num(self):
        f_num = []
        counter = 0
        for sat in range(self.scale):
            num = 0
            dec_arr = self.dec[sat]
            for file_id in range(self.file):
                if dec_arr[file_id] == 1:
                    num += 1
            f_num.append(num)
            counter += num
        avr_f_num = counter // self.scale
        return f_num, avr_f_num

    def ctrl_delay(self, trans_delay, proc_delay):
        delay = trans_delay * 2 + proc_delay
        return delay
