import time
import unittest
from amaxfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE, Verbosity.DEBUG])

CONTRACT_WASM_PATH = "/root/contracts/charlie/amaxfactory/templates/wasm/"

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        SCENARIO('''
        Create a contract from template, then build and deploy it.
        ''')
        reset()
    
    
    @classmethod
    def tearDownClass(cls):
        # time.sleep(60)
        stop()
        
    def test_register(self):
        '''The only test function.

        The account objects `master, host, alice, ...` which are of the global namespace, do not have to be explicitly declared (and still keep the linter silent).
        '''
        
        master = new_master_account()
        
        admin = new_account(master,"admin")
        init.deploy_amax(admin)
        init.deploy_apl_newbie(admin)
        init.deploy_mtoken(admin)
        
        COMMENT('''
        Create test accounts:
        ''')

        recover = new_account(master,"amax.recover")
        proxy = new_account(master,"amax.proxy")
        checker1 = new_account(master,"checker1")
        checker2 = new_account(master,"checker2")
        checker3 = new_account(master,"checker3")

        bob = new_account(master,"bob")

        recover_smart = Contract(recover,"/root/contracts/joss/amax.contracts/src_tools")
        recover_smart.build_sh("amax.recover")
        recover_smart.deploy()

        proxy_smart = Contract(proxy,"/root/contracts/joss/amax.contracts/src_tools")
        proxy_smart.build_sh("amax.proxy")
        proxy_smart.deploy()
        
        checker1_smart = Contract(checker1,"/root/contracts/joss/amax.contracts/src_tools")
        checker1_smart.build_sh("amax.checker")
        checker1_smart.deploy()

        checker2_smart = Contract(checker2,"/root/contracts/joss/amax.contracts/src_tools")
        checker2_smart.build_sh("amax.checker")
        checker2_smart.deploy()

        checker3_smart = Contract(checker3,"/root/contracts/joss/amax.contracts/src_tools")
        checker3_smart.build_sh("amax.checker")
        checker3_smart.deploy()

        recover.set_account_permission(add_code=True)
        proxy.set_account_permission(add_code=True)
        checker1.set_account_permission(add_code=True)
        checker2.set_account_permission(add_code=True)
        checker3.set_account_permission(add_code=True)
        
        
        recover.push_action("init",
                            {"recover_threshold":4,
                             "amax_proxy_contract":proxy},
                            permission=(recover, Permission.ACTIVE))

        proxy.push_action("init",
                            {"amax_recover":recover},
                            permission=(proxy, Permission.ACTIVE))

        checker1.push_action("init",
                            {"amax_recover":recover,
                             "amax_proxy_contract":proxy},
                            permission=(checker1, Permission.ACTIVE))

        checker2.push_action("init",
                            {"amax_recover":recover,
                             "amax_proxy_contract":proxy},
                            permission=(checker2, Permission.ACTIVE))

        checker3.push_action("init",
                            {"amax_recover":recover,
                             "amax_proxy_contract":proxy},
                            permission=(checker3, Permission.ACTIVE))
        
        
        recover.push_action("addauditconf",
                            {"check_contract":checker1,
                             "audit_type":"mobileno",
                             "conf":["1.00000000 MUSDT","title","desc","url",3,True,"running"]})
        
        recover.push_action("addauditconf",
                            {"check_contract":checker2,
                             "audit_type":"answer",
                             "conf":["1.00000000 MUSDT","title","desc","url",3,True,"running"]})
        
        recover.push_action("addauditconf",
                            {"check_contract":checker3,
                             "audit_type":"did",
                             "conf":["1.00000000 MUSDT","title","desc","url",3,False,"running"]})


        checker1.push_action("setauditor",
                            {"account":admin,
                             "actions":["bindinfo","createorder","setscore","newaccount"]},
                            )
        checker2.push_action("setauditor",
                            {"account":admin,
                             "actions":["bindinfo","createorder","setscore","newaccount"]},
                            )
        checker3.push_action("setauditor",
                            {"account":admin,
                             "actions":["bindinfo","createorder","setscore","newaccount"]},
                            )
        

        checker1.push_action("newaccount",
                             {"admin":admin,
                              "creator":proxy,
                              "account":"luffy",
                              "info":"infoxxxx",
                              "active":[1,[[bob.args[3],1]],[],[]]},
                             permission=(admin, Permission.ACTIVE))
        
        luffy = new_account("luffy",restore=True)
        
        recover.push_action("addauth",
                            {"account":luffy,
                             "contract":checker2},
                             permission=(luffy, Permission.ACTIVE))
        
        recover.push_action("addauth",
                            {"account":luffy,
                             "contract":checker3},
                             permission=(luffy, Permission.ACTIVE))
        
        checker2.push_action("bindinfo",
                             {"admin":admin,
                              "account":luffy,
                              "info":"lfajsldflsf"},
                             permission=(admin, Permission.ACTIVE))
        checker3.push_action("bindinfo",
                             {"admin":admin,
                              "account":luffy,
                              "info":"lfajsldflsf"},
                             permission=(admin, Permission.ACTIVE))

        checker1.push_action("createorder",
                             {"sn":1,
                              "admin":admin,
                              "account":luffy,
                              "manual_check_required":False,
                              "score":1,
                              "recover_target":["public_key","AM4tjT4pZsFWT8MT8jWr5JHiDuPvTqr9wwWKvMM5c4gg5jW98R6F"]},
                             permission=(admin, Permission.ACTIVE))
        
        checker1.pushaction("createorder",
                             {"sn":1,
                              "admin":admin,
                              "account":luffy,
                              "manual_check_required":False,
                              "score":1,
                              "recover_target":["public_key","AM4tjT4pZsFWT8MT8jWr5JHiDuPvTqr9wwWKvMM5c4gg5jW98R6F"]},
                             bob,False)
        
        checker1.pushaction("setscore",
                            {"admin":admin,
                            "account":luffy,
                            "order_id":1,
                            "score":3},
                            admin)
        
        checker2.pushaction("setscore",
                            {"admin":admin,
                            "account":luffy,
                            "order_id":1,
                            "score":3},
                            admin)
        
        recover.pushaction("closeorder",
                            {"submitter":admin,
                            "order_id":1},
                            admin)

        luffy.info()

        # admin = new_account(master,"admin")
        # init.deploy_amax(admin)
        # init.deploy_apl_newbie(admin)
        # init.deploy_mtoken(admin)

        # alice = new_account(master)
        # admin.transfer(alice,"1.00000000 AMAX")
        
        # amaxtoken = new_account(master,"amax.token")
        # admin = new_account("admin",restore=True)
        # bob = new_account(master)
        
        # mdaoinfo = new_account(master,"mdao.info")
        # mdaoinfo = new_account("mdao.info",restore=True)

        # info_smart = Contract(mdaoinfo,"/root/contracts/mdao.contracts")
        # info_smart.build_sh("mdao.info")
        # info_smart.deploy()

        # amaxtoken.push_action(
        # "transfer",
        # {
        #     "from": admin, "to": bob, 
        #     "quantity": "1.00000000 AMAX", "memo": "memo"
        # },
        # permission=(admin, Permission.ACTIVE))
        # admin.transfer(bob,"1.00000000 AMAX")
        # admin.transfer(bob,"2.0000 APL")
        # admin.transfer(bob,"3.00000000 MBTC")
        # admin.transfer(bob,"5.000000 MUSDT")

        # amaxtoken = new_account("",restore=True)
        # amaxtoken.info()
        # contract.print_stat()
        # bob = new_account(master)
        # carol = new_account(master)        
        
        # COMMENT('''
        # Create, build and deploy the contract:
        # ''')
        # host = new_account(master)
        # smart = Contract(host, 
        #     wasm_file=CONTRACT_WASM_PATH + 'amax/amax.token/amax.token.wasm',
        #     abi_file=CONTRACT_WASM_PATH + "amax/amax.token/amax.token.abi")
        # # smart.build()
        # smart.deploy()

        # COMMENT('''
        # Initialize the token and send some tokens to one of the accounts:
        # ''')

        # host.push_action(
        #     "create",
        #     {
        #         "issuer": alice,
        #         "maximum_supply": "1000000000.00000000 AMAX",
        #         "can_freeze": "0",
        #         "can_recall": "0",
        #         "can_whitelist": "0"
        #     },
        #     permission=[(master, Permission.ACTIVE), (host, Permission.ACTIVE)])

        # host.push_action(
        #     "issue",
        #     {
        #         "to": alice, "quantity": "100.00000000 AMAX", "memo": ""
        #     },
        #     permission=(alice, Permission.ACTIVE))

        # COMMENT('''
        # Execute a series of transfers between the accounts:
        # ''')

        # host.push_action(
        #     "transfer",
        #     {
        #         "from": alice, "to": carol,
        #         "quantity": "25.00000000 AMAX", "memo":""
        #     },
        #     permission=(alice, Permission.ACTIVE))

        # host.push_action(
        #     "transfer",
        #     {
        #         "from": carol, "to": bob, 
        #         "quantity": "11.00000000 AMAX", "memo": ""
        #     },
        #     permission=(carol, Permission.ACTIVE))

        # host.push_action(
        #     "transfer",
        #     {
        #         "from": carol, "to": bob, 
        #         "quantity": "2.00000000 AMAX", "memo": ""
        #     },
        #     permission=(carol, Permission.ACTIVE))

        # host.push_action(
        #     "transfer",
        #     {
        #         "from": bob, "to": alice, \
        #         "quantity": "2.00000000 AMAX", "memo":""
        #     },
        #     permission=(bob, Permission.ACTIVE))

        # COMMENT('''
        # Verify the outcome:
        # ''')

        # table_alice = host.table("accounts", alice)
        # table_bob = host.table("accounts", bob)
        # table_carol = host.table("accounts", carol)

        # self.assertEqual(
        #     table_alice.json["rows"][0]["balance"], '77.00000000 AMAX',
        #     '''assertEqual(table_alice.json["rows"][0]["balance"], '77.00000000 AMAX')''')
        # self.assertEqual(
        #     table_bob.json["rows"][0]["balance"], '11.00000000 AMAX',
        #     '''assertEqual(table_bob.json["rows"][0]["balance"], '11.00000000 AMAX')''')
        # self.assertEqual(
        #     table_carol.json["rows"][0]["balance"], '12.00000000 AMAX',
        #     '''assertEqual(table_carol.json["rows"][0]["balance"], '12.00000000 AMAX')''')




if __name__ == "__main__":
    unittest.main()
