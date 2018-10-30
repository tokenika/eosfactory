def wslMapLinuxWindows(path):
    if not path or path.find("/mnt/") == -1:
        return path
    path = path[5].upper() + ":" + path[6:]
    path = path.replace("/", r"\\")
    return path


def wslMapWindowsLinux(path):
    if path.find(":\\") == -1:
        return path
    path = path.replace("\\", "/")
    drive = path[0]
    return path.replace(drive + ":/", "/mnt/" + drive.lower() + "/")


import os
import re
import sys
from textwrap import dedent

def save_code():
    '''Copy the current file without heredoc comments.
    '''
    if len(sys.argv) < 2 or sys.argv[1] != "-s" and sys.argv[1] != "--save":
        return

    source = os.path.abspath(__file__)
    print(source)
    result = os.path.splitext(source)[0] + ".1.py"

    data = open(source, "r").read()
    prog = re.compile(r'\'\'\'.*?\'\'\'', flags=re.DOTALL)

    open(result, "w").write(re.sub(prog, '', data))
    exit()


def heredoc(message):
    message = dedent(message).strip()
    message.replace("<br>", "\n")
    return message