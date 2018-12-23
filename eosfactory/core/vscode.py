'''
.. module:: eosfactory.core.vscode
    :platform: Unix, Darwin
    :synopsis: Default configuration items of a contract project.

.. moduleauthor:: Tokenika
'''

import json

INCLUDES = [
        "${ROOT}/usr/local/eosio.cdt/include/eosiolib",
        "${ROOT}/usr/local/eosio.cdt/include",
        "${ROOT}/usr/local/eosio.cdt/include/libc",
        "${ROOT}/usr/local/eosio.cdt/include/libcxx",
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
                "command": "mkdir -p build; python3 -m eosfactory.core.build '${workspaceFolder}' --compile"
            },
            "osx": {
                "command": "mkdir -p build; python3 -m eosfactory.core.build '${workspaceFolder}' --compile"
            },
            "linux": {
                "command": "mkdir -p build; python3 -m eosfactory.core.build '${workspaceFolder}' --compile"
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
                "command": "mkdir -p build; python3 -m eosfactory.core.build '${workspaceFolder}'"        
            },
            "osx": {
                "command": "mkdir -p build; python3 -m eosfactory.core.build '${workspaceFolder}'"
            },
            "linux": {
                "command": "mkdir -p build; python3 -m eosfactory.core.build '${workspaceFolder}'"
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

c_cpp_properties = """
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

