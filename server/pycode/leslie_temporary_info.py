import subprocess


def get_node_info(node_name):
    cmd = 'kubectl describe node '+ node_name
    kube_nodes_info = subprocess.check_output(cmd, shell=True).decode('utf-8')
    return kube_nodes_info
