import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class APLINK_NEWBIE(CreateAccount):
	def __init__(self,contract_name="aplink.newbie"):
		self.name = contract_name
		master = new_master_account()
		aplink_newbie = new_account(master,contract_name)
		smart = Contract(aplink_newbie, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "aplink/aplink.newbie/aplink.newbie.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "aplink/aplink.newbie/aplink.newbie.abi")
		smart.deploy()
		self = aplink_newbie
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			aplink_newbie_init(self)
		except:
			print("aplink_newbie setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def claimreward(self,newbies=[],suber="admin",expect_asset=True):
		self.pushaction("claimreward",{"newbies":newbies,},suber,expect_asset=expect_asset) 

	def init(self,lease_id=1,farm_contract='user1',suber="admin",expect_asset=True):
		self.pushaction("init",{"lease_id":lease_id,"farm_contract":farm_contract,},suber,expect_asset=expect_asset) 

	def rewardinvite(self,to='user1',suber="admin",expect_asset=True):
		self.pushaction("rewardinvite",{"to":to,},suber,expect_asset=expect_asset) 

	def setbatchsize(self,batch_issue_size=1,suber="admin",expect_asset=True):
		self.pushaction("setbatchsize",{"batch_issue_size":batch_issue_size,},suber,expect_asset=expect_asset) 

	def setleaseid(self,suber="admin",expect_asset=True):
		self.pushaction("setleaseid",{},suber,expect_asset=expect_asset) 

	def setstate(self,newbie_reward="0.10000000 AMAX",aplink_token_contract='user1',aplink_admin='user1',suber="admin",expect_asset=True):
		self.pushaction("setstate",{"newbie_reward":newbie_reward,"aplink_token_contract":aplink_token_contract,"aplink_admin":aplink_admin,},suber,expect_asset=expect_asset) 

	def get_global(self,scope):
		return self.table("global",scope).json
