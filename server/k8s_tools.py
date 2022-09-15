import subprocess

import yaml

from server.pycode.leslie_sysinfo_code import *
from server.pycode.utils import *
from server.pycode.Node import *


# 总的Sname到卫星序号的映射函数
def sname2Pos(sname):
    return int(sname[1: len(sname)])


# 总的Sname到卫星序号的映射函数
def pos2sname(pos):
    return "L" + str(pos)


# 总的Sname到节点的映射函数
def sname2Node(sname):
    pos = sname2Pos(sname) % 2 + 1
    nodes = get_all_node_name_ip()
    return Node({"Name": nodes[pos][0], "Ip": nodes[pos][1]})


def nodeName2Ip(node_name):
    nodes = get_all_node_name_ip()
    for name, ip in nodes:
        if name == node_name:
            return ip


def nodeName2Node(node_name):
    nodes = get_all_node_name_ip()
    for name, ip in nodes:
        if name == node_name:
            return Node({"Name": name, "Ip": ip})


# def sname2ip(sname):
#     nodes = get_all_node_name_ip()
#     # todo 映射节点名和卫星名
#     # if sname == "k8s-master":
#     #     return Node({"Name": nodes[0][0], "Ip": nodes[0][1]})
#     # else:
#     #     return Node({"Name": nodes[1][0], "Ip": nodes[1][1]})
#     if sname == "d02":
#         return Node({"Name": nodes[0][0], "Ip": nodes[0][1]})
#     else:
#         pos = int(sname[1:len(sname)]) % 2 + 1
#         return Node({"Name": nodes[pos][0], "Ip": nodes[pos][1]})
#     # return Node({"Name": "ubuntu", "Ip": nodes[0][1]})


def pushStream(start: Node, target: Node, name, url_suf):
    with open("yaml_file/ffmpeg_video.yaml", 'r') as f:
        yaml_file = yaml.load(f, Loader=yaml.FullLoader)

        yaml_file['spec']['template']['spec']['nodeName'] = str(start.Name)
        # yaml_file['spec']['template']['spec']['volumes'][0]['hostPath']['path'] = "/home/dxh/cdn/"
        # yaml_file['spec']['template']['spec']['volumes'][0]['hostPath']['path'] = "/home/flan/tmp/fs_tmp/"
        yaml_file['spec']['template']['spec']['volumes'][0]['hostPath']['path'] = "/home/k8s/tmp/fs_tmp/"

        yaml_file['spec']['template']['spec']['containers'][0]['args'][2] = "/usr/app/tmp/" + name
        # yaml_file['spec']['template']['spec']['containers'][0]['args'][2] = "/home/" + name
        yaml_file['spec']['template']['spec']['containers'][0]['args'][8] = "rtmp://" + target.Ip + "/live/" + name + \
                                                                            url_suf

        changed_yaml_name = start.Name + get_r_code() + "-" + "ffmpeg_video"
        changed_yaml_name = changed_yaml_name.replace("_", "-")
        yaml_file['metadata']['name'] = changed_yaml_name
        changed_yaml_name = "yaml_file/tmp/yaml/" + start.Name + get_r_code() + "_" + "ffmpeg_video.yaml"
        changed_yaml_name = changed_yaml_name.replace("-", "_")
        with open(changed_yaml_name, 'w+') as out:
            yaml.dump(yaml_file, out)
        #
        cmd = "kubectl apply -f " + changed_yaml_name
        kube_apply_info = subprocess.check_output(cmd, shell=True).decode('utf-8')
        print(kube_apply_info)
        return "rtmp://" + target.Ip + "/live/" + name + url_suf


def deploySys():
    node = get_all_node_name_ip()
    for name, ip in node:
        with open("yaml_file/srs_run.yaml", 'r') as f:
            yaml_file = yaml.load(f, Loader=yaml.FullLoader)
            yaml_file['metadata']['labels']['app'] = "srs-" + name
            yaml_file['metadata']['name'] = "srs-" + name + "-deployment"
            yaml_file['spec']['selector']['matchLabels']['app'] = "srs-" + name
            yaml_file['spec']['template']['metadata']['labels']['app'] = "srs-" + name
            yaml_file['spec']['template']['spec']['nodeName'] = name
            yaml_file['spec']['template']['spec']['containers'][0]['name'] = "srs-" + name
            yaml_file_name = "yaml_file/tmp/sys/srs_run_" + name + ".yaml"
            with open(yaml_file_name, "w") as out:
                yaml.dump(yaml_file, out)
            cmd = "kubectl apply -f " + yaml_file_name
            subprocess.check_output(cmd, shell=True).decode('utf-8')


