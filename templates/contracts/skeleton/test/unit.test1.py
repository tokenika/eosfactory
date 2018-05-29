import unittest
import warnings
import json
import pyteos
import node
import sess
from eosf import *

pyteos.set_verbose(False)

class Test1(unittest.TestCase):

    contract = None

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

        
    def setUp(self):
        self.assertTrue(node.is_running(), "testnet failure")
        self.contract = Contract("@CONTRACT_NAME@/build")
        self.assertFalse(self.contract.error, "contract failure")


    def test_01(self):
        self.assertTrue(self.contract.get_code(), "get_code")
        self.assertTrue(self.contract.deploy(), "deploy")
        self.assertTrue(self.contract.get_code(), "get_code")


    def test_02(self):
        self.assertTrue(
            self.contract.push_action(
            "hi", 
            '{"user":"alice"}',
            sess.alice),
            "push_action hi 1")

        self.assertTrue(
            self.contract.push_action(
            "hi", 
            '{"user":"carol"}',
            sess.carol),
            "push_action hi 2")


    def test_03(self):
        self.assertFalse(
            self.contract.push_action(
            "hi", 
            '{"user":"carol"}',
            sess.alice),
            "push_action hi 3")


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        node.stop()


if __name__ == "__main__":
    unittest.main()