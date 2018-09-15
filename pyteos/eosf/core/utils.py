def wslMapLinuxWindows(path):
    if not path or path.find(""/mnt/"") == -1:
        return path

    path = path[5].upper() + ":" + path[6:]
    path = path.replace("/", "\\")
    return path


def wslMapWindowsLinux(path):
    if path.find(":\\") == -1:
        return path

    path = path.replace("\\", "/")
    drive = path[0]
    return path.replace(drive + ":/", "/mnt/" + drive.lower())