def deployFileServer():
    node = get_all_node_name_ip()
    for name, ip in node:
        with open("yaml_file/file_server.yaml", 'r') as f:
            yaml_file = yaml.load(f, Loader=yaml.FullLoader)
            yaml_file['metadata']['labels']['app'] = "file-server-" + name
            yaml_file['metadata']['name'] = "file-server-" + name + "-deployment"
            yaml_file['spec']['selector']['matchLabels']['app'] = "file-server-" + name
            yaml_file['spec']['template']['metadata']['labels']['app'] = "file-server-" + name
            yaml_file['spec']['template']['spec']['nodeName'] = name
            yaml_file['spec']['template']['spec']['containers'][0]['name'] = "file-server-" + name
            yaml_file_name = "yaml_file/tmp/sys/file_server_" + name + ".yaml"
            with open(yaml_file_name, "w") as out:
                yaml.dump(yaml_file, out)
            cmd = "kubectl apply -f " + yaml_file_name
            subprocess.check_output(cmd, shell=True).decode('utf-8')


def deployYolo():
    node = get_all_node_name_ip()
    i = 0
    for name, ip in node:
        with open("yaml_file/yolo.yaml", 'r') as f:
            yaml_file = yaml.load(f, Loader=yaml.FullLoader)
            yaml_file['metadata']['labels']['app'] = "yolo-" + name
            yaml_file['metadata']['name'] = "yolo-" + name + "-deployment"
            yaml_file['spec']['selector']['matchLabels']['app'] = "yolo-" + name
            yaml_file['spec']['template']['metadata']['labels']['app'] = "yolo-" + name
            yaml_file['spec']['template']['spec']['nodeName'] = name
            yaml_file['spec']['template']['spec']['containers'][0]['name'] = "yolo-" + name
            yaml_file['spec']['template']['spec']['containers'][0]['command'] = ["./start.sh"]
            yaml_file['spec']['template']['spec']['containers'][0]['args'] = ["192.168.50.25" + str(i),
                                                                              "admin", "osm123onap",
                                                                              "192.168.50.205:5000",
                                                                              "c" + str(i)]
            yaml_file_name = "yaml_file/tmp/sys/yolo_run_" + name + ".yaml"
            with open(yaml_file_name, "w") as out:
                yaml.dump(yaml_file, out)
            cmd = "kubectl apply -f " + yaml_file_name
            subprocess.check_output(cmd, shell=True).decode('utf-8')
        i += 1


def deployYolo2(pos):
    node = get_all_node_name_ip()
    name, ip = node[pos][0], node[pos][1]
    with open("yaml_file/yolo.yaml", 'r') as f:
        yaml_file = yaml.load(f, Loader=yaml.FullLoader)
        yaml_file['metadata']['labels']['app'] = "yolo-" + name
        yaml_file['metadata']['name'] = "yolo-" + name + "-deployment"
        yaml_file['spec']['selector']['matchLabels']['app'] = "yolo-" + name
        yaml_file['spec']['template']['metadata']['labels']['app'] = "yolo-" + name
        yaml_file['spec']['template']['spec']['nodeName'] = name
        yaml_file['spec']['template']['spec']['containers'][0]['name'] = "yolo-" + name
        yaml_file['spec']['template']['spec']['containers'][0]['command'] = ["./start.sh"]
        yaml_file['spec']['template']['spec']['containers'][0]['args'] = ["192.168.50.25" + str(pos),
                                                                          "admin", "osm123onap",
                                                                          "192.168.50.205:5000",
                                                                          "c" + str(pos)]
        yaml_file_name = "yaml_file/tmp/sys/yolo_run_" + name + ".yaml"
        with open(yaml_file_name, "w") as out:
            yaml.dump(yaml_file, out)
        cmd = "kubectl apply -f " + yaml_file_name
        subprocess.check_output(cmd, shell=True).decode('utf-8')


def deleteSysDeploy():
    infos = []
    for root, dic, files in os.walk("yaml_file/tmp/sys/"):
        for file in files:
            cmd = "kubectl delete -f " + root + file
            kube_apply_info = subprocess.check_output(cmd, shell=True).decode('utf-8')
            infos.append(kube_apply_info)
            os.remove(root + file)
    return infos


def deleteVideoDeploy():
    infos = []
    for root, dic, files in os.walk("yaml_file/tmp/yaml/"):
        for file in files:
            cmd = "kubectl delete -f " + root + file
            kube_apply_info = subprocess.check_output(cmd, shell=True).decode('utf-8')
            infos.append(kube_apply_info)
            os.remove(root + file)
    return infos
# pushStream(sname2ip(""), sname2ip(""), "cheat.mp4", "11919")
