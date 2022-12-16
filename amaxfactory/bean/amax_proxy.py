import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class AMAX_PROXY(CreateAccount):
	def __init__(self,contract_name="amax.proxy"):
		self.name = contract_name
		master = new_master_account()
		amax_proxy = new_account(master,contract_name)
		smart = Contract(amax_proxy, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.proxy/amax.proxy.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.proxy/amax.proxy.abi")
		smart.deploy()
		self = amax_proxy
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			amax_proxy_init(self)
		except:
			print("amax_proxy setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def init(self,amax_recover='user1',suber="admin",expect_asset=True):
		self.pushaction("init",{"amax_recover":amax_recover,},suber,expect_asset=expect_asset) 

	def newaccount(self,auth_contract='user1',creator='user1',account='user1',active=[],suber="admin",expect_asset=True):
		self.pushaction("newaccount",{"auth_contract":auth_contract,"creator":creator,"account":account,"active":active,},suber,expect_asset=expect_asset) 

	def updateauth(self,account='user1',pubkey=[],suber="admin",expect_asset=True):
		self.pushaction("updateauth",{"account":account,"pubkey":pubkey,},suber,expect_asset=expect_asset) 

	def get_global(self,scope):
		return self.table("global",scope).json
