import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class AMAX_SAVE(CreateAccount):
	def __init__(self,contract_name="amax.save"):
		self.name = contract_name
		master = new_master_account()
		amax_save = new_account(master,contract_name)
		smart = Contract(amax_save, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "apollo/amax.save/amax.save.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "apollo/amax.save/amax.save.abi")
		smart.deploy()
		self = amax_save
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			amax_save_init(self)
		except:
			print("amax_save setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def collectint(self,issuer='user1',owner='user1',save_id=1,suber="admin",expect_asset=True):
		self.pushaction("collectint",{"issuer":issuer,"owner":owner,"save_id":save_id,},suber,expect_asset=expect_asset) 

	def delplan(self,plan_id=1,suber="admin",expect_asset=True):
		self.pushaction("delplan",{"plan_id":plan_id,},suber,expect_asset=expect_asset) 

	def init(self,admin='user1',ptoken=[],itoken=[],pc=[],mini_deposit_amount="0.10000000 AMAX",share_pool_id=1,suber="admin",expect_asset=True):
		self.pushaction("init",{"admin":admin,"ptoken":ptoken,"itoken":itoken,"pc":pc,"mini_deposit_amount":mini_deposit_amount,"share_pool_id":share_pool_id,},suber,expect_asset=expect_asset) 

	def intcolllog(self,account='user1',account_id=1,plan_id=1,quantity="0.10000000 AMAX",created_at=[],suber="admin",expect_asset=True):
		self.pushaction("intcolllog",{"account":account,"account_id":account_id,"plan_id":plan_id,"quantity":quantity,"created_at":created_at,},suber,expect_asset=expect_asset) 

	def intrefuellog(self,refueller='user1',plan_id=1,quantity="0.10000000 AMAX",created_at=[],suber="admin",expect_asset=True):
		self.pushaction("intrefuellog",{"refueller":refueller,"plan_id":plan_id,"quantity":quantity,"created_at":created_at,},suber,expect_asset=expect_asset) 

	def setplan(self,plan_id=1,pc=[],suber="admin",expect_asset=True):
		self.pushaction("setplan",{"plan_id":plan_id,"pc":pc,},suber,expect_asset=expect_asset) 

	def withdraw(self,issuer='user1',owner='user1',save_id=1,suber="admin",expect_asset=True):
		self.pushaction("withdraw",{"issuer":issuer,"owner":owner,"save_id":save_id,},suber,expect_asset=expect_asset) 

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_saveaccounts(self,scope):
		return self.table("saveaccounts",scope).json

	def get_saveplans(self,scope):
		return self.table("saveplans",scope).json
