import subprocess

from pycode.leslie_sysinfo_code import get_all_node_name_ip
import yaml

from pycode.Node import *
from pycode.utils import *


def sname2ip(sname):
    nodes = get_all_node_name_ip()
    # todo 映射节点名和卫星名
    return Node({"Name": "ubuntu", "Ip": nodes[0][1]})


def pushStream(start: Node, target: Node, name, url_suf):
    with open("yaml_file/ffmpeg_video.yaml", 'r') as f:
        yaml_file = yaml.load(f, Loader=yaml.FullLoader)

        yaml_file['spec']['template']['spec']['nodeName'] = str(start.Name)

        yaml_file['spec']['template']['spec']['containers'][0]['args'][2] = "/usr/app/tmp/" + name
        yaml_file['spec']['template']['spec']['containers'][0]['args'][8] = "rtmp://" + target.Ip + "/live/" + name + \
                                                                            url_suf

        changed_yaml_name = start.Name + get_r_code() + "-" + "ffmpeg_video.yaml"
        changed_yaml_name = changed_yaml_name.replace("_", "-")
        yaml_file['metadata']['name'] = changed_yaml_name
        changed_yaml_name = "yaml_file/tmp/" + start.Name + get_r_code() + "_" + "ffmpeg_video.yaml"
        changed_yaml_name = changed_yaml_name.replace("-", "_")
        with open(changed_yaml_name, 'w+') as out:
            yaml.dump(yaml_file, out)
        #
        cmd = "kubectl apply -f " + changed_yaml_name
        kube_apply_info = subprocess.check_output(cmd, shell=True).decode('utf-8')
        print(kube_apply_info)
        return "rtmp://" + target.Ip + "/live/" + name + url_suf

# pushStream(sname2ip(""), sname2ip(""), "cheat.mp4", "11919")
