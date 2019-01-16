'''
.. module:: eosfactory.core.vscode
    :platform: Unix, Darwin
    :synopsis: Default configuration items of a contract project.

.. moduleauthor:: Tokenika
'''

import json
import subprocess

import eosfactory.core.config as config
import eosfactory.core.logger as logger


def get_eosio_cpp_version():
    """Get the version code of *eosio-cpp*.
    """
    process = subprocess.run(
        [config.eosio_cpp(), "-version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE) 

    out = process.stdout.decode("ISO-8859-1").strip()
    err = process.stderr.decode("ISO-8859-1").strip()        

    if err:
        logger.ERROR('''
        Cannot determine the version of 'eosio-cpp'.
        The error message is 
        {}
        '''.format(err))

    return out.replace("eosio-cpp version ", "")


EOSIO_CPP_VERSION = "${eosio-cpp version}"
INCLUDES = [
        "${ROOT}/usr/opt/eosio.cdt/${eosio-cpp version}/include/eosiolib",
        "${ROOT}/usr/opt/eosio.cdt/${eosio-cpp version}/include",
        "${ROOT}/usr/opt/eosio.cdt/${eosio-cpp version}/include/libc",
        "${ROOT}/usr/opt/eosio.cdt/${eosio-cpp version}/include/libcxx",
        "${workspaceFolder}"
    ]


LIBS = [
]
COMPILER_OPTIONS = [
]
TASKS = '''
{
    "version": "2.0.0",   
    "tasks": [
        {
            "label": "Compile",
            "type": "shell",
            "windows": {
                "options": {
                    "shell": {
                        "executable": "bash.exe",
                        "args": [
                            "-c"
                        ]
                    }
                },
                "command": "mkdir -p build; python3 -m eosfactory.utils.build '${workspaceFolder}' --compile"
            },
            "osx": {
                "command": "mkdir -p build; python3 -m eosfactory.utils.build '${workspaceFolder}' --compile"
            },
            "linux": {
                "command": "mkdir -p build; python3 -m eosfactory.utils.build '${workspaceFolder}' --compile"
            },
            "presentation": {
                "reveal": "always",
                "panel": "dedicated"
            },
            "problemMatcher": [
            ]
        },
        {
            "label": "Build",
            "type": "shell",
            "windows": {
                "options": {
                    "shell": {
                        "executable": "bash.exe",
                        "args": [
                            "-c"
                        ]
                    }
                },
                "command": "mkdir -p build; python3 -m eosfactory.utils.build '${workspaceFolder}'"        
            },
            "osx": {
                "command": "mkdir -p build; python3 -m eosfactory.utils.build '${workspaceFolder}'"
            },
            "linux": {
                "command": "mkdir -p build; python3 -m eosfactory.utils.build '${workspaceFolder}'"
            },
            "problemMatcher": [],
            "presentation": {
                "reveal": "always",
                "panel": "dedicated"
            },
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "problemMatcher": [
            ]
        },
        {
            "label": "Test",
            "type": "shell",
            "windows": {
                "options": {
                    "shell": {
                        "executable": "bash.exe",
                        "args": [
                            "-c"
                        ]
                    }
                },            
                "command": "python3 ./tests/test1.py"
            },
            "osx": {
                "command": "python3 ./tests/test1.py"
            },
            "linux": {
                "command": "python3 ./tests/test1.py"
            },
            "presentation": {
                "reveal": "always",
                "panel": "dedicated"
            },
            "problemMatcher": [
            ]
        },
        {
            "label": "Unittest",
            "type": "shell",
            "windows": {
                "options": {
                    "shell": {
                        "executable": "bash.exe",
                        "args": [
                            "-c"
                        ]
                    }
                },            
                "command": "python3 ./tests/unittest1.py"
            },
            "osx": {
                "command": "python3 ./tests/unittest1.py"
            },
            "linux": {
                "command": "python3 ./tests/unittest1.py"
            },
            "presentation": {
                "reveal": "always",
                "panel": "dedicated"
            },
            "problemMatcher": [
            ]
        },
        {
            "label": "EOSIO API",
            "type": "shell",
            "windows": {
                "options": {
                    "shell": {
                        "executable": "bash.exe",
                        "args": [
                            "-c"
                        ]
                    }
                },            
                "command": "explorer.exe"
            },
            "osx": {
                "command": "open"
            },
            "linux": {
                "command": "sensible-browser"
            },
            "args": [
                "https://developers.eos.io/eosio-cpp/reference"
            ],
            "presentation": {
                "reveal": "always",
                "panel": "dedicated"
            },
            "problemMatcher": [
            ]
        }
    ]
}
'''

def c_cpp_properties():
    eosio_cpp_version = get_eosio_cpp_version()
    retval = """
{
    "configurations": [
        {
            "includePath": %s,
            "libs": %s,
            "compilerOptions": %s,
            "defines": [],
            "intelliSenseMode": "clang-x64",
            "browse": {
                "path": %s,
                "limitSymbolsToIncludedHeaders": true,
                "databaseFilename": ""
            }
        }
    ],
    "version": 4
}
""" % (
    json.dumps(INCLUDES, indent=4),
    json.dumps(LIBS, indent=4),
    json.dumps(COMPILER_OPTIONS, indent=4),
    json.dumps(INCLUDES, indent=4))

    return retval.replace(EOSIO_CPP_VERSION, eosio_cpp_version)

    