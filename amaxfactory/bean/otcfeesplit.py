import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class OTCFEESPLIT(CreateAccount):
	def __init__(self,contract_name="otcfeesplit"):
		self.name = contract_name
		master = new_master_account()
		otcfeesplit = new_account(master,contract_name,factory=True)
		smart = Contract(otcfeesplit, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "otcfeesplit/otcfeesplit.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "otcfeesplit/otcfeesplit.abi")
		smart.deploy()
		self = otcfeesplit
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			otcfeesplit_init(self)
		except:
			print("otcfeesplit setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def init(self,admin='user1',submitter_="admin",expect_asset=True):
		self.pushaction("init",{"admin":admin,},submitter_,expect_asset=expect_asset) 

	def setratios(self,ratios=1,to_add='true',submitter_="admin",expect_asset=True):
		self.pushaction("setratios",{"ratios":ratios,"to_add":to_add,},submitter_,expect_asset=expect_asset) 

	def get_global(self,scope):
		return self.table("global",scope).json
