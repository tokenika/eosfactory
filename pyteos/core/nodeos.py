import os
import subprocess
import time
import core.config as config
import core.errors as errors

def get_pid(name=None):
    """Return process ids found by (partial) name or regex.

    >>> get_process_id('kthreadd')
    [2]
    >>> get_process_id('watchdog')
    [10, 11, 16, 21, 26, 31, 36, 41, 46, 51, 56, 61]  # ymmv
    >>> get_process_id('non-existent process')
    []
    """    
    if not name:
        name = config.node_exe_name()

    child = subprocess.Popen(
        ['pgrep', '-f', name], stdout=subprocess.PIPE, shell=False)
    response = child.communicate()[0]
    return [int(pid) for pid in response.split()]


def node_is_running():
    return not get_pid()


def DaemonStop():
    pid = get_pid()
    count = 10
    if pid:
        os.system("pkill " + str(pid[0]))
        while pid and count > 0:
            time.sleep(1)
            pid = get_pid()
            count = count -1

    if count <= 0:
        raise errors.Error('''
Failed to kill {}. Pid is {}.
    '''.format(config.node_exe_name(), pid[0])
    )
