import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class OTCSWAP(CreateAccount):
	def __init__(self,contract_name="otcswap"):
		self.name = contract_name
		master = new_master_account()
		otcswap = new_account(master,contract_name)
		smart = Contract(otcswap, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "otcswap/otcswap.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "otcswap/otcswap.abi")
		smart.deploy()
		self = otcswap
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			otcswap_init(self)
		except:
			print("otcswap setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def setconf(self,conf_contract='user1',suber="admin",expect_asset=True):
		self.pushaction("setconf",{"conf_contract":conf_contract,},suber,expect_asset=expect_asset) 

	def settleto(self,user='user1',fee="0.10000000 AMAX",quantity="0.10000000 AMAX",suber="admin",expect_asset=True):
		self.pushaction("settleto",{"user":user,"fee":fee,"quantity":quantity,},suber,expect_asset=expect_asset) 

	def get_accounts(self,scope):
		return self.table("accounts",scope).json

	def get_global(self,scope):
		return self.table("global",scope).json
