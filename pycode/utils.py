import json
import random
import time

def get_r_code():
    t = str(time.time())
    return t[len(t) - 5: len(t)] + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(
        random.randint(0, 9)) + str(
        random.randint(0, 9)) + str(random.randint(0, 9))


def nodeNameByL(l: str):
    with open("star_bind.config", "r") as file:
        tmpDict = json.loads(file.read())
    return tmpDict.get(l)


__log = ''
__log_screen = None


def log(*l):
    global __log
    global __log_screen
    for s in l:
        __log += str(s)
    __log += '\n'
    if __log_screen:
        __log_screen.logNotify()


def getLog():
    global __log
    return __log


def bindScreen(screen):
    global __log_screen
    __log_screen = screen


def unbindScreen():
    global __log_screen
    __log_screen = None
