#!/usr/bin/env python3
"""Install EOSFactory"""

import argparse
import eosfactory.core.config as config


def install():
    wsl_root = config.wsl_root()
    if wsl_root:
        print("""
The root is the Windows Subsystem Linux is
'{}'
        """.format(wsl_root))
    
    config.set_contract_workspace_dir()
        
parser = argparse.ArgumentParser(description="""
""")

if __name__ == '__main__':
        install()