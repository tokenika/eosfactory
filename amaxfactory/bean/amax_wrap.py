import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class AMAX_WRAP(CreateAccount):
	def __init__(self,contract_name="amax.wrap"):
		self.name = contract_name
		master = new_master_account()
		amax_wrap = new_account(master,contract_name)
		smart = Contract(amax_wrap, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.wrap/amax.wrap.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.wrap/amax.wrap.abi")
		smart.deploy()
		self = amax_wrap
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			amax_wrap_init(self)
		except:
			print("amax_wrap setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def exec(self,executer='user1',trx=[],submitter_="admin",expect_asset=True):
		self.pushaction("exec",{"executer":executer,"trx":trx,},submitter_,expect_asset=expect_asset) 
