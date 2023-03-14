import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class PASS_MART(CreateAccount):
	def __init__(self,contract_name="pass.mart"):
		self.name = contract_name
		master = new_master_account()
		pass_mart = new_account(master,contract_name,factory=True)
		smart = Contract(pass_mart, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "pass.mart/pass.mart.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "pass.mart/pass.mart.abi")
		smart.deploy()
		self = pass_mart
		self.set_account_permission(add_code=True)
    
	def setup(self):
		pass_mart_init(self)
		return self

	def __str__(self):
		return self.name
            

	def addpass(self,owner='user1',title='x',nft_symbol=[],gift_symbol=[],price="0.10000000 AMAX",started_at=[],ended_at=[],custody_plan_id=1,token_split_plan_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("addpass",{"owner":owner,"title":title,"nft_symbol":nft_symbol,"gift_symbol":gift_symbol,"price":price,"started_at":started_at,"ended_at":ended_at,"custody_plan_id":custody_plan_id,"token_split_plan_id":token_split_plan_id,},submitter_,expect_asset=expect_asset) 

	def closepass(self,pass_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("closepass",{"pass_id":pass_id,},submitter_,expect_asset=expect_asset) 

	def init(self,admin='user1',nft_contract='user1',gift_nft_contract='user1',custody_contract='user1',token_split_contract='user1',submitter_="admin",expect_asset=True):
		self.pushaction("init",{"admin":admin,"nft_contract":nft_contract,"gift_nft_contract":gift_nft_contract,"custody_contract":custody_contract,"token_split_contract":token_split_contract,},submitter_,expect_asset=expect_asset) 

	def ordertrace(self,order=[],submitter_="admin",expect_asset=True):
		self.pushaction("ordertrace",{"order":order,},submitter_,expect_asset=expect_asset) 

	def setendtime(self,pass_id=1,sell_ended_at=[],submitter_="admin",expect_asset=True):
		self.pushaction("setendtime",{"pass_id":pass_id,"sell_ended_at":sell_ended_at,},submitter_,expect_asset=expect_asset) 

	def setowner(self,pass_id=1,owner='user1',submitter_="admin",expect_asset=True):
		self.pushaction("setowner",{"pass_id":pass_id,"owner":owner,},submitter_,expect_asset=expect_asset) 

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_passes(self,scope):
		return self.table("passes",scope).json
