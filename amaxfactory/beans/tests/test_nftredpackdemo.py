import time
import unittest
from amaxfactory.eosf import * 

class NRTest(unittest.TestCase):
    def setUp(self):
            print('setUp')
            
            reset()
            global amax,admin,nftredpack,token,ntoken,ntokena,luffy
            amax = new_master_account()
            admin = new_account(amax,"admin")

            nftredpack = new_account(amax,"nft.redpack")

            nftredpack_smart = Contract(nftredpack,"/root/contracts/did.contracts")
            nftredpack_smart.build_sh("nft.redpack")
            nftredpack_smart.deploy()
            nftredpack.set_account_permission(add_code=True)

            token = init.deploy_amax()
            ntoken = init.deploy_ntoken()
            ntokena = init.deploy_ntoken("ntokena")
            
            luffy = new_account(amax,"luffy")
            admin.transfer(luffy,"100.10000000 AMAX","")
            ntoken.pushaction("transfer",
                            {"from":admin,
                            "to":luffy,
                            "assets":[[5000,[1,0]]],
                            "memo":""},
                            admin)
            ntokena.pushaction("transfer",
                            {"from":admin,
                            "to":luffy,
                            "assets":[[50,[1,0]]],
                            "memo":""},
                            admin)
            ntoken.pushaction("transfer",
                            {"from":admin,
                            "to":luffy,
                            "assets":[[50,[2,0]]],
                            "memo":""},
                            admin)
            



    def test_start(self):
        reset()
        master = new_master_account()
        nftredpack = new_account(master,"nft.redpack")

        nftredpack_smart = Contract(nftredpack,"/root/contracts/did.contracts")
        nftredpack_smart.build_sh("nft.redpack")
        nftredpack_smart.deploy()
    
        token = init.deploy_token()
        ntoken = init.deploy_ntoken()
    
    def test_token_ontransfer(self):
        nftredpack = new_account("nft.redpack",restore=True)

        nftredpack_smart = Contract(nftredpack,"/root/contracts/did.contracts")
        nftredpack_smart.build_sh("nft.redpack",True)
        nftredpack_smart.deploy()
    
        amax = new_master_account()
        admin = new_account("admin",restore=True)

        luffy = new_account(amax,"luffy")
        admin.transfer(luffy,"100.10000000 AMAX","")
        
        nftredpack.table("fees",nftredpack)
        
        #memo params format:
        #code : id : parent_id : quantity：nft_contract
        luffy.transfer(nftredpack,"1.00000000 AMAX","code1:1:0:5:amax.ntoken")
        nftredpack.table("redpacks",nftredpack)

    def test_ntoken_ontransfer(self):
        ntoken = new_account("amax.ntoken",restore=True)
        admin = new_account("admin",restore=True)
        luffy = new_account("luffy",restore=True)
        nftredpack = new_account("nft.redpack",restore=True)

        ntoken.pushaction("transfer",
                        {"from":admin,
                            "to":luffy,
                            "assets":[[5,[1,0]]],
                            "memo":""},
                        admin)
        
        ntoken.pushaction("transfer",
                        {"from":luffy,
                            "to":nftredpack,
                            "assets":[[5,[1,0]]],
                            "memo":"hash:code1"},
                        luffy)
        
        
    
    
    def test_addfee(self):
        nftredpack = new_account("nft.redpack",restore=True)
        admin = new_account("admin",restore=True)
        ntoken = new_account("amax.ntoken",restore=True)
        token = new_account("amax.token",restore=True)
    
        nftredpack.pushaction("addfee",{"fee":"0.20000000 AMAX","fee_contract":token,"nft_contract":ntoken},nftredpack) 

    def test_cancel(self):
        nftredpack = new_account("nft.redpack",restore=True)
        admin = new_account("admin",restore=True)
        nftredpack.pushaction("cancel",{"code":'user1',},admin) 

    def test_claimredpack(self):
        
        nftredpack = new_account("nft.redpack",restore=True)
        
        admin = new_account("admin",restore=True)
        amax = new_master_account()
        robin = new_account(amax,"robin")
        nftredpack.pushaction("claimredpack",{"claimer":robin,"code":"code1","pwhash":"hash",},admin) 

    def test_delfee(self):
        nftredpack = new_account("nft.redpack",restore=True)
        admin = new_account("admin",restore=True)
        nftredpack.pushaction("delfee",{"nft_contract":new_account("amax.ntoken",restore=True),},admin) 

    def test_delredpacks(self):
        nftredpack = new_account("nft.redpack",restore=True)
        admin = new_account("admin",restore=True)
        nftredpack.pushaction("delredpacks",{"code":'user1',},admin) 

    def test_setconf(self):
        nftredpack = new_account("nft.redpack",restore=True)
        admin = new_account("admin",restore=True)
        nftredpack.pushaction("setconf",{"admin":admin,"hours":1,"enable_did":False},nftredpack) 

    def test_setconf_case(self):
        
        # setconf
        nftredpack.pushaction("setconf",{"admin":"xx1","hours":1,"enable_did":False},nftredpack,False) 
        nftredpack.pushaction("setconf",{"admin":admin,"hours":0,"enable_did":False},nftredpack,False) 
        # nftredpack.pushaction("setconf",{"admin":admin,"hours":-1,"enable_did":False},nftredpack,False) 
        nftredpack.pushaction("setconf",{"admin":admin,"hours":1,"enable_did":False},admin,False) 
        admin1 = new_account(amax,"admin1")
        nftredpack.pushaction("setconf",{"admin":admin1,"hours":1,"enable_did":True},nftredpack) 

        redpack_conf = nftredpack.table("global",nftredpack)
        assert redpack_conf.json["rows"][0]["tg_admin"] == "admin1"
        assert redpack_conf.json["rows"][0]["expire_hours"] == 1
        assert redpack_conf.json["rows"][0]["enable_did"] == 1

        nftredpack.pushaction("setconf",{"admin":admin,"hours":2,"enable_did":False},nftredpack) 
        redpack_conf = nftredpack.table("global",nftredpack)
        assert redpack_conf.json["rows"][0]["tg_admin"] == "admin"
        assert redpack_conf.json["rows"][0]["expire_hours"] == 2
        assert redpack_conf.json["rows"][0]["enable_did"] == 0

    def test_addfee_case(self):
        nftredpack.pushaction("setconf",{"admin":admin,"hours":2,"enable_did":False},nftredpack) 

        # addfee 
        nftredpack.pushaction("addfee",{"fee":"-0.20000000 AMAX","fee_contract":token,"nft_contract":ntoken},nftredpack,False) 
        nftredpack.pushaction("addfee",{"fee":"0.2000000 AMAX","fee_contract":token,"nft_contract":ntoken},nftredpack,False) 
        nftredpack.pushaction("addfee",{"fee":"0.200000 MUSSDT","fee_contract":token,"nft_contract":ntoken},nftredpack,False) 
        nftredpack.pushaction("addfee",{"fee":"0.20000000 AMAX","fee_contract":"tokenx","nft_contract":ntoken},nftredpack,False) 
        nftredpack.pushaction("addfee",{"fee":"0.20000000 AMAX","fee_contract":token,"nft_contract":"ntokenx"},nftredpack,False) 
        nftredpack.pushaction("addfee",{"fee":"0.00000000 AMAX","fee_contract":token,"nft_contract":ntoken},admin,False) 

        nftredpack.pushaction("addfee",{"fee":"0.00000000 AMAX","fee_contract":token,"nft_contract":ntoken},nftredpack) 
        fees = nftredpack.table("fees",nftredpack)
        assert fees.json["rows"][0]["nft_contract"] == "amax.ntoken"
        assert fees.json["rows"][0]["fee"]          == "0.00000000 AMAX"
        assert fees.json["rows"][0]["fee_contract"] == "amax.token"

        nftredpack.pushaction("addfee",{"fee":"0.20000000 AMAX","fee_contract":token,"nft_contract":ntoken},nftredpack) 
        fees = nftredpack.table("fees",nftredpack)
        assert fees.json["rows"][0]["nft_contract"] == "amax.ntoken"
        assert fees.json["rows"][0]["fee"]          == "0.20000000 AMAX"
        assert fees.json["rows"][0]["fee_contract"] == "amax.token"

    def test_delfee_case(self):
        nftredpack.pushaction("setconf",{"admin":admin,"hours":2,"enable_did":False},nftredpack) 
        nftredpack.pushaction("addfee",{"fee":"0.20000000 AMAX","fee_contract":token,"nft_contract":ntoken},nftredpack) 


        # delfee
        nftredpack.pushaction("delfee",{"nft_contract":"ntokenxx"},nftredpack,False) 
        nftredpack.pushaction("delfee",{"nft_contract":""},nftredpack,False) 
        nftredpack.pushaction("delfee",{"nft_contract":ntoken},admin,False) 

        nftredpack.pushaction("delfee",{"nft_contract":ntoken},nftredpack) 

        time.sleep(2)
        nftredpack.pushaction("delfee",{"nft_contract":ntoken},nftredpack,False) 

        fees = nftredpack.table("fees",nftredpack)
        assert fees.json["rows"] == []


    def test_create_case(self):
        nftredpack.pushaction("setconf",{"admin":admin,"hours":2,"enable_did":False},nftredpack) 
        
        luffy.transfer(nftredpack,"1.00000000 AMAX","code1:1:0:5:amax.ntoken",False)

        nftredpack.pushaction("addfee",{"fee":"0.00000000 AMAX","fee_contract":token,"nft_contract":ntoken},nftredpack) 
        luffy.transfer(nftredpack,"1.00000000 AMAX","code:1:0:5:amax.ntoken")

        time.sleep(2)
        nftredpack.pushaction("addfee",{"fee":"0.20000000 AMAX","fee_contract":token,"nft_contract":ntoken},nftredpack) 
        
        #memo params format:
        #code : id : parent_id : quantity：nft_contract
        luffy.transfer(nftredpack,"1.00000000 AMAX","code1:1:0:5:amax.ntoken")
        luffy.transfer(nftredpack,"1.00000000 AMAX","code1:1:0:6:amax.ntoken",False)

        #code 为空应失败
        luffy.transfer(nftredpack,"1.00000000 AMAX",":1:0:5:amax.ntoken",False)
        luffy.transfer(nftredpack,"1.00000000 AMAX","code2:0:0:5:amax.ntoken",False)
        luffy.transfer(nftredpack,"1.00000000 AMAX","code2::0:5:amax.ntoken",False)
        luffy.transfer(nftredpack,"1.00000000 AMAX","code2:1::5:amax.ntoken",False)
        luffy.transfer(nftredpack,"1.00000000 AMAX","code3:100:0:5:amax.ntoken",False)

        #quantity 为0应失败
        luffy.transfer(nftredpack,"1.00000000 AMAX","code2:1:0:0:amax.ntoken",False)
        # luffy.transfer(nftredpack,"1.00000000 AMAX","code2:1:0:-5:amax.ntoken",False)
        # luffy.transfer(nftredpack,"1.00000000 AMAX","code2:1:-1:5:amax.ntoken",False)
        # luffy.transfer(nftredpack,"1.00000000 AMAX","code2:-1:0:5:amax.ntoken",False)

        #数量大于用户余额应失败
        luffy.transfer(nftredpack,"100.00000000 AMAX","code2:1:0:500:amax.ntoken",False)

        luffy.transfer(nftredpack,"1.00000000 AMAX","code3:1:0:5:amntoken",False)
        luffy.transfer(nftredpack,"1.00000000 AMAX","code3:1:0:5:amax.token",False)

        nftredpack.table("redpacks",nftredpack)

    # fee = 0
    def test_deposit_case(self):
        nftredpack.pushaction("setconf",{"admin":admin,"hours":2,"enable_did":False},nftredpack) 
        
        # 未添加fee配置，应失败
        ntoken.pushaction("transfer",
                           {"from":luffy,
                            "to":nftredpack,
                            "assets":[[5,[1,0]]],
                            "memo":"hash1:code1"},
                           luffy,False)

        nftredpack.pushaction("addfee",{"fee":"0.00000000 AMAX","fee_contract":token,"nft_contract":ntoken},nftredpack) 
        
        # fee = 0 时，应可以直接创建红包
        ntoken.pushaction("transfer",
                        {"from":luffy,
                            "to":nftredpack,
                            "assets":[[5,[1,0]]],
                            "memo":"hash2:code2"},
                        luffy)
        nftredpack.pushaction("claimredpack",{"claimer":admin,"code":"code2","pwhash":"hash2",},admin) 

        

        
        ntoken.pushaction("transfer",
                        {"from":luffy,
                            "to":nftredpack,
                            "assets":[[5,[1,0]]],
                            "memo":":code3"},
                        luffy,False)
        ntoken.pushaction("transfer",
                        {"from":luffy,
                            "to":nftredpack,
                            "assets":[[5,[1,0]]],
                            "memo":"hash4:"},
                        luffy,False)
        time.sleep(2)
        ntoken.pushaction("transfer",
                        {"from":luffy,
                            "to":nftredpack,
                            "assets":[[1,[1,0]]],
                            "memo":"hash2:code2"},
                        luffy,False)    
    
    # fee != 0
    def test_deposit_case2(self):
        nftredpack.pushaction("setconf",{"admin":admin,"hours":2,"enable_did":False},nftredpack) 
        nftredpack.pushaction("addfee",{"fee":"0.10000000 AMAX","fee_contract":token,"nft_contract":ntoken},nftredpack) 
                
        ntoken.pushaction("transfer",
                        {"from":luffy,
                            "to":nftredpack,
                            "assets":[[5,[1,0]]],
                            "memo":"hash:code1"},
                        luffy,False)

        luffy.transfer(nftredpack,"0.50000000 AMAX","code1:1:0:5:amax.ntoken")

        ntoken.pushaction("transfer",
                        {"from":luffy,
                            "to":nftredpack,
                            "assets":[[1,[1,0]]],
                            "memo":"hash:code1"},
                        luffy,False)

        ntoken.pushaction("transfer",
                        {"from":luffy,
                            "to":nftredpack,
                            "assets":[[5,[2,0]]],
                            "memo":"hash:code1"},
                        luffy,False)

        ntokena.pushaction("transfer",
                        {"from":luffy,
                            "to":nftredpack,
                            "assets":[[5,[1,0]]],
                            "memo":"hash:code1"},
                        luffy,False)


        ntoken.pushaction("transfer",
                        {"from":luffy,
                            "to":nftredpack,
                            "assets":[[5,[1,0]]],
                            "memo":"hash:code1"},
                        luffy)
        # time.sleep(2)
        ntoken.pushaction("transfer",
                        {"from":luffy,
                            "to":nftredpack,
                            "assets":[[5,[1,0]]],
                            "memo":"hash:code1"},
                        luffy,False)

        robin1 = new_account(amax,"robin1")
        nftredpack.pushaction("claimredpack",{"claimer":robin1,"code":"code1","pwhash":"hash",},admin) 

        robin2 = new_account(amax,"robin2")
        nftredpack.pushaction("claimredpack",{"claimer":robin2,"code":"code1","pwhash":"hash",},admin) 

        robin3 = new_account(amax,"robin3")
        nftredpack.pushaction("claimredpack",{"claimer":robin3,"code":"code1","pwhash":"hash",},admin) 

        robin4 = new_account(amax,"robin4")
        nftredpack.pushaction("claimredpack",{"claimer":robin4,"code":"code1","pwhash":"hash",},admin) 

        robin5 = new_account(amax,"robin5")
        nftredpack.pushaction("claimredpack",{"claimer":robin5,"code":"code1","pwhash":"hash",},admin) 

        robina = new_account(amax,"robina")
        nftredpack.pushaction("claimredpack",{"claimer":robina,"code":"code1","pwhash":"hash",},admin,False) 
        
        nftredpack.table("redpacks",nftredpack)

        time.sleep(2)
        ntoken.pushaction("transfer",
                        {"from":luffy,
                            "to":nftredpack,
                            "assets":[[5,[1,0]]],
                            "memo":"hash:code1"},
                        luffy,False)


    def test_claim_case(self):
        nftredpack.pushaction("setconf",{"admin":admin,"hours":2,"enable_did":False},nftredpack) 
        nftredpack.pushaction("addfee",{"fee":"0.10000000 AMAX","fee_contract":token,"nft_contract":ntoken},nftredpack) 

        robin1 = new_account(amax,"robin1")

        luffy.transfer(nftredpack,"0.50000000 AMAX","code1:1:0:5:amax.ntoken")

        robin1 = new_account(amax,"robin1")
        nftredpack.pushaction("claimredpack",{"claimer":robin1,"code":"code1","pwhash":"",},admin,False) 

        ntoken.pushaction("transfer",
                        {"from":luffy,
                            "to":nftredpack,
                            "assets":[[5,[1,0]]],
                            "memo":"hash:code1"},
                        luffy)

        nftredpack.pushaction("claimredpack",{"claimer":robin1,"code":"code1","pwhash":"hash",},robin1,False) 
        nftredpack.pushaction("claimredpack",{"claimer":"userxx","code":"code1","pwhash":"hash",},admin,False) 
        nftredpack.pushaction("claimredpack",{"claimer":robin1,"code":"codex1","pwhash":"hash",},admin,False) 
        nftredpack.pushaction("claimredpack",{"claimer":robin1,"code":"code1","pwhash":"hashxx",},admin,False) 

        nftredpack.pushaction("claimredpack",{"claimer":robin1,"code":"code1","pwhash":"hash",},admin) 

        time.sleep(2)
        nftredpack.pushaction("claimredpack",{"claimer":robin1,"code":"code1","pwhash":"hash",},admin,False) 

        robin2 = new_account(amax,"robin2")
        nftredpack.pushaction("claimredpack",{"claimer":robin2,"code":"code1","pwhash":"hash",},admin) 

        robin3 = new_account(amax,"robin3")
        nftredpack.pushaction("claimredpack",{"claimer":robin3,"code":"code1","pwhash":"hash",},admin) 

        robin4 = new_account(amax,"robin4")
        nftredpack.pushaction("claimredpack",{"claimer":robin4,"code":"code1","pwhash":"hash",},admin) 

        robin5 = new_account(amax,"robin5")
        nftredpack.pushaction("claimredpack",{"claimer":robin5,"code":"code1","pwhash":"hash",},admin) 

        robina = new_account(amax,"robina")
        nftredpack.pushaction("claimredpack",{"claimer":robina,"code":"code1","pwhash":"hash",},admin,False) 
        
        nftredpack.table("redpacks",nftredpack)

    def test_cancel_case(self):
        nftredpack.pushaction("setconf",{"admin":admin,"hours":2,"enable_did":False},nftredpack) 
        nftredpack.pushaction("addfee",{"fee":"0.10000000 AMAX","fee_contract":token,"nft_contract":ntoken},nftredpack) 

        robin1 = new_account(amax,"robin1")

        luffy.transfer(nftredpack,"0.50000000 AMAX","code:1:0:5:amax.ntoken")

        # nftredpack.pushaction("cancel",{"code":'code1',},admin,False) 

        # time.sleep(11)

        nftredpack.pushaction("cancel",{"code":'code',},robin1,False) 
        nftredpack.pushaction("cancel",{"code":'code2',},admin,False) 
        nftredpack.pushaction("cancel",{"code":'code',},admin) 


        luffy.transfer(nftredpack,"0.50000000 AMAX","code1:1:0:5:amax.ntoken")

        ntoken.pushaction("transfer",
                        {"from":luffy,
                            "to":nftredpack,
                            "assets":[[5,[1,0]]],
                            "memo":"hash:code1"},
                        luffy)

        robin1 = new_account(amax,"robin1")
        nftredpack.pushaction("claimredpack",{"claimer":robin1,"code":"code1","pwhash":"hash",},admin) 

        robin2 = new_account(amax,"robin2")
        nftredpack.pushaction("claimredpack",{"claimer":robin2,"code":"code1","pwhash":"hash",},admin) 

        robin3 = new_account(amax,"robin3")
        nftredpack.pushaction("claimredpack",{"claimer":robin3,"code":"code1","pwhash":"hash",},admin) 

        robin4 = new_account(amax,"robin4")
        nftredpack.pushaction("claimredpack",{"claimer":robin4,"code":"code1","pwhash":"hash",},admin) 

        robin5 = new_account(amax,"robin5")
        nftredpack.pushaction("claimredpack",{"claimer":robin5,"code":"code1","pwhash":"hash",},admin) 

        robina = new_account(amax,"robina")
        nftredpack.pushaction("claimredpack",{"claimer":robina,"code":"code1","pwhash":"hash",},admin,False) 
        
        nftredpack.pushaction("cancel",{"code":'code1',},admin) 

        nftredpack.table("redpacks",nftredpack)


        luffy.transfer(nftredpack,"0.50000000 AMAX","code3:1:0:5:amax.ntoken")

        ntoken.pushaction("transfer",
                        {"from":luffy,
                            "to":nftredpack,
                            "assets":[[5,[1,0]]],
                            "memo":"hash3:code3"},
                        luffy)
        nftredpack.pushaction("cancel",{"code":'code3',},admin) 


        luffy.transfer(nftredpack,"0.50000000 AMAX","code4:1:0:5:amax.ntoken")

        ntoken.pushaction("transfer",
                        {"from":luffy,
                            "to":nftredpack,
                            "assets":[[5,[1,0]]],
                            "memo":"hash4:code4"},
                        luffy)
        nftredpack.pushaction("claimredpack",{"claimer":robin1,"code":"code4","pwhash":"hash4",},admin) 

        nftredpack.pushaction("cancel",{"code":'code4',},admin) 

        nftredpack.pushaction("addfee",{"fee":"0.00000000 AMAX","fee_contract":token,"nft_contract":ntoken},nftredpack) 
        ntoken.pushaction("transfer",
                        {"from":luffy,
                            "to":nftredpack,
                            "assets":[[5,[1,0]]],
                            "memo":"hash5:code5"},
                        luffy)
        nftredpack.pushaction("claimredpack",{"claimer":robin1,"code":"code5","pwhash":"hash5",},admin) 

        nftredpack.pushaction("cancel",{"code":'code5',},admin) 
        

    def test_cancel_max_case(self):
        nftredpack.pushaction("setconf",{"admin":admin,"hours":2,"enable_did":False},nftredpack) 
        nftredpack.pushaction("addfee",{"fee":"0.01000000 AMAX","fee_contract":token,"nft_contract":ntoken},nftredpack) 

        luffy.transfer(nftredpack,"1.00000000 AMAX","code:1:0:100:amax.ntoken")

        ntoken.pushaction("transfer",
                        {"from":luffy,
                            "to":nftredpack,
                            "assets":[[100,[1,0]]],
                            "memo":"hash:code"},
                        luffy)

        for i in range(100):
            temp = new_account(amax)
            nftredpack.pushaction("claimredpack",{"claimer":temp,"code":"code","pwhash":"hash",},admin) 

        luffy.transfer(nftredpack,"1.00000000 AMAX","code2:1:0:100:amax.ntoken")

        ntoken.pushaction("transfer",
                        {"from":luffy,
                            "to":nftredpack,
                            "assets":[[100,[1,0]]],
                            "memo":"hash:code2"},
                        luffy)
        

        for i in range(50):
            temp = new_account(amax)
            nftredpack.pushaction("claimredpack",{"claimer":temp,"code":"code2","pwhash":"hash",},admin) 

        nftredpack.pushaction("cancel",{"code":'code',},admin) 

        # nftredpack.pushaction("cancel",{"code":'code2',},admin) 
        
        for i in range(10):
            time.sleep(2)
            nftredpack.pushaction("delclaims",{"max_rows":15,},admin) 

        nftredpack.table("redpacks",nftredpack)
        nftredpack.table("claims",nftredpack)
