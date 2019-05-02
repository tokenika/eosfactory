'''
.. module:: eosfactory.core.vscode
    :platform: Unix, Darwin
    :synopsis: Default configuration items of a contract project.

.. moduleauthor:: Tokenika
'''

import json
import argparse
import eosfactory.core.config as config


def get_includes():
    includes = config.eosio_cpp_includes()
    retval = []
    root = config.wsl_root()
    for include in includes:
        retval.append(root + include)

    retval.append("${workspaceFolder}")
    retval.append("${workspaceFolder}/include")

    return retval


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
                "command": "mkdir -p build; python3 -m eosfactory.build '${workspaceFolder}' --compile"
            },
            "osx": {
                "command": "mkdir -p build; python3 -m eosfactory.build '${workspaceFolder}' --compile"
            },
            "linux": {
                "command": "mkdir -p build; python3 -m eosfactory.build '${workspaceFolder}' --compile"
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
                "command": "mkdir -p build; python3 -m eosfactory.build '${workspaceFolder}'"        
            },
            "osx": {
                "command": "mkdir -p build; python3 -m eosfactory.build '${workspaceFolder}'"
            },
            "linux": {
                "command": "mkdir -p build; python3 -m eosfactory.build '${workspaceFolder}'"
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
                "https://developers.eos.io/"
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
    includes = get_includes()
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
    json.dumps(includes, indent=4),
    json.dumps(LIBS, indent=4),
    json.dumps(COMPILER_OPTIONS, indent=4),
    json.dumps(includes, indent=4))

    return retval


def main(c_cpp_properties_path=None):
    if c_cpp_properties_path:
        config.update_eosio_cpp_includes(c_cpp_properties_path)
    else:
        print(c_cpp_properties())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--c_cpp_prop_path", default="")
    args = parser.parse_args()
    main(args.c_cpp_prop_path)