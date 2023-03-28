import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class AMAX_TWO(CreateAccount):
	def __init__(self,contract_name="amax.two"):
		self.name = contract_name
		master = new_master_account()
		amax_two = new_account(master,contract_name,factory=True)
		smart = Contract(amax_two, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.two/amax.two.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.two/amax.two.abi")
		smart.deploy()
		self = amax_two
		self.set_account_permission(add_code=True)
    
	def setup(self):
		amax_two_init(self)
		return self

	def __str__(self):
		return self.name
            

	def addminetoken(self,account='user1',mine_token_total="0.10000000 AMAX",mine_token_remained="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("addminetoken",{"account":account,"mine_token_total":mine_token_total,"mine_token_remained":mine_token_remained,},submitter_,expect_asset=expect_asset) 

	def aplswaplog(self,miner='user1',recd_apls="0.10000000 AMAX",swap_tokens="0.10000000 AMAX",created_at=[],submitter_="admin",expect_asset=True):
		self.pushaction("aplswaplog",{"miner":miner,"recd_apls":recd_apls,"swap_tokens":swap_tokens,"created_at":created_at,},submitter_,expect_asset=expect_asset) 

	def init(self,admin='user1',mine_token_contract='user1',started_at=[],ended_at=[],mine_token_total="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("init",{"admin":admin,"mine_token_contract":mine_token_contract,"started_at":started_at,"ended_at":ended_at,"mine_token_total":mine_token_total,},submitter_,expect_asset=expect_asset) 

	def get_global(self,scope):
		return self.table("global",scope).json
