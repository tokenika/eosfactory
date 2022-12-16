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
		rndnft_mart = new_account(master,contract_name)
		smart = Contract(rndnft_mart, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "nftone/rndnft.mart/rndnft.mart.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "nftone/rndnft.mart/rndnft.mart.abi")
		smart.deploy()
		self = rndnft_mart
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			rndnft_mart_init(self)
		except:
			print("rndnft_mart setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def closebooth(self,owner='user1',booth_id=1,suber="admin",expect_asset=True):
		self.pushaction("closebooth",{"owner":owner,"booth_id":booth_id,},suber,expect_asset=expect_asset) 

	def createbooth(self,owner='user1',title='x',nft_contract='user1',fund_contract='user1',split_plan_id=1,price="0.10000000 AMAX",opened_at=[],duration_days=1,suber="admin",expect_asset=True):
		self.pushaction("createbooth",{"owner":owner,"title":title,"nft_contract":nft_contract,"fund_contract":fund_contract,"split_plan_id":split_plan_id,"price":price,"opened_at":opened_at,"duration_days":duration_days,},suber,expect_asset=expect_asset) 

	def dealtrace(self,trace=[],suber="admin",expect_asset=True):
		self.pushaction("dealtrace",{"trace":trace,},suber,expect_asset=expect_asset) 

	def delboothbox(self,booth_id=1,nsymb=[],suber="admin",expect_asset=True):
		self.pushaction("delboothbox",{"booth_id":booth_id,"nsymb":nsymb,},suber,expect_asset=expect_asset) 

	def enablebooth(self,owner='user1',booth_id=1,enabled='true',suber="admin",expect_asset=True):
		self.pushaction("enablebooth",{"owner":owner,"booth_id":booth_id,"enabled":enabled,},suber,expect_asset=expect_asset) 

	def fixboothbox(self,booth_id=1,nfts=[],suber="admin",expect_asset=True):
		self.pushaction("fixboothbox",{"booth_id":booth_id,"nfts":nfts,},suber,expect_asset=expect_asset) 

	def init(self,admin='user1',fund_distributor='user1',suber="admin",expect_asset=True):
		self.pushaction("init",{"admin":admin,"fund_distributor":fund_distributor,},suber,expect_asset=expect_asset) 

	def setboothtime(self,owner='user1',booth_id=1,opened_at=[],closed_at=[],suber="admin",expect_asset=True):
		self.pushaction("setboothtime",{"owner":owner,"booth_id":booth_id,"opened_at":opened_at,"closed_at":closed_at,},suber,expect_asset=expect_asset) 

	def get_boothboxes(self,scope):
		return self.table("boothboxes",scope).json

	def get_booths(self,scope):
		return self.table("booths",scope).json

	def get_global(self,scope):
		return self.table("global",scope).json
