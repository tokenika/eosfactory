import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class TG_BIND(CreateAccount):
	def __init__(self,contract_name="tg.bind"):
		self.name = contract_name
		master = new_master_account()
		tg_bind = new_account(master,contract_name)
		smart = Contract(tg_bind, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "tg/tg.bind/tg.bind.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "tg/tg.bind/tg.bind.abi")
		smart.deploy()
		self = tg_bind
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			tg_bind_init(self)
		except:
			print("tg_bind setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def bind(self,account='user1',tgid=1,suber="admin",expect_asset=True):
		self.pushaction("bind",{"account":account,"tgid":tgid,},suber,expect_asset=expect_asset) 

	def confirm(self,tgid=1,suber="admin",expect_asset=True):
		self.pushaction("confirm",{"tgid":tgid,},suber,expect_asset=expect_asset) 

	def delbind(self,tgid=1,suber="admin",expect_asset=True):
		self.pushaction("delbind",{"tgid":tgid,},suber,expect_asset=expect_asset) 

	def init(self,account='user1',suber="admin",expect_asset=True):
		self.pushaction("init",{"account":account,},suber,expect_asset=expect_asset) 

	def get_binds(self,scope):
		return self.table("binds",scope).json

	def get_global(self,scope):
		return self.table("global",scope).json
