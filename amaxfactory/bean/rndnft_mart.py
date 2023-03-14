import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class RNDNFT_MART(CreateAccount):
	def __init__(self,contract_name="rndnft.mart"):
		self.name = contract_name
		master = new_master_account()
		rndnft_mart = new_account(master,contract_name,factory=True)
		smart = Contract(rndnft_mart, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "rndnft.mart/rndnft.mart.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "rndnft.mart/rndnft.mart.abi")
		smart.deploy()
		self = rndnft_mart
		self.set_account_permission(add_code=True)
    
	def setup(self):
		rndnft_mart_init(self)
		return self

	def __str__(self):
		return self.name
            

	def closebooth(self,owner='user1',booth_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("closebooth",{"owner":owner,"booth_id":booth_id,},submitter_,expect_asset=expect_asset) 

	def createbooth(self,owner='user1',title='x',nft_contract='user1',fund_contract='user1',split_plan_id=1,price="0.10000000 AMAX",opened_at=[],duration_days=1,submitter_="admin",expect_asset=True):
		self.pushaction("createbooth",{"owner":owner,"title":title,"nft_contract":nft_contract,"fund_contract":fund_contract,"split_plan_id":split_plan_id,"price":price,"opened_at":opened_at,"duration_days":duration_days,},submitter_,expect_asset=expect_asset) 

	def dealtrace(self,trace=[],submitter_="admin",expect_asset=True):
		self.pushaction("dealtrace",{"trace":trace,},submitter_,expect_asset=expect_asset) 

	def delboothbox(self,booth_id=1,nsymb=[],submitter_="admin",expect_asset=True):
		self.pushaction("delboothbox",{"booth_id":booth_id,"nsymb":nsymb,},submitter_,expect_asset=expect_asset) 

	def enablebooth(self,owner='user1',booth_id=1,enabled='true',submitter_="admin",expect_asset=True):
		self.pushaction("enablebooth",{"owner":owner,"booth_id":booth_id,"enabled":enabled,},submitter_,expect_asset=expect_asset) 

	def fixboothbox(self,booth_id=1,nfts=[],submitter_="admin",expect_asset=True):
		self.pushaction("fixboothbox",{"booth_id":booth_id,"nfts":nfts,},submitter_,expect_asset=expect_asset) 

	def init(self,admin='user1',fund_distributor='user1',submitter_="admin",expect_asset=True):
		self.pushaction("init",{"admin":admin,"fund_distributor":fund_distributor,},submitter_,expect_asset=expect_asset) 

	def setboothtime(self,owner='user1',booth_id=1,opened_at=[],closed_at=[],submitter_="admin",expect_asset=True):
		self.pushaction("setboothtime",{"owner":owner,"booth_id":booth_id,"opened_at":opened_at,"closed_at":closed_at,},submitter_,expect_asset=expect_asset) 

	def get_boothboxes(self,scope):
		return self.table("boothboxes",scope).json

	def get_booths(self,scope):
		return self.table("booths",scope).json

	def get_global(self,scope):
		return self.table("global",scope).json
