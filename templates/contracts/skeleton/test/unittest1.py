import unittest
from  eosfactory import *

Logger.verbosity = [Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG]
_ = Logger()

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        _.SCENARIO('''
Set-up is that the local testnet is runnuning, after reseting, and it contains 
the "hello" account that has power of returning greetings after pushed any 
account.

Test is to demonstrate Factory's facility for debugging smart contracts.

Note the "logger_info("user: ", name{user});" statement in the code of the 
contract in the file "hello.cpp":

        #define DEBUG
        #include "logger.hpp"

        using namespace eosio;

        class hello : public eosio::contract {
        public:
            using contract::contract; 

            /// @abi action 
            void hi( account_name user ) {

            logger_info("user: ", name{user});
        ..............................................................

The test verifies the contents of the "DEBUG" channel of the Factory's logger.
""
        ''')
        reset([Verbosity.INFO])
        create_wallet()
        account_master_create("account_master")
        account_create("hello", account_master)
        import sys
        contract = Contract(hello, sys.path[0] + "/../")
        contract.build()
        contract.deploy()
        
        set_is_testing_errors()        

    def test_debugging_printout(self):

        account_create("alice", account_master)
        hello.push_action(
            "hi", {"user":alice}, alice)
        self.assertTrue("alice" in hello.debug_buffer)

        account_create("carol", account_master)
        hello.push_action(
            "hi", {"user":carol}, carol)
        self.assertTrue("carol" in hello.debug_buffer)
            
    @classmethod
    def tearDownClass(cls):
        stop()

if __name__ == "__main__":
    unittest.main()