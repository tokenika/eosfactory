import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class AMAX_IDO(CreateAccount):
	def __init__(self,contract_name="amax.ido"):
		self.name = contract_name
		master = new_master_account()
		amax_ido = new_account(master,contract_name,factory=True)
		smart = Contract(amax_ido, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.ido/amax.ido.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.ido/amax.ido.abi")
		smart.deploy()
		self = amax_ido
		self.set_account_permission(add_code=True)
    
	def setup(self):
		amax_ido_init(self)
		return self

	def __str__(self):
		return self.name
            

	def init(self,admin='user1',submitter_="admin",expect_asset=True):
		self.pushaction("init",{"admin":admin,},submitter_,expect_asset=expect_asset) 

	def setprice(self,price="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("setprice",{"price":price,},submitter_,expect_asset=expect_asset) 

	def get_global(self,scope):
		return self.table("global",scope).json
