# python3 ./tests/unit.test1.py

import unittest
import warnings
import json
import node
import sess
from eosf import *

set_verbose(False)

class Test1(unittest.TestCase):

    CONTRACT_NAME = ""

    def run(self, result = None):
        """ Stop after first error """      
        if not result.failures:
            super().run(result)


    @classmethod
    def setUpClass(cls):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cls.assertTrue(node.reset(), "node failure")
        cls.assertTrue(sess.setup(), "session failure")

        contract = Contract(cls.CONTRACT_NAME)
        cls.assertTrue(contract.is_created(), "contract failure")
        cls.assertTrue(contract.deploy(), "deployment failure")


    def setUp(self):
        self.contract = Contract(self.CONTRACT_NAME)
        self.assertTrue(self.contract.is_deployed(), "contract is not deployed")
        

    def test_01(self):
        #########################
        # Your test 1 goes here #
        #########################
        pass


    def test_02(self):
        #########################
        # Your test 2 goes here #
        #########################
        pass


    def test_03(self):
        #########################
        # Your test 3 goes here #
        #########################
        pass


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        node.stop()


if __name__ == "__main__":
    unittest.main()