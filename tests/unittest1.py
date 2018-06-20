# python3 ./tests/unittest1.py

import setup
import teos
import cleos
import sess
import eosf
import unittest
import json
import time

CONTRACT_NAME = "eosio.token"
setup.set_verbose(False)
cleos.dont_keosd()

class Test1(unittest.TestCase):

    def run(self, result=None):
        """ Stop after first error """      
        if not result.failures:
            super().run(result)


    @classmethod
    def setUpClass(cls):
        teos.node_reset()
        sess.init()


    def setUp(self):
        self.assertTrue(cleos.node_is_running(), "testnet failure")

    def test_05(self):
        global contract
        account = cleos.AccountLT()
        sess.wallet.import_key(account)
        
        print(sess.alice)
        print(sess.bob)
        print(sess.carol)
        print(account)

        contract = eosf.Contract(account, CONTRACT_NAME)
        self.assertTrue(not contract.error, "contract failure")

        print('test contract.code():')
        self.assertTrue(not contract.code().error)

        print('test contract.deploy():')
        self.assertTrue(contract.deploy())

        print('test contract.get_code():')
        self.assertTrue(not contract.code().error)

        print('test contract.push_action("create"):')
        self.assertTrue(not contract.push_action(
            "create", 
            '{"issuer":"' 
                + str(sess.account_eosio) 
                + '", "maximum_supply":"1000000000.0000 EOS", \
                "can_freeze":0, "can_recall":0, "can_whitelist":0}').error)

        print('test contract.push_action("issue"):')
        self.assertTrue(not contract.push_action(
            "issue", 
            '{"to":"' + str(sess.alice)
                + '", "quantity":"100.0000 EOS", "memo":"memo"}', \
                sess.account_eosio).error)

        print('test contract.push_action("transfer", sess.alice):')
        self.assertTrue(not contract.push_action(
            "transfer", 
            '{"from":"' 
                + str(sess.alice)
                + '", "to":"' + str(sess.carol)
                + '", "quantity":"25.0000 EOS", "memo":"memo"}', 
            sess.alice).error)

        time.sleep(1)
        
        print('test contract.push_action("transfer", sess.carol):')
        self.assertTrue(not contract.push_action(
            "transfer", 
            '{"from":"' 
                + str(sess.carol)
                + '", "to":"' + str(sess.bob)
                + '", "quantity":"13.0000 EOS", "memo":"memo"}', 
            sess.carol).error)

        print('test contract.push_action("transfer" sess.bob):')
        self.assertTrue(not contract.push_action(
            "transfer", 
            '{"from":"' 
                + str(sess.bob)
                + '", "to":"' 
                + str(sess.alice)
                + '", "quantity":"2.0000 EOS", "memo":"memo"}', 
            sess.bob).error)

        print('test contract.get_table("accounts", sess.alice):')
        t1 = contract.get_table("accounts", sess.alice)
        
        print('test contract.get_table("accounts", sess.bob):')
        t2 = contract.get_table("accounts", sess.bob)
        
        print('test contract.get_table("accounts", sess.carol):')
        t3 = contract.get_table("accounts", sess.carol)

        print('self.assertTrue(t1.json["rows"][0]["balance"] == "77.0000 EOS":')
        self.assertTrue(t1.json["rows"][0]["balance"] == '77.0000 EOS')
        
        print('self.assertTrue(t2.json["rows"][0]["balance"] == "11.0000 EOS":')
        self.assertTrue(t2.json["rows"][0]["balance"] == '11.0000 EOS')
        
        print('self.assertTrue(t3.json["rows"][0]["balance"] == "12.0000 EOS":')
        self.assertTrue(t3.json["rows"][0]["balance"] == '12.0000 EOS')

        print('test node.stop():')
        teos.node_stop()

        print("Test OK")




    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        teos.node_stop()


if __name__ == "__main__":
    unittest.main()