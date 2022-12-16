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

        # build 方法内容：
        # 编译合约
        # 复制到/templates/wasm/文件夹下
        # 运行amaxfactory.bean.test_create_bean方法，自动创建合约的对象文件
        # 把合约类添加到init.py中
        speedreg_path = "/root/contracts/joss/amax.contracts/src_tools"
        init.build(speedreg_path)

        master = new_master_account()
        admin = new_account(master,"admin")

        # 实例化合约，自动部署好，add-code
        amax_token = init.AMAX_TOKEN()
        # 合约的预设操作，可以不调用，也可能没有对应的方法
        amax_token.setup()

        # 可以指定账号,可以加setup一起
        amax_token1 = init.AMAX_TOKEN("amax.token1").setup()

        # 可以直接调用合约方法
        amax_token.transfer(admin,master,"1.00000000 AMAX","",admin)

        # 查表
        amax_token.get_accounts(admin)


        apl = init.APLINK_TOKEN().setup()
        mtoken = init.AMAX_MTOKEN().setup()
        

        COMMENT('''
        流程测试示例:
        ''')

        recover = init.AMAX_RECOVER()
        proxy = init.AMAX_PROXY()
        checker1 = init.AMAX_AUTH()
        checker2 = init.AMAX_AUTH("checker2")
        checker3 = init.AMAX_AUTH("checker3")

        bob = new_account(master,"bob")
        
        recover.init(4,proxy,recover)
        proxy.init(recover,proxy)
        checker1.init(recover,proxy,checker1)
        checker2.init(recover,proxy,checker2)
        checker3.init(recover,proxy,checker3)

        recover.addauditconf(checker1,"mobileno",["1.00000000 MUSDT","title","desc","url",3,True,"running"],recover)
        recover.addauditconf(checker2,"mobileno",["1.00000000 MUSDT","title","desc","url",3,True,"running"],recover)
        recover.addauditconf(checker3,"mobileno",["1.00000000 MUSDT","title","desc","url",3,True,"running"],recover)

        checker1.setauth(admin,["bindinfo","createorder","setscore","newaccount"],checker1)
        checker2.setauth(admin,["bindinfo","createorder","setscore","newaccount"],checker2)
        checker3.setauth(admin,["bindinfo","createorder","setscore","newaccount"],checker3)
        
        checker1.newaccount(admin,proxy,"luffy","infoxx",[1,[[bob.args[3],1]],[],[]],admin)

        luffy = new_account("luffy",restore=True)
        
        recover.addauth(luffy,checker2,luffy)
        recover.addauth(luffy,checker3,luffy)

        checker2.bindinfo(admin,luffy,"xxxxxsss",admin)
        checker3.bindinfo(admin,luffy,"xxxxxsss",admin)

        checker1.createorder(1,admin,luffy,False,1,["public_key","AM4tjT4pZsFWT8MT8jWr5JHiDuPvTqr9wwWKvMM5c4gg5jW98R6F"],admin)
        checker1.createorder(1,admin,luffy,False,1,["public_key","AM4tjT4pZsFWT8MT8jWr5JHiDuPvTqr9wwWKvMM5c4gg5jW98R6F"],bob,False)

        checker1.setscore(admin,luffy,1,3,admin)
        checker2.setscore(admin,luffy,1,3,admin) 

        recover.get_recorders(recover)

        recover.closeorder(checker3,1,checker3)

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
