import unittest
import json
import random
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE, Verbosity.DEBUG])

CONTRACT_WORKSPACE = "_wslqwjvacdyugodewiyd"

class Test(unittest.TestCase):

    def run(self, result=None):
        super().run(result)

    @classmethod
    def init_eosio(cls):
        system_contract_path = "/Users/wuyuan/Documents/study/eos/build/contracts/"
        create_account("et",master,"eosio.token")
        create_account("em",master,"eosio.msig")
        create_account("er",master,"eosio.ram")
        create_account("erf",master,"eosio.ramfee")
        create_account("es",master,"eosio.stake")
        et_contract = Contract(et,system_contract_path + "eosio.token","eosio.token.abi","eosio.token.wasm")
        et_contract.deploy();
        em_contract = Contract(em,system_contract_path + "eosio.msig","eosio.msig.abi","eosio.msig.wasm")
        em_contract.deploy();

        et.push_action("create",{"issuer":"eosio","maximum_supply":"100000000000.0000 EOS"},permission=(et,Permission.ACTIVE))
        et.push_action("issue",{"to":"eosio","quantity":"100000000.0000 EOS","memo":"haha"},permission=(master,Permission.ACTIVE))


    @classmethod
    def setUpClass(cls):
        SCENARIO('''
        Create a contract from dice, then build and deploy it.
        ''')
        reset()
        create_master_account("master");
        append_account_methods_and_finish(master.account_object_name,master)
        cls.init_eosio()
        contract = Contract(master,"/Users/wuyuan/Documents/study/eos/build/contracts/eosio.system","eosio.system.abi","eosio.system.wasm")
        contract.deploy()
        create_account("dice",master,"dice","","","1000","1000",None,"10000")
        create_account("alice",master,"alice","","","1000","1000",None,"1000")
        create_account("bob",master,"bob","","","1000","1000",None,"1000")

        et.push_action("transfer",{"from":"eosio","to":"alice","quantity":"10000.0000 EOS","memo":"hi"},permission=("eosio",Permission.ACTIVE))
        et.push_action("transfer",{"from":"eosio","to":"bob","quantity":"10000.0000 EOS","memo":"hi"},permission=("eosio",Permission.ACTIVE))

    def setUp(self):
        pass

    def deploy_contract(self):
        dice_path = "/usr/local/eosProject/sample/dice_contract/"
        dice_contract = Contract(dice,dice_path, "dice_contract.abi", "dice_contract.wasm")
        dice_contract.deploy()

    def updateauth(self,name):
        try:
            master.push_action("updateauth",{"account": name, "permission": "active", "parent": "owner", "auth": {"threshold": 1, "keys": [{"key":"EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV","weight":1}], "waits": [], "accounts": [{"permission":{"actor":dice.name,"permission":"eosio.code"},"weight":1}]}},permission=(name, Permission.ACTIVE))
        except errors.Error as e:
            print("except errors.Error as e: ",e)

    def deposit(self, eosfrom, quantity):
        try:
            dice.push_action("deposit",{"from":eosfrom,"quantity":quantity},permission=(eosfrom,Permission.ACTIVE))
        except errors.Error as e:
            print("except errors.Error as e: ",e)

    def withdraw(self, to, quantity):
        try:
            dice.push_action("withdraw",{"to":to,"quantity":quantity},permission=(to,Permission.ACTIVE))
        except errors.Error as e:
            print("except errors.Error as e: ",e)

    def offerbet(self, bet, player, commitment):
        try:
            dice.push_action("offerbet",{"bet":bet,"player":player,"commitment":commitment},permission=(player,Permission.ACTIVE))
        except errors.Error as e:
            print("except errors.Error as e: ",e)

    def canceloffer(self, commitment,player):
        try:
            dice.push_action("canceloffer",{"commitment":commitment},permission=(player,Permission.ACTIVE))
        except errors.Error as e:
            print("except errors.Error as e: ",e)

    def reveal(self, commitment, source, player):
        try:
            dice.push_action("reveal",{"commitment":commitment,"source":source},permission=(player,Permission.ACTIVE))
        except errors.Error as e:
            print("except errors.Error as e: ",e)

    def get_offer_by_commitment(self, commitment):
        try:
            offer = dice.table("offer",dice.name,False,1,"",commitment,"","ter","sha256").json["rows"]
            if len(offer) != 0:
                self.assertEqual( offer[0]["commitment"] , commitment, "not this game id")
                return offer[0]
        except errors.Error as e:
            print("except errors.Error as e: ",e)
        return None

    def get_offer_by_id(self, id):
        try:
            offer = dice.table("offer",dice.name,False,1,"",id).json["rows"]
            if len(offer) != 0:
                self.assertEqual( offer[0]["id"] , id, "not this game id")
                return offer[0]
        except errors.Error as e:
            print("except errors.Error as e: ",e)
        return None

    def get_game_by_id(self, id):
        try:
            game = dice.table("game",dice.name,False,1,"",str(id)).json["rows"]
            if len(game) != 0:
                self.assertEqual( game[0]["id"] , id, "not this game owner")
                return game[0]
        except errors.Error as e:
            print("except errors.Error as e: ",e)
        return None

    def get_global_dice(self):
        global_dice = dice.table("global",dice.name).json["rows"]
        return global_dice

    def get_account(self):
        try:
            account = dice.table("account",dice.name).json["rows"]
            return account
        except errors.Error as e:
            print("except errors.Error as e: ",e)
        return None

    def test_01(self):
        # init dice contract
        self.deploy_contract()

        # updaete auth
        self.updateauth(alice.name)
        self.updateauth(bob.name)

        # deposit
        self.deposit(alice.name,"100.0000 EOS")
        self.deposit(bob.name,"100.0000 EOS")
        account = self.get_account()
        print(account)

        # start game
        source1 = "28349b1d4bcdc9905e4ef9719019e55743c84efa0c5e9a0b077f0b54fcd84905"
        commitment1 = "d533f24d6f28ddcef3f066474f7b8355383e485681ba8e793e037f5cf36e4883"
        source2 = "15fe76d25e124b08feb835f12e00a879bd15666a33786e64b655891fba7d6c12"
        commitment2 = "50ed53fcdaf27f88d51ea4e835b1055efe779bb87e6cfdff47d28c88ffb27129"
        self.offerbet("3.0000 EOS",alice.name,commitment1)
        offer = self.get_offer_by_commitment(commitment1)
        print(offer)

        self.offerbet("3.0000 EOS",bob.name,commitment2)
        offer2 = self.get_offer_by_commitment(commitment2)
        print(offer2)

        game = self.get_game_by_id(offer2["gameid"])
        print(game)

        self.reveal(commitment1,source1,alice.name)
        game = self.get_game_by_id(offer2["gameid"])
        print(game)

        self.reveal(commitment2,source2,bob.name)

        # show result
        account = self.get_account()
        print(account)

        # show global value
        print(self.get_global_dice())

    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
       # stop()
       pass



if __name__ == "__main__":
    unittest.main()
