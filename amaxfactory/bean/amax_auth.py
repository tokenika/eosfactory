import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class AMAX_AUTH(CreateAccount):
	def __init__(self,contract_name="amax.auth"):
		self.name = contract_name
		master = new_master_account()
		amax_auth = new_account(master,contract_name)
		smart = Contract(amax_auth, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.auth/amax.auth.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.auth/amax.auth.abi")
		smart.deploy()
		self = amax_auth
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			amax_auth_init(self)
		except:
			print("amax_auth setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def bindinfo(self,admin='user1',account='user1',info='x',suber="admin",expect_asset=True):
		self.pushaction("bindinfo",{"admin":admin,"account":account,"info":info,},suber,expect_asset=expect_asset) 

	def createorder(self,sn=1,admin='user1',account='user1',manual_check_required='true',score=1,recover_target=[],suber="admin",expect_asset=True):
		self.pushaction("createorder",{"sn":sn,"admin":admin,"account":account,"manual_check_required":manual_check_required,"score":score,"recover_target":recover_target,},suber,expect_asset=expect_asset) 

	def delauth(self,account='user1',suber="admin",expect_asset=True):
		self.pushaction("delauth",{"account":account,},suber,expect_asset=expect_asset) 

	def init(self,amax_recover='user1',amax_proxy_contract='user1',suber="admin",expect_asset=True):
		self.pushaction("init",{"amax_recover":amax_recover,"amax_proxy_contract":amax_proxy_contract,},suber,expect_asset=expect_asset) 

	def newaccount(self,admin='user1',creator='user1',account='user1',info='x',active=[],suber="admin",expect_asset=True):
		self.pushaction("newaccount",{"admin":admin,"creator":creator,"account":account,"info":info,"active":active,},suber,expect_asset=expect_asset) 

	def setauth(self,account='user1',actions=[],suber="admin",expect_asset=True):
		self.pushaction("setauth",{"account":account,"actions":actions,},suber,expect_asset=expect_asset) 

	def setscore(self,admin='user1',account='user1',order_id=1,score=1,suber="admin",expect_asset=True):
		self.pushaction("setscore",{"admin":admin,"account":account,"order_id":order_id,"score":score,},suber,expect_asset=expect_asset) 

	def get_acctrealme(self,scope):
		return self.table("acctrealme",scope).json

	def get_auths(self,scope):
		return self.table("auths",scope).json

	def get_global(self,scope):
		return self.table("global",scope).json
