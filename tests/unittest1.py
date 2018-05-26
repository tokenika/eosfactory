# python3 ./tests/test1.py

import unittest
import json
import pyteos
import node
import sess
import eosf
import warnings

pyteos.set_verbose(False)

class Test1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass
        
    def setUp(self):
        pass

    def run(self, result=None):
        """ Stop after first error """      
        if not result.failures:
            super().run(result)
    
    def test_00_node_reset(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.assertTrue(node.reset(), "node reset")
        self.assertTrue(sess.setup(), "session setup")

    def test_01_contract(self):
        c = eosf.Contract("eosio.token")
        self.assertFalse(c.error, "Contract")

        self.assertTrue(c.get_code(), "get_code")
        self.assertTrue(c.deploy(), "deploy")
        self.assertTrue(c.get_code(), "get_code")

        self.assertTrue(
            c.push_action(
            "create", 
            '{"issuer":"eosio", "maximum_supply":"1000000000.0000 EOS", \
                "can_freeze":0, "can_recall":0, "can_whitelist":0}'), 
            "push_action create")

        self.assertTrue(
            c.push_action(
            "issue", 
            '{"to":"alice", "quantity":"100.0000 EOS", \
                "memo":"issue 100.0000 EOS"}', 
            sess.eosio), 
            "push_action issue")

        self.assertTrue(
            c.push_action(
            "transfer", 
            '{"from":"alice", "to":"carol", "quantity":"25.0000 EOS", \
                "memo":"transfer 25.0000 EOS"}', 
            sess.alice), 
            "push_action transfer")

        x = c.push_action(
            "transfer", 
            '{"from":"carol", "to":"bob", "quantity":"13.0000 EOS", \
                "memo":"transfer 13.0000 EOS"}', 
            sess.carol)
        self.assertTrue(x, "push_action transfer")
        
        self.assertTrue(
            c.push_action(
            "transfer", 
            '{"from":"bob", "to":"alice", "quantity":"2.0000 EOS", \
                "memo":"transfer 2.0000 EOS"}', 
            sess.bob), 
            "push_action transfer")

        t1 =  c.get_table("accounts", sess.alice)
        self.assertFalse(t1.error, "get_table alice")
        t2 = c.get_table("accounts", sess.bob)
        self.assertFalse(t2.error, "get_table bob")
        t3 = c.get_table("accounts", sess.carol)
        self.assertFalse(t2.error, "get_table carol")

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