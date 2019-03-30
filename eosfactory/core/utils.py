import eosfactory.core.errors as errors

def wslMapLinuxWindows(path, back_slash=True):
    if not path or path.find("/mnt/") != 0:
        return path
    path = path[5].upper() + ":" + path[6:]
    if back_slash:
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


def spawn(
        command_line, error_message='', shell=False, raise_exception=True):
    import subprocess
    stdout = None
    stderr = None
    try:
        p = subprocess.run(
            command_line,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        stdout = p.stdout.decode("ISO-8859-1").strip()
        stderr = p.stderr.decode("ISO-8859-1").strip()          
    except Exception as e:
        stderr = str(e)

    if raise_exception:
        if stderr:
            raise errors.Error('''
    {}

    command line:
    =============
    {}

    error message:
    ==============
    {}
            '''.format(error_message, " ".join(command_line), stderr))

        return stdout
    else:
        return (stdout, stderr)


def uname(options=None):
    command_line = ['uname']
    if options:
        command_line.append(options)

    return spawn(command_line)


def is_windows_ubuntu():
    resp = uname("-v")
    return resp.find("Microsoft") != -1


def which(file_path):
    return spawn("which {}".format(file_path), shell=True)