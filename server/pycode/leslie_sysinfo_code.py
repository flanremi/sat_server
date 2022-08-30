import os
import subprocess
import yaml

from server.pycode.Node import *
from server.pycode.utils import *
from server.pycode.leslie_temporary_info import *

path = "tmp_deploy/"


def splitNodeStr(s: str):
    result = []
    start = 0
    for i in range(len(s)):
        if s[i] == " " and i > 1 and s[i - 1] != " " and s[i - 2] != " ":
            result.append(s[start:i])
        elif s[i] != "" and i > 1 and s[i - 1] == " " and s[i - 2] == " ":
            start = i
    return result


def get_all_node_name_ip():
    all_nodes = []
    kube_nodes_info = subprocess.check_output('kubectl get nodes -o=wide', shell=True).decode('utf-8')
    kube_nodes_info = kube_nodes_info.split('\n')

    i = 0
    for line in kube_nodes_info:
        if i == 0 or i == len(kube_nodes_info) - 1 or line[i] == "":
            i += 1
            continue
        node_l = splitNodeStr(line)
        all_nodes.append((node_l[0], node_l[5]))
        i += 1

    return all_nodes


def get_all_node_name():
    all_nodenames = []
    kube_nodes_info = subprocess.check_output('kubectl get nodes -o=wide', shell=True).decode('utf-8')
    kube_nodes_info = kube_nodes_info.split('\n')

    log("\n********************" +
        "\nThere are  %d nodes in total" % (len(kube_nodes_info) - 2) +
        "\n***********************\n")
    i = 0
    for line in kube_nodes_info:
        if i == 0 or i == len(kube_nodes_info) - 1 or line[i] == "":
            i += 1
            continue
        node_l = line.split("   ")
        all_nodenames.append(node_l[0])
        i += 1

    return all_nodenames


# get_all_node_name_ip()


def node_bind(node: Node, yaml_name: str):
    with open(yaml_name + ".yaml", 'r') as f:
        yaml_file = yaml.load(f, Loader=yaml.FullLoader)
        log(node.Name)
        yaml_file['spec']['template']['spec']['nodeName'] = str(node.Name)
        yaml_file['spec']['template']['spec']['volumes'][0]['hostPath']['path'] = \
            node.rootPath + "python-darknet-docker/test"

        # deploy_spec = yaml_file['spec'] #detail of a deploy
        # template_of_deploy = deploy_spec['template'] #template of deploy
        # pod_spec = template_of_deploy['spec'] #detail of pod
        # log(pod_spec['nodeName'])  #where to place pod 
        # pod_spec['nodeName'] = str(201)
        # log(pod_spec['nodeName'])

        changed_yaml_name = node.Name + get_r_code() + "-" + yaml_name
        changed_yaml_name = changed_yaml_name.replace("_", "-")
        yaml_file['metadata']['name'] = changed_yaml_name
        changed_yaml_name = path + node.Name + get_r_code() + "_" + yaml_name
        changed_yaml_name = changed_yaml_name.replace("-", "_")
        with open(changed_yaml_name, 'w+') as out:
            yaml.dump(yaml_file, out)

        cmd = "kubectl apply -f " + changed_yaml_name
        kube_apply_info = subprocess.check_output(cmd, shell=True).decode('utf-8')
        log(kube_apply_info)
    return changed_yaml_name


def deleteDeploy(deploy_file: str):
    cmd = "kubectl delete -f " + deploy_file
    kube_apply_info = subprocess.check_output(cmd, shell=True).decode('utf-8')
    log(kube_apply_info)
    os.remove(deploy_file)


def execSeq(seqs, yaml_name: str):
    last_file = ''
    for i in range(len(seqs)):
        seq = seqs[i]
        node = Node.nodeCreate(get_node_info(seq.get("name")))
        last_file = node_bind(node, yaml_name)
        log("\n exec:" + node.Name)
        time.sleep((int(seq.get("end")) - int(seq.get("start"))) / 5)
        if len(last_file) > 0:
            deleteDeploy(last_file)
            log("\n finish:" + node.Name)
    # if len(last_file) > 0:
    #     deleteDeploy(last_file)


def deleteAllDeploy():
    log("开始清除任务")
    for root, dic, files in os.walk(path):
        for file in files:
            cmd = "kubectl delete -f " + root + file
            kube_apply_info = subprocess.check_output(cmd, shell=True).decode('utf-8')
            log(kube_apply_info)
            os.remove(root + file)
    log("任务清除完毕")
# if __name__ == '__main__':
#     log("systeminfo_node  runs as main() function!")
#     get_all_node_name()
