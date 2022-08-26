#!/usr/bin/python3
import subprocess
from time import sleep

from leslie_sysinfo_code import get_all_node_name
from hwy_schedule_algorithm import *
import leslie_temporary_info
# from utils import *


def yolo():
    all_nodenames = get_all_node_name()
    # log("\nHere are all nodes' name", all_nodenames, "\n")

    selected_node = select_one_node(all_nodenames, {})
    log("\nnode ", selected_node.Name, " was selected!\n")
    node_bind(selected_node, "yolo_detect")

    # seqs = getSequence(20, 20, 10)
    # log("\n" + str(seqs))
    # execSeq(seqs, "yolo_detect")

    # node_bind(selected_node, "observation")

# if __name__ == '__main__':
    # main()
    # deleteAllDeploy()
