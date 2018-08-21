import unittest
from  eosfactory import *

set_throw_error(False)
_ = Logger([Verbosity.TRACE, Verbosity.OUT, Verbosity.DEBUG])

CONTRACT_NAME = "_e4b2ffc804529ce9c6fae258197648cc2"

class Test(unittest.TestCase):

    def run(self, result=None):
        super().run(result)

    @classmethod
    def setUpClass(cls):
        print()

    def setUp(self):
        restart()
        set_is_testing_errors(False)
        set_throw_error(True)

    def test_contract_template(self):
        reset([Verbosity.INFO]) 
        
        wallet = Wallet()
        account_master_create("account_master")
        set_throw_error(False)
        set_is_testing_errors()

        _.SCENARIO('''
        This is a test of creating a contract from a pre-defined template,
        then building and deploying it.
        Finnally, a couple of basic methods are tested.
        ''')

        contract_dir = contract_workspace_from_template(
                CONTRACT_NAME, remove_existing=True, visual_studio_code=False)

        account_create("account_host", account_master)
        account_create("account_alice", account_master)
        account_create("account_carol", account_master)

        contract = Contract(account_host, contract_dir)
        contract.build()
        contract.deploy()

        account_host.push_action(
            "hi", {"user":account_alice}, account_alice)

        account_host.push_action(
            "hi", {"user":account_carol}, account_carol)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        stop()

if __name__ == "__main__":
    unittest.main()