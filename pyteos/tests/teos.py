# python3 ./pyteos/tests/teos.py 

import unittest
import warnings
import teos


class Test1(unittest.TestCase):

    def run(self, result=None):
        """ Stop after first error """      
        if not result.failures:
            super().run(result)

    @classmethod
    def setUpClass(cls):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            teos.node_reset()

    def setUp(self):
        pass

    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        teos.node_stop()

if __name__ == "__main__":
    unittest.main()