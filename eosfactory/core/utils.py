
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


def heredoc(message):
    from textwrap import dedent
    message = dedent(message).strip()
    message.replace("<br>", "\n")
    return message


def process(command_line, error_message='', shell=False):
    import subprocess
    p = subprocess.run(
        command_line,
        shell=shell,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE) 

    stdout = p.stdout.decode("ISO-8859-1").strip()
    stderr = p.stderr.decode("ISO-8859-1").strip()        

    if stderr:
        logger.ERROR('''
{}

command line:
=============
{}

error message:
==============
{}
        '''.format(error_message, " ".join(command_line), stderr))

    return stdout