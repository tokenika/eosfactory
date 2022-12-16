import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class AMAX_RECOVER(CreateAccount):
	def __init__(self,contract_name="amax.recover"):
		self.name = contract_name
		master = new_master_account()
		amax_recover = new_account(master,contract_name)
		smart = Contract(amax_recover, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.recover/amax.recover.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.recover/amax.recover.abi")
		smart.deploy()
		self = amax_recover
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			amax_recover_init(self)
		except:
			print("amax_recover setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def addauditconf(self,check_contract='user1',audit_type='user1',conf=[],suber="admin",expect_asset=True):
		self.pushaction("addauditconf",{"check_contract":check_contract,"audit_type":audit_type,"conf":conf,},suber,expect_asset=expect_asset) 

	def addauth(self,account='user1',contract='user1',suber="admin",expect_asset=True):
		self.pushaction("addauth",{"account":account,"contract":contract,},suber,expect_asset=expect_asset) 

	def bindaccount(self,account='user1',default_auth='user1',suber="admin",expect_asset=True):
		self.pushaction("bindaccount",{"account":account,"default_auth":default_auth,},suber,expect_asset=expect_asset) 

	def checkauth(self,auth_contract='user1',account='user1',suber="admin",expect_asset=True):
		self.pushaction("checkauth",{"auth_contract":auth_contract,"account":account,},suber,expect_asset=expect_asset) 

	def closeorder(self,submitter='user1',order_id=1,suber="admin",expect_asset=True):
		self.pushaction("closeorder",{"submitter":submitter,"order_id":order_id,},suber,expect_asset=expect_asset) 

	def createorder(self,sn=1,auth_contract='user1',account='user1',manual_check_required='true',score=1,recover_target=[],suber="admin",expect_asset=True):
		self.pushaction("createorder",{"sn":sn,"auth_contract":auth_contract,"account":account,"manual_check_required":manual_check_required,"score":score,"recover_target":recover_target,},suber,expect_asset=expect_asset) 

	def delauditconf(self,contract_name='user1',suber="admin",expect_asset=True):
		self.pushaction("delauditconf",{"contract_name":contract_name,},suber,expect_asset=expect_asset) 

	def delorder(self,submitter='user1',order_id=1,suber="admin",expect_asset=True):
		self.pushaction("delorder",{"submitter":submitter,"order_id":order_id,},suber,expect_asset=expect_asset) 

	def init(self,recover_threshold=1,amax_proxy_contract='user1',suber="admin",expect_asset=True):
		self.pushaction("init",{"recover_threshold":recover_threshold,"amax_proxy_contract":amax_proxy_contract,},suber,expect_asset=expect_asset) 

	def setscore(self,auth_contract='user1',account='user1',order_id=1,score=1,suber="admin",expect_asset=True):
		self.pushaction("setscore",{"auth_contract":auth_contract,"account":account,"order_id":order_id,"score":score,},suber,expect_asset=expect_asset) 

	def test(self,count=1,suber="admin",expect_asset=True):
		self.pushaction("test",{"count":count,},suber,expect_asset=expect_asset) 

	def get_auditconf(self,scope):
		return self.table("auditconf",scope).json

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_recauths(self,scope):
		return self.table("recauths",scope).json

	def get_recorders(self,scope):
		return self.table("recorders",scope).json

	def get_regauths(self,scope):
		return self.table("regauths",scope).json
