# python3 ./tests/unittest2.py

import unittest
import warnings
import json
import node
import sess
from eosf import *

set_verbose(False)

class Test1(unittest.TestCase):

    CONTRACT_NAME = "tic.tac.toe"

    def run(self, result=None):
        """ Stop after first error """      
        if not result.failures:
            super().run(result)


    @classmethod
    def setUpClass(cls):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            node.reset()
        sess.setup()
        contract = Contract(cls.CONTRACT_NAME)
        contract.deploy()


    def setUp(self):
        self.assertTrue(node.is_running(), "testnet failure")
        self.contract = Contract(self.CONTRACT_NAME)
        self.assertTrue(self.contract.is_created(), "contract failure")
        self.assertTrue(self.contract.is_deployed(), "deployment failure")


    def test_01(self):
        self.assertTrue(
            self.contract.push_action(
            "create", 
            '{"challenger":"alice", "host":"bob"}',
            sess.bob), 
            "push_action create")

        t = self.contract.get_table("games", sess.bob)
        self.assertFalse(t.error, "get_table")

        self.assertEqual(t.json["rows"][0]["board"][0], "0")
        self.assertEqual(t.json["rows"][0]["board"][1], "0")
        self.assertEqual(t.json["rows"][0]["board"][2], "0")
        self.assertEqual(t.json["rows"][0]["board"][3], "0")
        self.assertEqual(t.json["rows"][0]["board"][4], "0")
        self.assertEqual(t.json["rows"][0]["board"][5], "0")
        self.assertEqual(t.json["rows"][0]["board"][6], "0")
        self.assertEqual(t.json["rows"][0]["board"][7], "0")
        self.assertEqual(t.json["rows"][0]["board"][8], "0")


    def test_02(self):
        self.assertTrue(
            self.contract.push_action(
            "move", 
            '{"challenger":"alice", "host":"bob", "by":"bob", "mvt":{"row":0, "column":0} }',
            sess.bob), 
            "push_action move 1")

        self.assertTrue(
            self.contract.push_action(
            "move", 
            '{"challenger":"alice", "host":"bob", "by":"alice", "mvt":{"row":1, "column":1} }',
            sess.alice), 
            "push_action move 2")

        t = self.contract.get_table("games", sess.bob)
        self.assertFalse(t.error, "get_table")

        self.assertEqual(t.json["rows"][0]["board"][0], "1")
        self.assertEqual(t.json["rows"][0]["board"][1], "0")
        self.assertEqual(t.json["rows"][0]["board"][2], "0")
        self.assertEqual(t.json["rows"][0]["board"][3], "0")
        self.assertEqual(t.json["rows"][0]["board"][4], "2")
        self.assertEqual(t.json["rows"][0]["board"][5], "0")
        self.assertEqual(t.json["rows"][0]["board"][6], "0")
        self.assertEqual(t.json["rows"][0]["board"][7], "0")
        self.assertEqual(t.json["rows"][0]["board"][8], "0")


    def test_03(self):
        self.assertTrue(
            self.contract.push_action(
            "restart", 
            '{"challenger":"alice", "host":"bob", "by":"bob"}',
            sess.bob), 
            "push_action restart")

        t = self.contract.get_table("games", sess.bob)
        self.assertFalse(t.error, "get_table")

        self.assertEqual(t.json["rows"][0]["board"][0], "0")
        self.assertEqual(t.json["rows"][0]["board"][1], "0")
        self.assertEqual(t.json["rows"][0]["board"][2], "0")
        self.assertEqual(t.json["rows"][0]["board"][3], "0")
        self.assertEqual(t.json["rows"][0]["board"][4], "0")
        self.assertEqual(t.json["rows"][0]["board"][5], "0")
        self.assertEqual(t.json["rows"][0]["board"][6], "0")
        self.assertEqual(t.json["rows"][0]["board"][7], "0")
        self.assertEqual(t.json["rows"][0]["board"][8], "0")


    def test_04(self):
        self.assertTrue(
            self.contract.push_action(
            "close", 
            '{"challenger":"alice", "host":"bob"}',
            sess.bob), 
            "push_action close")


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        node.stop()


if __name__ == "__main__":
    unittest.main()