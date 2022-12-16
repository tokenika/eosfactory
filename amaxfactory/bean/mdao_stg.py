import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class MDAO_STG(CreateAccount):
	def __init__(self,contract_name="mdao.stg"):
		self.name = contract_name
		master = new_master_account()
		mdao_stg = new_account(master,contract_name)
		smart = Contract(mdao_stg, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "mdao.stg/mdao.stg.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "mdao.stg/mdao.stg.abi")
		smart.deploy()
		self = mdao_stg
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			mdao_stg_init(self)
		except:
			print("mdao_stg setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def balancestg(self,creator='user1',stg_name='x',weight_value=1,type='user1',ref_contract='user1',ref_sym=[],submitter_="admin",expect_asset=True):
		self.pushaction("balancestg",{"creator":creator,"stg_name":stg_name,"weight_value":weight_value,"type":type,"ref_contract":ref_contract,"ref_sym":ref_sym,},submitter_,expect_asset=expect_asset) 

	def create(self,creator='user1',stg_name='x',stg_algo='x',type='user1',ref_contract='user1',ref_sym=[],submitter_="admin",expect_asset=True):
		self.pushaction("create",{"creator":creator,"stg_name":stg_name,"stg_algo":stg_algo,"type":type,"ref_contract":ref_contract,"ref_sym":ref_sym,},submitter_,expect_asset=expect_asset) 

	def publish(self,creator='user1',stg_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("publish",{"creator":creator,"stg_id":stg_id,},submitter_,expect_asset=expect_asset) 

	def remove(self,creator='user1',stg_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("remove",{"creator":creator,"stg_id":stg_id,},submitter_,expect_asset=expect_asset) 

	def setalgo(self,creator='user1',stg_id=1,stg_algo='x',submitter_="admin",expect_asset=True):
		self.pushaction("setalgo",{"creator":creator,"stg_id":stg_id,"stg_algo":stg_algo,},submitter_,expect_asset=expect_asset) 

	def testalgo(self,account='user1',stg_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("testalgo",{"account":account,"stg_id":stg_id,},submitter_,expect_asset=expect_asset) 

	def thresholdstg(self,creator='user1',stg_name='x',threshold_value=1,type='user1',ref_contract='user1',ref_sym=[],submitter_="admin",expect_asset=True):
		self.pushaction("thresholdstg",{"creator":creator,"stg_name":stg_name,"threshold_value":threshold_value,"type":type,"ref_contract":ref_contract,"ref_sym":ref_sym,},submitter_,expect_asset=expect_asset) 

	def verify(self,creator='user1',stg_id=1,value=1,expect_weight=1,submitter_="admin",expect_asset=True):
		self.pushaction("verify",{"creator":creator,"stg_id":stg_id,"value":value,"expect_weight":expect_weight,},submitter_,expect_asset=expect_asset) 

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_stglist(self,scope):
		return self.table("stglist",scope).json
