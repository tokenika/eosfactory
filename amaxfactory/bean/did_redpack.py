import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class DID_REDPACK(CreateAccount):
	def __init__(self,contract_name="did.redpack"):
		self.name = contract_name
		master = new_master_account()
		did_redpack = new_account(master,contract_name,factory=True)
		smart = Contract(did_redpack, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "did.redpack/did.redpack.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "did.redpack/did.redpack.abi")
		smart.deploy()
		self = did_redpack
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			did_redpack_init(self)
		except:
			print("did_redpack setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def addfee(self,fee="0.10000000 AMAX",contract='user1',min_unit=1,did_contract='user1',did_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("addfee",{"fee":fee,"contract":contract,"min_unit":min_unit,"did_contract":did_contract,"did_id":did_id,},submitter_,expect_asset=expect_asset) 

	def cancel(self,code='user1',submitter_="admin",expect_asset=True):
		self.pushaction("cancel",{"code":code,},submitter_,expect_asset=expect_asset) 

	def claimredpack(self,claimer='user1',code='user1',pwhash='x',submitter_="admin",expect_asset=True):
		self.pushaction("claimredpack",{"claimer":claimer,"code":code,"pwhash":pwhash,},submitter_,expect_asset=expect_asset) 

	def delclaims(self,max_rows=1,submitter_="admin",expect_asset=True):
		self.pushaction("delclaims",{"max_rows":max_rows,},submitter_,expect_asset=expect_asset) 

	def delfee(self,coin='8,AMAX',submitter_="admin",expect_asset=True):
		self.pushaction("delfee",{"coin":coin,},submitter_,expect_asset=expect_asset) 

	def delredpacks(self,code='user1',submitter_="admin",expect_asset=True):
		self.pushaction("delredpacks",{"code":code,},submitter_,expect_asset=expect_asset) 

	def init(self,admin='user1',hours=1,did_supported='true',submitter_="admin",expect_asset=True):
		self.pushaction("init",{"admin":admin,"hours":hours,"did_supported":did_supported,},submitter_,expect_asset=expect_asset) 

	def get_claims(self,scope):
		return self.table("claims",scope).json

	def get_feeconf(self,scope):
		return self.table("feeconf",scope).json

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_redpacks(self,scope):
		return self.table("redpacks",scope).json
