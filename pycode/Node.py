import json

class Node:
    def __init__(self, data: dict) -> None:
        super().__init__()
        self.Name = data.get("Name")
        self.Roles = data.get("Roles")
        self.Labels = data.get("Labels")
        self.Annotations = data.get("Annotations")
        self.CreationTimestamp = data.get("CreationTimestamp")
        self.Taints = data.get("Taints")
        self.Unschedulable = data.get("Unschedulable")
        self.Lease = data.get("Lease")
        self.Conditions = data.get("Conditions")
        self.Addresses = data.get("Addresses")
        self.Capacity = data.get("Capacity")
        self.Allocatable = data.get("Allocatable")
        self.SystemInfo = data.get("System Info")
        self.PodCIDR = data.get("PodCIDR")
        self.PodCIDRs = data.get("PodCIDRs")
        self.NonterminatedPods = data.get("Non-terminated Pods")
        self.AllocatedResources = data.get("Allocated resources")
        self.Events = data.get("Events")
        with open("node_info_static.config","r") as file:
            try:
                self.rootPath = json.loads(file.read()).get(self.Name).get("rootPath")
            except Exception:
                print(Exception)






    def canUse(self):
        if self.Taints:
            return True
        else:
            return False


def info2dict(info: str):
    data = {}
    lines = info.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.find(":") == -1:
            i += 1
            continue
        if numOfContent(lines[i]) == 0 \
                and ((i + 1 < len(lines) and (numOfContent(lines[i + 1]) == 0
                                              or numOfContent(lines[i + 1]) == -1)) or i + 1 == len(lines)):
            cut = line.find(":")
            data.update({line[0:cut]: clearSpace(line[cut + 1:len(line)])})
        elif numOfContent(lines[i]) == 0 and i + 1 < len(lines) and numOfContent(lines[i + 1]) > 2:
            cut = line.find(":")
            name = line[0:line.find(":")]
            if name == "Labels" or name == "Annotations":
                subs = [clearSpace(line[cut + 1:len(line)])]
                for j in range(i + 1, len(lines)):
                    subline = lines[j]
                    if numOfContent(subline) != 0:
                        subs.append(clearSpace(subline))
                    else:
                        i = j - 1
                        break
                data.update({name: subs})
        elif numOfContent(lines[i]) == 0 and i + 1 < len(lines) and numOfContent(lines[i + 1]) <= 2 and numOfContent(
                lines[i + 1]) > 0:
            name = line[0:line.find(":")]
            if name == "Conditions" or name == "Non-terminated Pods" or name == "Allocated resources":
                subs = ""
                for j in range(i + 1, len(lines)):
                    subline = lines[j]
                    if numOfContent(subline) != 0:
                        subs += subline + "\n"
                    else:
                        i = j - 1
                        break
                data.update({name: subs})
            else:
                subdict = {}
                for j in range(i + 1, len(lines)):
                    subline = lines[j]
                    if numOfContent(subline) != 0:
                        cut = subline.find(":")
                        subdict.update({clearSpace(subline[0:cut]): clearSpace(subline[cut + 1:len(subline)])})
                    else:
                        i = j - 1
                        break
                data.update({name: subdict})
        i += 1
    return data


def clearSpace(s: str):
    cut = numOfContent(s)
    return s[cut:len(s)]


# the position of the first non-space char
def numOfContent(line: str):
    num = 0
    for c in line:
        if c == ' ':
            num += 1
            continue
        return num
    return -1


def nodeCreate(info: str):
    return Node(info2dict(info))
