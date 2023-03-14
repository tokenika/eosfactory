import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class AMAX_XTOKEN(CreateAccount):
	def __init__(self,contract_name="amax.xtoken"):
		self.name = contract_name
		master = new_master_account()
		amax_xtoken = new_account(master,contract_name,factory=True)
		smart = Contract(amax_xtoken, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.xtoken/amax.xtoken.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.xtoken/amax.xtoken.abi")
		smart.deploy()
		self = amax_xtoken
		self.set_account_permission(add_code=True)
    
	def setup(self):
		amax_xtoken_init(self)
		return self

	def __str__(self):
		return self.name
            

	def close(self,owner='user1',symbol='8,AMAX',submitter_="admin",expect_asset=True):
		self.pushaction("close",{"owner":owner,"symbol":symbol,},submitter_,expect_asset=expect_asset) 

	def create(self,issuer='user1',maximum_supply="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("create",{"issuer":issuer,"maximum_supply":maximum_supply,},submitter_,expect_asset=expect_asset) 

	def feeexempt(self,symbol='8,AMAX',account='user1',is_fee_exempt='true',submitter_="admin",expect_asset=True):
		self.pushaction("feeexempt",{"symbol":symbol,"account":account,"is_fee_exempt":is_fee_exempt,},submitter_,expect_asset=expect_asset) 

	def feeratio(self,symbol='8,AMAX',fee_ratio=1,submitter_="admin",expect_asset=True):
		self.pushaction("feeratio",{"symbol":symbol,"fee_ratio":fee_ratio,},submitter_,expect_asset=expect_asset) 

	def feereceiver(self,symbol='8,AMAX',fee_receiver='user1',submitter_="admin",expect_asset=True):
		self.pushaction("feereceiver",{"symbol":symbol,"fee_receiver":fee_receiver,},submitter_,expect_asset=expect_asset) 

	def freezeacct(self,symbol='8,AMAX',account='user1',is_frozen='true',submitter_="admin",expect_asset=True):
		self.pushaction("freezeacct",{"symbol":symbol,"account":account,"is_frozen":is_frozen,},submitter_,expect_asset=expect_asset) 

	def issue(self,to='user1',quantity="0.10000000 AMAX",memo='x',submitter_="admin",expect_asset=True):
		self.pushaction("issue",{"to":to,"quantity":quantity,"memo":memo,},submitter_,expect_asset=expect_asset) 

	def minfee(self,symbol='8,AMAX',min_fee_quantity="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("minfee",{"symbol":symbol,"min_fee_quantity":min_fee_quantity,},submitter_,expect_asset=expect_asset) 

	def notifypayfee(self,from_='user1',to='user1',fee_receiver='user1',fee="0.10000000 AMAX",memo='x',submitter_="admin",expect_asset=True):
		self.pushaction("notifypayfee",{"from":from_,"to":to,"fee_receiver":fee_receiver,"fee":fee,"memo":memo,},submitter_,expect_asset=expect_asset) 

	def open(self,owner='user1',symbol='8,AMAX',ram_payer='user1',submitter_="admin",expect_asset=True):
		self.pushaction("open",{"owner":owner,"symbol":symbol,"ram_payer":ram_payer,},submitter_,expect_asset=expect_asset) 

	def pause(self,symbol='8,AMAX',is_paused='true',submitter_="admin",expect_asset=True):
		self.pushaction("pause",{"symbol":symbol,"is_paused":is_paused,},submitter_,expect_asset=expect_asset) 

	def retire(self,quantity="0.10000000 AMAX",memo='x',submitter_="admin",expect_asset=True):
		self.pushaction("retire",{"quantity":quantity,"memo":memo,},submitter_,expect_asset=expect_asset) 

	def transfer(self,from_='user1',to='user1',quantity="0.10000000 AMAX",memo='x',submitter_="admin",expect_asset=True):
		self.pushaction("transfer",{"from":from_,"to":to,"quantity":quantity,"memo":memo,},submitter_,expect_asset=expect_asset) 

	def get_accounts(self,scope):
		return self.table("accounts",scope).json

	def get_stat(self,scope):
		return self.table("stat",scope).json
