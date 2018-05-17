# python3 ./tests/test1.py

import unittest
import node
import sess
from eosf import *

class Test1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import pyteos
        import node
        import sess
        import eosf
        import json

        pyteos.set_verbose(False)

    def setUp(self):
        pass

    """

    """
    def run(self, result=None):
        """ Stop after first error """      
        if not result.failures:
            super().run(result)
    

    def test_00_node_reset(self):
        x = node.reset()
        self.assertFalse(x.error)
        x = node.info()
        self.assertTrue("last_irreversible_block_id" in x.json.keys())
        x = sess.Init()
        self.assertFalse(x.error)

    def test_01_contract(self):
        c = Contract("eosio.token")
        self.assertFalse(c.error, "Contract")
        x = c.get_code()
        self.assertTrue(x, "get_code")
        x = c.deploy()
        self.assertTrue(x, "deploy")
        x = c.get_code()
        self.assertTrue(x, "get_code") 

        x = c.push_action(
            "create", 
            '{"issuer":"eosio", "maximum_supply":"1000000000.0000 EOS", \
                "can_freeze":0, "can_recall":0, "can_whitelist":0}') 
        self.assertTrue(x, "push_action create")

        x = c.push_action(
            "issue", 
            '{"to":"alice", "quantity":"100.0000 EOS", \
                "memo":"issue 100.0000 EOS"}', 
            sess.eosio)
        self.assertTrue(x, "push_action issue")

        x = c.push_action(
            "transfer", 
            '{"from":"alice", "to":"carol", "quantity":"25.0000 EOS", \
                "memo":"transfer 25.0000 EOS"}', 
            sess.alice)
        self.assertTrue(x, "push_action transfer")

        x = c.push_action(
            "transfer", 
            '{"from":"carol", "to":"bob", "quantity":"13.0000 EOS", \
                "memo":"transfer 13.0000 EOS"}', 
            sess.carol)
        self.assertTrue(x, "push_action transfer")
        
        x = c.push_action(
            "transfer", 
            '{"from":"bob", "to":"alice", "quantity":"2.0000 EOS", \
                "memo":"transfer 2.0000 EOS"}', 
            sess.bob)
        self.assertTrue(x, "push_action transfer")

        t1 =  c.get_table("accounts", sess.alice)
        self.assertFalse(t1.error, "get table accounts")

        t2 = c.get_table("accounts", sess.bob)
        self.assertFalse(t2.error, "get table accounts")

        t3 = c.get_table("accounts", sess.carol)
        self.assertFalse(t3.error, "get table accounts")

        self.assertEqual(
            t1.json["rows"][0]["balance"], "77.0000 EOS")
        self.assertEqual(
            t2.json["rows"][0]["balance"], "11.0000 EOS")
        self.assertEqual(
            t3.json["rows"][0]["balance"], "12.0000 EOS")


    def test_99_node_stop(self):
        x = node.stop()
        self.assertTrue(x)


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        s = node.stop()


if __name__ == "__main__":
    unittest.main()