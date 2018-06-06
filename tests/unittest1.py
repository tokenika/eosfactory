# python3 ./tests/unittest1.py

import unittest
import warnings
import json
import node
import sess
from eosf import *

CONTRACT_NAME = "eosio.token"
set_verbose(False)

class Test1(unittest.TestCase):

    def run(self, result=None):
        """ Stop after first error """      
        if not result.failures:
            super().run(result)


    @classmethod
    def setUpClass(cls):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            node.reset()
        sess.init()
        contract = Contract(CONTRACT_NAME)
        contract.deploy()


    def setUp(self):
        self.assertTrue(node.is_running(), "testnet failure")
        self.contract = Contract(CONTRACT_NAME)
        self.assertTrue(self.contract.is_created(), "contract failure")
        self.assertTrue(self.contract.is_deployed(), "deployment failure")


    def test_01(self):
        self.assertTrue(
            self.contract.push_action(
            "create", 
            '{"issuer":"eosio", "maximum_supply":"1000000000.0000 EOS", \
                "can_freeze":0, "can_recall":0, "can_whitelist":0}'), 
            "push_action create")

        self.assertTrue(
            self.contract.push_action(
            "issue", 
            '{"to":"alice", "quantity":"100.0000 EOS", \
                "memo":"issue 100.0000 EOS"}', 
            sess.eosio), 
            "push_action issue")


    def test_02(self):
        self.assertTrue(
            self.contract.push_action(
            "transfer", 
            '{"from":"alice", "to":"carol", "quantity":"25.0000 EOS", \
                "memo":"transfer 25.0000 EOS"}', 
            sess.alice), 
            "push_action transfer")

        self.assertTrue(
            self.contract.push_action(
            "transfer", 
            '{"from":"carol", "to":"bob", "quantity":"13.0000 EOS", \
                "memo":"transfer 13.0000 EOS"}', 
            sess.carol),
            "push_action transfer")
        
        self.assertTrue(
            self.contract.push_action(
            "transfer", 
            '{"from":"bob", "to":"alice", "quantity":"2.0000 EOS", \
                "memo":"transfer 2.0000 EOS"}', 
            sess.bob), 
            "push_action transfer")


    def test_03(self):   
        t1 = self.contract.get_table("accounts", sess.alice)
        self.assertFalse(t1.error, "get_table alice")

        t2 = self.contract.get_table("accounts", sess.bob)
        self.assertFalse(t2.error, "get_table bob")

        t3 = self.contract.get_table("accounts", sess.carol)
        self.assertFalse(t2.error, "get_table carol")

        self.assertEqual(
            t1.json["rows"][0]["balance"], "77.0000 EOS")

        self.assertEqual(
            t2.json["rows"][0]["balance"], "11.0000 EOS")

        self.assertEqual(
            t3.json["rows"][0]["balance"], "12.0000 EOS")


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        node.stop()


if __name__ == "__main__":
    unittest.main()