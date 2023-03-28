import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class AMAX_ONE(CreateAccount):
	def __init__(self,contract_name="amax.one"):
		self.name = contract_name
		master = new_master_account()
		amax_one = new_account(master,contract_name,factory=True)
		smart = Contract(amax_one, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.one/amax.one.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.one/amax.one.abi")
		smart.deploy()
		self = amax_one
		self.set_account_permission(add_code=True)
    
	def setup(self):
		amax_one_init(self)
		return self

	def __str__(self):
		return self.name
            

	def addswapconf(self,account='user1',amount=1,swap_tokens="0.10000000 AMAX",swap_tokens_after_adscheck="0.10000000 AMAX",total_amount="0.10000000 AMAX",remain_amount="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("addswapconf",{"account":account,"amount":amount,"swap_tokens":swap_tokens,"swap_tokens_after_adscheck":swap_tokens_after_adscheck,"total_amount":total_amount,"remain_amount":remain_amount,},submitter_,expect_asset=expect_asset) 

	def aplswaplog(self,miner='user1',recd_apls="0.10000000 AMAX",swap_tokens="0.10000000 AMAX",ads_id='x',created_at=[],submitter_="admin",expect_asset=True):
		self.pushaction("aplswaplog",{"miner":miner,"recd_apls":recd_apls,"swap_tokens":swap_tokens,"ads_id":ads_id,"created_at":created_at,},submitter_,expect_asset=expect_asset) 

	def confirmads(self,order_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("confirmads",{"order_id":order_id,},submitter_,expect_asset=expect_asset) 

	def delswapconf(self,account='user1',amount=1,submitter_="admin",expect_asset=True):
		self.pushaction("delswapconf",{"account":account,"amount":amount,},submitter_,expect_asset=expect_asset) 

	def init(self,admin='user1',mine_token_contract='user1',started_at=[],ended_at=[],submitter_="admin",expect_asset=True):
		self.pushaction("init",{"admin":admin,"mine_token_contract":mine_token_contract,"started_at":started_at,"ended_at":ended_at,},submitter_,expect_asset=expect_asset) 

	def onswapexpird(self,order_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("onswapexpird",{"order_id":order_id,},submitter_,expect_asset=expect_asset) 

	def setremained(self,swap_conf_id=1,amount="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("setremained",{"swap_conf_id":swap_conf_id,"amount":amount,},submitter_,expect_asset=expect_asset) 

	def get_adsorder(self,scope):
		return self.table("adsorder",scope).json

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_swapconfs(self,scope):
		return self.table("swapconfs",scope).json
