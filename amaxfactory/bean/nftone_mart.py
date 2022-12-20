import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class NFTONE_MART(CreateAccount):
	def __init__(self,contract_name="nftone.mart"):
		self.name = contract_name
		master = new_master_account()
		nftone_mart = new_account(master,contract_name,factory=True)
		smart = Contract(nftone_mart, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "nftone.mart/nftone.mart.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "nftone.mart/nftone.mart.abi")
		smart.deploy()
		self = nftone_mart
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			nftone_mart_init(self)
		except:
			print("nftone_mart setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def cancelbid(self,buyer='user1',buyer_bid_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("cancelbid",{"buyer":buyer,"buyer_bid_id":buyer_bid_id,},submitter_,expect_asset=expect_asset) 

	def cancelorder(self,maker='user1',token_id=1,order_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("cancelorder",{"maker":maker,"token_id":token_id,"order_id":order_id,},submitter_,expect_asset=expect_asset) 

	def dealtrace(self,trace=[],submitter_="admin",expect_asset=True):
		self.pushaction("dealtrace",{"trace":trace,},submitter_,expect_asset=expect_asset) 

	def init(self,pay_symbol='8,AMAX',pay_contract='user1',admin='user1',devfeerate=[],feecollector='user1',ipfeerate=[],submitter_="admin",expect_asset=True):
		self.pushaction("init",{"pay_symbol":pay_symbol,"pay_contract":pay_contract,"admin":admin,"devfeerate":devfeerate,"feecollector":feecollector,"ipfeerate":ipfeerate,},submitter_,expect_asset=expect_asset) 

	def setfeecollec(self,dev_fee_collector='user1',submitter_="admin",expect_asset=True):
		self.pushaction("setfeecollec",{"dev_fee_collector":dev_fee_collector,},submitter_,expect_asset=expect_asset) 

	def takebuybid(self,issuer='user1',token_id=1,buyer_bid_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("takebuybid",{"issuer":issuer,"token_id":token_id,"buyer_bid_id":buyer_bid_id,},submitter_,expect_asset=expect_asset) 

	def get_buyerbids(self,scope):
		return self.table("buyerbids",scope).json

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_sellorders(self,scope):
		return self.table("sellorders",scope).json
