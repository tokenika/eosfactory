import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class OTCSETTLE(CreateAccount):
	def __init__(self,contract_name="otcsettle"):
		self.name = contract_name
		master = new_master_account()
		otcsettle = new_account(master,contract_name,factory=True)
		smart = Contract(otcsettle, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "otcsettle/otcsettle.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "otcsettle/otcsettle.abi")
		smart.deploy()
		self = otcsettle
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			otcsettle_init(self)
		except:
			print("otcsettle setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def claim(self,reciptian='user1',rewards=1,submitter_="admin",expect_asset=True):
		self.pushaction("claim",{"reciptian":reciptian,"rewards":rewards,},submitter_,expect_asset=expect_asset) 

	def deal(self,deal_id=1,merchant='user1',user='user1',quantity="0.10000000 AMAX",fee="0.10000000 AMAX",arbit_status=1,start_at=[],end_at=[],submitter_="admin",expect_asset=True):
		self.pushaction("deal",{"deal_id":deal_id,"merchant":merchant,"user":user,"quantity":quantity,"fee":fee,"arbit_status":arbit_status,"start_at":start_at,"end_at":end_at,},submitter_,expect_asset=expect_asset) 

	def setconf(self,conf_contract='user1',submitter_="admin",expect_asset=True):
		self.pushaction("setconf",{"conf_contract":conf_contract,},submitter_,expect_asset=expect_asset) 

	def setlevel(self,user='user1',level=1,submitter_="admin",expect_asset=True):
		self.pushaction("setlevel",{"user":user,"level":level,},submitter_,expect_asset=expect_asset) 

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_rewards(self,scope):
		return self.table("rewards",scope).json

	def get_settles(self,scope):
		return self.table("settles",scope).json
