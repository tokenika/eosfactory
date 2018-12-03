import unittest
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE, Verbosity.DEBUG])

class Test(unittest.TestCase):

    def run(self, result=None):
        super().run(result)


    @classmethod
    def setUpClass(cls):
        SCENARIO('''
        Create a contract from template, then build and deploy it.
        Also, initialize the token and run the `set_permission` command.
        ''')
        reset()
        create_master_account("master")

        COMMENT('''
        Create test accounts:
        ''')
        create_account("alice", master)

    def setUp(self):
        pass

    def test_01(self):
        COMMENT('''
        Create, build and deploy the contract:
        ''')
        create_account("host", master)

        contract = Contract(host, "02_eosio_token")
        # contract.build()
        contract.deploy()

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

    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
