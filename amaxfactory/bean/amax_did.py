import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class AMAX_DID(CreateAccount):
	def __init__(self,contract_name="amax.did"):
		self.name = contract_name
		master = new_master_account()
		amax_did = new_account(master,contract_name)
		smart = Contract(amax_did, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.did/amax.did.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.did/amax.did.abi")
		smart.deploy()
		self = amax_did
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			amax_did_init(self)
		except:
			print("amax_did setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def addvendor(self,vendor_name='x',vendor_account='user1',kyc_level=1,user_reward_quant="0.10000000 AMAX",user_charge_quant="0.10000000 AMAX",nft_id=[],submitter_="admin",expect_asset=True):
		self.pushaction("addvendor",{"vendor_name":vendor_name,"vendor_account":vendor_account,"kyc_level":kyc_level,"user_reward_quant":user_reward_quant,"user_charge_quant":user_charge_quant,"nft_id":nft_id,},submitter_,expect_asset=expect_asset) 

	def auditlog(self,order_id=1,taker='user1',vendor_name='x',vendor_account='user1',kyc_level=1,vendor_charge_quant="0.10000000 AMAX",status='user1',msg='x',created_at=[],submitter_="admin",expect_asset=True):
		self.pushaction("auditlog",{"order_id":order_id,"taker":taker,"vendor_name":vendor_name,"vendor_account":vendor_account,"kyc_level":kyc_level,"vendor_charge_quant":vendor_charge_quant,"status":status,"msg":msg,"created_at":created_at,},submitter_,expect_asset=expect_asset) 

	def chgvendor(self,vendor_id=1,status='user1',user_reward_quant="0.10000000 AMAX",user_charge_quant="0.10000000 AMAX",nft_id=[],submitter_="admin",expect_asset=True):
		self.pushaction("chgvendor",{"vendor_id":vendor_id,"status":status,"user_reward_quant":user_reward_quant,"user_charge_quant":user_charge_quant,"nft_id":nft_id,},submitter_,expect_asset=expect_asset) 

	def init(self,admin='user1',nft_contract='user1',fee_colletor='user1',lease_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("init",{"admin":admin,"nft_contract":nft_contract,"fee_colletor":fee_colletor,"lease_id":lease_id,},submitter_,expect_asset=expect_asset) 

	def setadmin(self,admin='user1',submitter_="admin",expect_asset=True):
		self.pushaction("setadmin",{"admin":admin,},submitter_,expect_asset=expect_asset) 

	def setdidstatus(self,order_id=1,status='user1',msg='x',submitter_="admin",expect_asset=True):
		self.pushaction("setdidstatus",{"order_id":order_id,"status":status,"msg":msg,},submitter_,expect_asset=expect_asset) 

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_orders(self,scope):
		return self.table("orders",scope).json

	def get_pendings(self,scope):
		return self.table("pendings",scope).json

	def get_vendorinfo(self,scope):
		return self.table("vendorinfo",scope).json
