from pycode.leslie_sysinfo_code import get_all_node_name_ip


def sname2ip(sname):
    nodes = get_all_node_name_ip()
    # todo 映射节点名和卫星名
    return nodes[0][1]

print(sname2ip("11"))