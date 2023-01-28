import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class MDAO_STAKE(CreateAccount):
	def __init__(self,contract_name="mdao.stake"):
		self.name = contract_name
		master = new_master_account()
		mdao_stake = new_account(master,contract_name,factory=True)
		smart = Contract(mdao_stake, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "mdao.stake/mdao.stake.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "mdao.stake/mdao.stake.abi")
		smart.deploy()
		self = mdao_stake
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			mdao_stake_init(self)
		except:
			print("mdao_stake setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def extendlock(self,manager='user1',id=1,locktime=1,submitter_="admin",expect_asset=True):
		self.pushaction("extendlock",{"manager":manager,"id":id,"locktime":locktime,},submitter_,expect_asset=expect_asset) 

	def init(self,managers=[],supported_tokens=[],submitter_="admin",expect_asset=True):
		self.pushaction("init",{"managers":managers,"supported_tokens":supported_tokens,},submitter_,expect_asset=expect_asset) 

	def unstakenft(self,id=1,nfts=[],submitter_="admin",expect_asset=True):
		self.pushaction("unstakenft",{"id":id,"nfts":nfts,},submitter_,expect_asset=expect_asset) 

	def unstaketoken(self,id=1,tokens=[],submitter_="admin",expect_asset=True):
		self.pushaction("unstaketoken",{"id":id,"tokens":tokens,},submitter_,expect_asset=expect_asset) 

	def get_daostake(self,scope):
		return self.table("daostake",scope).json

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_usrstake(self,scope):
		return self.table("usrstake",scope).json
