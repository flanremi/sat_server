import sys
import time

from analysis import Ana
from network import Network
from process import Process
from traffic import Traffic


def run():
    # 单位 KB
    res_size = 102400.0
    sat_num = 120
    plane_num = 12
    altitude = 880.0
    inclination = 86.0
    alpha = 0.7
    file_num = 1000
    req = 100000
    # 单位 S
    time_ = 3600
    algo = "Linear"
    output = "output-120-sat-Linear.txt"
    file_path = "sat-bit-o1s120.txt"
    user_longitude = 30
    user_latitude = 30
    user_longitude2 = 60
    user_latitude2 = 60
    net = Network(sat_num, plane_num, altitude, inclination)
    t = Traffic(res_size, sat_num)
    t.set_pattern()
    file_list = t.get_file_list()
    size_list = t.get_size_list()
    # random为每一个星的随机请求次数
    rand_list = t.get_random_pop()
    p = Process(file_list, size_list, rand_list, sat_num, file_path)
    p.init()
    # init request
    p.proc("test1.txt", user_longitude, user_latitude)
    p.proc("test2.txt", user_longitude, user_latitude)
    p.proc("test3.txt", user_longitude, user_latitude)
    file = p.get_file()
    results = p.get_results()
    prob = p.get_req_prop()
    size = p.get_size()
    traffic = p.get_feature_list()
    filename_list = p.get_filename_list()
    proc_time = p.get_proc_time()
    r = Ana(file, sat_num, prob, rand_list, size, results, size_list)
    # total_hit, avr_hit = r.cache_eff()
    # total_eff, avr_eff = r.res_eff()
    # total_num, avr_num = r.file_num()
    delivr_time = net.get_delay()
    total_delay = r.ctrl_delay(delivr_time, proc_time)
    print("File", output, "have more details.")
    try:
        with open(output, 'w+') as output_file:
            output_file.write(
                "==================================================================================================" +
                "==================================================================================================" +
                "=========================================\n")
            output_file.write("\n\n")
            output_file.write(
                "                               SatNet Scheduler Software                                   \n")
            output_file.write("\n")
            str_time = time.asctime(time.localtime(time.time()))
            output_file.write("Time: " + str_time + "\n")

            output_file.write(
                "==================================================================================================" +
                "==================================================================================================" +
                "=========================================\n")
            output_file.write(
                "                                        Network Setting                                    \n")
            output_file.write("Constellation: Self-Defined Satellite Network\n")

            output_file.write("Satellite: " + str(sat_num) + "\n")
            output_file.write("Plane: " + str(plane_num) + "\n")
            output_file.write("Altitude: " + str(altitude) + "\n")
            output_file.write("Orbit Inclination: " + str(inclination) + "\n")

            output_file.write(
                "==================================================================================================" +
                "==================================================================================================" +
                "=========================================\n")
            output_file.write(
                "                                       Parameter Setting                                   \n")
            output_file.write("Alpha: " + str(alpha) + "\n")
            output_file.write("File: " + str(file_num) + "\n")
            output_file.write("File Size: [100kb, 1Mb] \n")
            output_file.write("Request: " + str(req) + "\n")
            output_file.write("Duration: " + str(time_) + "\n")
            output_file.write("Satellite Storage Space: 100Mb \n")

            output_file.write("Algorithm: " + str(algo) + "\n")
            output_file.write(
                "==================================================================================================" +
                "==================================================================================================" +
                "=========================================\n")
            output_file.write(
                "                                      Experiment Results                                   \n")

            # output_file.write("Request Satisfaction: " + str(avr_hit) + "%\n")
            # output_file.write("Number of Cached Files: " + str(avr_num) + " / " + str(file) + "\n")
            # output_file.write("Resource Utility Efficiency: " + str(avr_eff) + "%\n")
            # output_file.write("Maximum Transmission Delay: " + str(delivr_time) + "s\n")
            # if algo == 2:
            # output_file.write("Algorithm Running Time: " + str(train_time) + "s\n")
            output_file.write("Algorithm Running Time: " + str(proc_time) + "s\n")
            output_file.write("Total Scheduling Time: " + str(total_delay) + "s\n")
            output_file.write(
                "==================================================================================================" +
                "==================================================================================================" +
                "=========================================\n")
            output_file.write(
                "                                        Content Info                                       \n")

            output_file.write(
                "--------------------------------------------------------------------------------------------------" +
                "--------------------------------------------------------------------------------------------------" +
                "------------------------------------------\n")
            output_file.write(
                "File Size Of " + str(file) + " Files In This Experiment: \n")
            count = 0
            for file_id in range(file):
                count += 1
                output_file.write(str(size[file_id]) + "   ")
                if count == 10:
                    count = 0
                    output_file.write("\n")
            if file % 10 != 0:
                output_file.write("\n")
            output_file.write(
                "--------------------------------------------------------------------------------------------------" +
                "--------------------------------------------------------------------------------------------------" +
                "------------------------------------------\n")
            output_file.write(
                "                                        File Info                                       \n")
            output_file.write(
                "--------------------------------------------------------------------------------------------------" +
                "--------------------------------------------------------------------------------------------------" +
                "------------------------------------------\n")
            output_file.write(
                "%-16s%-16s%-16s%-16s%-16s%-16s%-16s\n" % (
                    "SatID", "FileName", "PopRank", "Size", "ReqProb", "ReqTimes", "Action"))
            for sat_id in range(sat_num):
                # f_size_arr, rand_arr, result_arr = f_size[sat], rand[sat], results[sat]
                data = traffic[sat_id]
                rand_ = rand_list[sat_id]
                dec = results[sat_id]
                for file_id in range(file):
                    feature = data[file_id]
                    req_prob = prob[rand_[file_id]]
                    req_time = req_prob * req
                    output_file.write(
                        "%-16d%-16s%-16d%-16.2f%-16.6f%-16.2f%-16s\n" % (
                            sat_id, filename_list[file_id], rand_[file_id] + 1, feature[2], req_prob,
                            req_time, dec[file_id]))

    except FileNotFoundError:
        print("Error: Cannot open file %s", output)
        sys.exit()
    except IOError:
        print("Error: There is an IO errorb")
        sys.exit()
    # request again
    p.request("test1.txt", user_longitude, user_latitude)
    p.request("test2.txt", user_longitude2, user_latitude2)
    hit_count = p.get_hit_count()
    total_count = p.get_total_count()
    avr_hit = hit_count / total_count * 100
    print("Request Satisfaction: %.2f %%" % avr_hit)

    print("Maximum Transmission Delay: ", delivr_time, "s")
    print("Algorithm Running Time: ", proc_time, "s")
    print("Total Scheduling Time: ", total_delay, "s")


if __name__ == '__main__':
    run()
