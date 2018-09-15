import enum
import re
import inspect

from textwrap import dedent
from termcolor import cprint, colored

class Verbosity(enum.Enum):
    COMMENT = ['green', None, []]
    INFO = ['blue', None, []]
    TRACE = ['cyan', None, []]
    ERROR = ['red', None, ['reverse']]
    ERROR_TESTING = ['green', None, ['reverse']]
    OUT = [None, None, []]
    DEBUG = ['yellow', None, []]
    NONE = None


__verbosity = [Verbosity.TRACE, Verbosity.OUT, Verbosity.DEBUG]
def verbosity(verbosity):
    global __verbosity
    __verbosity = verbosity


def COMMENT(msg):
    frame = inspect.stack()[1][0]
    test_name = inspect.getframeinfo(frame).function
    color = Verbosity.COMMENT.value
    cprint(
        "\n###  " + test_name + ":\n" + condition(msg) + "\n",
        color[0], color[1], attrs=color[2])


def SCENARIO(msg):
    COMMENT(msg)


def TRACE(msg, translate=True, verbosity=None):
    msg = condition(msg, translate)
    if msg and (Verbosity.TRACE in verbosity if verbosity else __verbosity):
        color = Verbosity.TRACE.value
        cprint(msg, color[0], color[1], attrs=color[2])


def INFO(msg, translate=True, verbosity=None):
    v = verbosity if verbosity else __verbosity
    if msg and (
            Verbosity.TRACE in v or Verbosity.INFO in v
        ):
        color = Verbosity.INFO.value
        cprint(condition(msg, translate), color[0], color[1], attrs=color[2])        

def OUT(msg, translate=True, verbosity=None):
    if msg and (Verbosity.OUT in verbosity if verbosity else __verbosity):
        color = Verbosity.OUT.value
        msg = condition(msg, translate)
        cprint(msg, color[0], color[1], attrs=color[2])

__debug_buffer = ""
def DEBUG(msg=None, translate=True, verbosity=None):
    if not msg:
        return __debug_buffer
    
    msg = condition(msg, translate)
    global __debug_buffer
    __debug_buffer = msg

    if msg and (Verbosity.DEBUG in verbosity if verbosity else __verbosity):
        color = Verbosity.DEBUG.value
        cprint(msg, color[0], color[1], attrs=color[2])


__is_testing_errors = False
def set_is_testing_errors(status=True):
    '''Changes the color of the ``ERROR`` logger printout.

    Makes it less alarming.
    '''
    global _is_testing_errors
    if status:
        __is_testing_errors = True
    else:
        __is_testing_errors = False


def error(msg, translate=True):
    color = Verbosity.ERROR_TESTING.value \
        if __is_testing_errors else Verbosity.ERROR.value
    return colored(
        "ERROR:\n{}".format(condition(msg, translate)),  
        color[0], color[1], attrs=color[2])


def ERROR(msg, translate=True, verbosity=None):
    if not verbosity:
        cprint(error(msg, translate))


def condition(message, translate=True):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    message = dedent(message).strip()
    message.replace("<br>", "\n")
    # if translate:
    #    message = efman.accout_names_2_object_names(message)

    return message
