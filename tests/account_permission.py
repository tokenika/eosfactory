import sys
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG])

def test():
    SCENARIO('''
    Initialize the token and run a couple of transfers between different accounts.
    ''')
    reset()
    create_master_account("master")

    COMMENT('''
    Build & deploy the contract:
    ''')
    create_account("host", master)
    contract = Contract(host, "02_eosio_token")
    contract.build(force=False)
    contract.deploy()

    COMMENT('''
    Create test accounts:
    ''')
    create_account("alice", master)
    create_account("bob", master)
    create_account("carol", master)

    COMMENT('''
    Initialize the token and send some tokens to one of the accounts:
    ''')

    COMMENT('''
    `set_permission` command:
    ''')        
    alice.set_permission(Permission.ACTIVE, 
        {
            "threshold": 1,
            "keys": 
                [
                    {
                        "key": host.owner(),
                        "weight": 1
                    }
                ],
            "accounts": 
                [
                    {
                        "permission":
                            {
                                "actor": host,
                                "permission": "eosio.code"
                            },
                        "weight":1
                    }
                ]
        }
    )

    stop()


if __name__ == "__main__":
    test()
