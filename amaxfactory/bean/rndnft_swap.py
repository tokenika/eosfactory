import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class RNDNFT_SWAP(CreateAccount):
	def __init__(self,contract_name="rndnft.swap"):
		self.name = contract_name
		master = new_master_account()
		rndnft_swap = new_account(master,contract_name)
		smart = Contract(rndnft_swap, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "nftone/rndnft.swap/rndnft.swap.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "nftone/rndnft.swap/rndnft.swap.abi")
		smart.deploy()
		self = rndnft_swap
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			rndnft_swap_init(self)
		except:
			print("rndnft_swap setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def closebooth(self,owner='user1',quote_nft_contract='user1',symbol_id=1,suber="admin",expect_asset=True):
		self.pushaction("closebooth",{"owner":owner,"quote_nft_contract":quote_nft_contract,"symbol_id":symbol_id,},suber,expect_asset=expect_asset) 

	def createbooth(self,conf=[],suber="admin",expect_asset=True):
		self.pushaction("createbooth",{"conf":conf,},suber,expect_asset=expect_asset) 

	def dealtrace(self,trace=[],suber="admin",expect_asset=True):
		self.pushaction("dealtrace",{"trace":trace,},suber,expect_asset=expect_asset) 

	def enablebooth(self,owner='user1',quote_nft_contract='user1',symbol_id=1,enabled='true',suber="admin",expect_asset=True):
		self.pushaction("enablebooth",{"owner":owner,"quote_nft_contract":quote_nft_contract,"symbol_id":symbol_id,"enabled":enabled,},suber,expect_asset=expect_asset) 

	def init(self,admin='user1',suber="admin",expect_asset=True):
		self.pushaction("init",{"admin":admin,},suber,expect_asset=expect_asset) 

	def setboothtime(self,owner='user1',quote_nft_contract='user1',symbol_id=1,opened_at=[],closed_at=[],suber="admin",expect_asset=True):
		self.pushaction("setboothtime",{"owner":owner,"quote_nft_contract":quote_nft_contract,"symbol_id":symbol_id,"opened_at":opened_at,"closed_at":closed_at,},suber,expect_asset=expect_asset) 

	def get_boothboxes(self,scope):
		return self.table("boothboxes",scope).json

	def get_booths(self,scope):
		return self.table("booths",scope).json

	def get_global(self,scope):
		return self.table("global",scope).json
