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
        c = eosf.Contract("@CONTRACT_NAME@/build")
        self.assertFalse(c.error, "Contract")

        self.assertTrue(c.get_code(), "get_code")
        self.assertTrue(c.deploy(), "deploy")
        self.assertTrue(c.get_code(), "get_code")

        c.push_action("hi", '{"user":"alice"}', sess.alice)
        out = c.get_console()
        print(out, "\n")
        self.assertTrue(out.find("Hello, alice") != -1)
        
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