def wslMapLinuxWindows(path):
    if not path or path.find("/mnt/") == -1:
        return path
    path = path[5].upper() + ":" + path[6:]
    path = path.replace("/", r"\\")
    return path


def wslMapWindowsLinux(path):
    if path.find(":") == -1:
        return path
    path = path.replace("\\", "/")
    drive = path[0]
    return path.replace(drive + ":/", "/mnt/" + drive.lower() + "/")


from textwrap import dedent

def heredoc(message):
    message = dedent(message).strip()
    message.replace("<br>", "\n")
    return message