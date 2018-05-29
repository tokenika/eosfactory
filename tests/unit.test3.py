# python3 ./tests/unit.test1.py

import unittest
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
        node.reset()
        sess.setup()
        cls.contract = ContractFromTemplate("_e4b2ffc804529ce9c6fae258197648cc2", remove_existing = True)

        
    def setUp(self):
        self.assertTrue(node.is_running(), "testnet failure")

        
    def test_01(self):
        self.assertTrue(self.__class__.contract.build(), "build")

    
    def test_02(self):
        self.assertTrue(self.__class__.contract.deploy(), "deploy")


    def test_03(self):
        self.assertTrue(self.__class__.contract.get_code(), "get_code")


    def test_04(self):
        self.assertTrue(
            self.__class__.contract.push_action(
            "hi", 
            '{"user":"alice"}',
            sess.alice),
            "push_action hi 1")

        self.assertTrue(
            self.__class__.contract.push_action(
            "hi", 
            '{"user":"carol"}',
            sess.carol),
            "push_action hi 2")


    def test_05(self):
        self.assertFalse(
            self.__class__.contract.push_action(
            "hi", 
            '{"user":"carol"}',
            sess.alice),
            "push_action hi 3")


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        cls.contract.delete()
        node.stop()


if __name__ == "__main__":
    unittest.main()