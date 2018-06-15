#!/usr/bin/python3


_is_verbose = True
_suppress_error_msg = False

def set_verbose(is_verbose):
    """
    If set `False`, print error messages only.
    """
    global _is_verbose
    _is_verbose = is_verbose


def is_verbose():
    global _is_verbose
    return _is_verbose


def set_suppress_error_msg(suppress_error_msg):
    global _suppress_error_msg
    _suppress_error_msg = suppress_error_msg


def is_suppress_error_msg():
    global _suppress_error_msg
    return _suppress_error_msg    


def output(msg):
    if _is_verbose:
        print("#  " + msg.replace("\n", "\n#  "))


class Setup:
    """ Interface to the json configuration file.

    The configuration file is expected in the same folder as the current file.
    """
    __setupFile = os.path.dirname(os.path.abspath(__file__)) + "/../teos/config.json"
    __CLEOS_EXE = "cleos_executable"    
    __TEOS_EXE = "teos_executable"
    __CLEOS_ENV = "EOSIO_SOURCE_DIR"
    __TEOS_ENV = "eosf"

    __review = False
    cleos_exe = ""
    teos_exe = ""

    def __init__(self):

        with open(self.__setupFile) as json_data:
            setup_json = json.load(json_data)

        if not self.cleos_exe:
            try:
                path_to_cleos = os.path.dirname(os.environ[__CLEOS_ENV]) \
                    + "/build/programs/cleos"
                if os.path.isfile(path_to_cleos):
                    self.cleos_exe = os.path.realpath(path_to_cleos)
            except:
                pass

        if not self.teos_exe:
            try:
                path_to_teos = os.path.dirname(os.environ[__TEOS_ENV]) 
                if os.path.isfile(path_to_teos):
                    self.teos_exe = os.path.realpath(path_to_cleos)
            except:
                pass            

        if not self.teos_exe:
            path_to_teos = os.path.dirname(os.path.abspath(__file__)) \
                + "/../teos/build/teos/teos"
            if os.path.isfile(path_to_teos):
                self.teos_exe = os.path.realpath(path_to_teos)

        if not self.teos_exe:
            try:
                if os.path.isfile(self.__setupFile):
                    path_to_teos = os.path.dirname(os.path.abspath(__file__)) \
                            + setup_json[self.__TEOS_EXE]
                    if os.path.isfile(path_to_teos):
                        self.teos_exe = os.path.realpath(path_to_teos)
            except:
                pass

        if not self.cleos_exe:
            print('''ERROR in setup.py!
Do not know the cleos executable!
It is expected to be the environment variable:
{0}
or
it is expected to be in the config file named
{1}
as {{"{2}":"absolute-path-to-eos-repository"}}
            '''.format(
                    __CLEOS_ENV,                 
                    os.path.realpath(self.__setupFile),
                    self.__CLEOS_EXE,
                    )
            
            )

        if not self.teos_exe:
            print('''ERROR in pyteos.py!
Do not know the teos executable!
It is expected to be the environment variable:
{0}
it is expected to be in the config file named
{1}
as {{"{2}":"absolute-path-to-teos-executable"}}
                '''.format(
                    __TEOS_ENV,                 
                    os.path.realpath(self.__setupFile),
                    self.__TEOS_EXE,
                    )
                )

