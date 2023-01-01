import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class NFT_REDPACK(CreateAccount):
	def __init__(self,contract_name="nft.redpack"):
		self.name = contract_name
		master = new_master_account()
		nft_redpack = new_account(master,contract_name,factory=True)
		smart = Contract(nft_redpack, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "nft.redpack/nft.redpack.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "nft.redpack/nft.redpack.abi")
		smart.deploy()
		self = nft_redpack
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			nft_redpack_init(self)
		except:
			print("nft_redpack setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def addfee(self,fee="0.10000000 AMAX",fee_contract='user1',nft_contract='user1',submitter_="admin",expect_asset=True):
		self.pushaction("addfee",{"fee":fee,"fee_contract":fee_contract,"nft_contract":nft_contract,},submitter_,expect_asset=expect_asset) 

	def cancel(self,code='user1',submitter_="admin",expect_asset=True):
		self.pushaction("cancel",{"code":code,},submitter_,expect_asset=expect_asset) 

	def claimredpack(self,claimer='user1',code='user1',pwhash='x',submitter_="admin",expect_asset=True):
		self.pushaction("claimredpack",{"claimer":claimer,"code":code,"pwhash":pwhash,},submitter_,expect_asset=expect_asset) 

	def delclaims(self,max_rows=1,submitter_="admin",expect_asset=True):
		self.pushaction("delclaims",{"max_rows":max_rows,},submitter_,expect_asset=expect_asset) 

	def delfee(self,nft_contract='user1',submitter_="admin",expect_asset=True):
		self.pushaction("delfee",{"nft_contract":nft_contract,},submitter_,expect_asset=expect_asset) 

	def delredpacks(self,code='user1',submitter_="admin",expect_asset=True):
		self.pushaction("delredpacks",{"code":code,},submitter_,expect_asset=expect_asset) 

	def setconf(self,admin='user1',hours=1,enable_did='true',submitter_="admin",expect_asset=True):
		self.pushaction("setconf",{"admin":admin,"hours":hours,"enable_did":enable_did,},submitter_,expect_asset=expect_asset) 

	def get_claims(self,scope):
		return self.table("claims",scope).json

	def get_fees(self,scope):
		return self.table("fees",scope).json

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_redpacks(self,scope):
		return self.table("redpacks",scope).json
