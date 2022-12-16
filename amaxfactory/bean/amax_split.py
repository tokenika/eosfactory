import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class AMAX_SPLIT(CreateAccount):
	def __init__(self,contract_name="amax.split"):
		self.name = contract_name
		master = new_master_account()
		amax_split = new_account(master,contract_name)
		smart = Contract(amax_split, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.split/amax.split.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.split/amax.split.abi")
		smart.deploy()
		self = amax_split
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			amax_split_init(self)
		except:
			print("amax_split setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def addplan(self,plan_sender_contract='user1',token_symbol='8,AMAX',split_by_rate='true',suber="admin",expect_asset=True):
		self.pushaction("addplan",{"plan_sender_contract":plan_sender_contract,"token_symbol":token_symbol,"split_by_rate":split_by_rate,},suber,expect_asset=expect_asset) 

	def delplan(self,plan_sender_contract='user1',plan_id=1,suber="admin",expect_asset=True):
		self.pushaction("delplan",{"plan_sender_contract":plan_sender_contract,"plan_id":plan_id,},suber,expect_asset=expect_asset) 

	def init(self,suber="admin",expect_asset=True):
		self.pushaction("init",{},suber,expect_asset=expect_asset) 

	def setplan(self,plan_sender_contract='user1',plan_id=1,conf=[],suber="admin",expect_asset=True):
		self.pushaction("setplan",{"plan_sender_contract":plan_sender_contract,"plan_id":plan_id,"conf":conf,},suber,expect_asset=expect_asset) 

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_splitplans(self,scope):
		return self.table("splitplans",scope).json
