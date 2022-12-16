import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class MDAO_GOV(CreateAccount):
	def __init__(self,contract_name="mdao.gov"):
		self.name = contract_name
		master = new_master_account()
		mdao_gov = new_account(master,contract_name)
		smart = Contract(mdao_gov, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "mdao/mdao.gov/mdao.gov.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "mdao/mdao.gov/mdao.gov.abi")
		smart.deploy()
		self = mdao_gov
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			mdao_gov_init(self)
		except:
			print("mdao_gov setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def create(self,dao_code='user1',propose_strategy_id=1,vote_strategy_id=1,require_participation=1,require_pass=1,update_interval=1,voting_period=1,suber="admin",expect_asset=True):
		self.pushaction("create",{"dao_code":dao_code,"propose_strategy_id":propose_strategy_id,"vote_strategy_id":vote_strategy_id,"require_participation":require_participation,"require_pass":require_pass,"update_interval":update_interval,"voting_period":voting_period,},suber,expect_asset=expect_asset) 

	def setlocktime(self,dao_code='user1',update_interval=1,suber="admin",expect_asset=True):
		self.pushaction("setlocktime",{"dao_code":dao_code,"update_interval":update_interval,},suber,expect_asset=expect_asset) 

	def setpropmodel(self,dao_code='user1',propose_model='user1',suber="admin",expect_asset=True):
		self.pushaction("setpropmodel",{"dao_code":dao_code,"propose_model":propose_model,},suber,expect_asset=expect_asset) 

	def setproposestg(self,dao_code='user1',propose_strategy_id=1,suber="admin",expect_asset=True):
		self.pushaction("setproposestg",{"dao_code":dao_code,"propose_strategy_id":propose_strategy_id,},suber,expect_asset=expect_asset) 

	def setvotestg(self,dao_code='user1',vote_strategy_id=1,require_participation=1,require_pass=1,suber="admin",expect_asset=True):
		self.pushaction("setvotestg",{"dao_code":dao_code,"vote_strategy_id":vote_strategy_id,"require_participation":require_participation,"require_pass":require_pass,},suber,expect_asset=expect_asset) 

	def setvotetime(self,dao_code='user1',voting_period=1,suber="admin",expect_asset=True):
		self.pushaction("setvotetime",{"dao_code":dao_code,"voting_period":voting_period,},suber,expect_asset=expect_asset) 

	def get_governances(self,scope):
		return self.table("governances",scope).json
