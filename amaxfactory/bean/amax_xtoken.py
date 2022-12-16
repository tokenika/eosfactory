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
		amax_xtoken = new_account(master,contract_name)
		smart = Contract(amax_xtoken, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.xtoken/amax.xtoken.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.xtoken/amax.xtoken.abi")
		smart.deploy()
		self = amax_xtoken
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			amax_xtoken_init(self)
		except:
			print("amax_xtoken setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def close(self,owner='user1',symbol='8,AMAX',suber="admin",expect_asset=True):
		self.pushaction("close",{"owner":owner,"symbol":symbol,},suber,expect_asset=expect_asset) 

	def create(self,issuer='user1',maximum_supply="0.10000000 AMAX",suber="admin",expect_asset=True):
		self.pushaction("create",{"issuer":issuer,"maximum_supply":maximum_supply,},suber,expect_asset=expect_asset) 

	def feeexempt(self,symbol='8,AMAX',account='user1',is_fee_exempt='true',suber="admin",expect_asset=True):
		self.pushaction("feeexempt",{"symbol":symbol,"account":account,"is_fee_exempt":is_fee_exempt,},suber,expect_asset=expect_asset) 

	def feeratio(self,symbol='8,AMAX',fee_ratio=1,suber="admin",expect_asset=True):
		self.pushaction("feeratio",{"symbol":symbol,"fee_ratio":fee_ratio,},suber,expect_asset=expect_asset) 

	def feereceiver(self,symbol='8,AMAX',fee_receiver='user1',suber="admin",expect_asset=True):
		self.pushaction("feereceiver",{"symbol":symbol,"fee_receiver":fee_receiver,},suber,expect_asset=expect_asset) 

	def freezeacct(self,symbol='8,AMAX',account='user1',is_frozen='true',suber="admin",expect_asset=True):
		self.pushaction("freezeacct",{"symbol":symbol,"account":account,"is_frozen":is_frozen,},suber,expect_asset=expect_asset) 

	def issue(self,to='user1',quantity="0.10000000 AMAX",memo='x',suber="admin",expect_asset=True):
		self.pushaction("issue",{"to":to,"quantity":quantity,"memo":memo,},suber,expect_asset=expect_asset) 

	def minfee(self,symbol='8,AMAX',min_fee_quantity="0.10000000 AMAX",suber="admin",expect_asset=True):
		self.pushaction("minfee",{"symbol":symbol,"min_fee_quantity":min_fee_quantity,},suber,expect_asset=expect_asset) 

	def notifypayfee(self,from_='user1',to='user1',fee_receiver='user1',fee="0.10000000 AMAX",memo='x',suber="admin",expect_asset=True):
		self.pushaction("notifypayfee",{"from":from_,"to":to,"fee_receiver":fee_receiver,"fee":fee,"memo":memo,},suber,expect_asset=expect_asset) 

	def open(self,owner='user1',symbol='8,AMAX',ram_payer='user1',suber="admin",expect_asset=True):
		self.pushaction("open",{"owner":owner,"symbol":symbol,"ram_payer":ram_payer,},suber,expect_asset=expect_asset) 

	def pause(self,symbol='8,AMAX',is_paused='true',suber="admin",expect_asset=True):
		self.pushaction("pause",{"symbol":symbol,"is_paused":is_paused,},suber,expect_asset=expect_asset) 

	def retire(self,quantity="0.10000000 AMAX",memo='x',suber="admin",expect_asset=True):
		self.pushaction("retire",{"quantity":quantity,"memo":memo,},suber,expect_asset=expect_asset) 

	def transfer(self,from_='user1',to='user1',quantity="0.10000000 AMAX",memo='x',suber="admin",expect_asset=True):
		self.pushaction("transfer",{"from":from_,"to":to,"quantity":quantity,"memo":memo,},suber,expect_asset=expect_asset) 

	def get_accounts(self,scope):
		return self.table("accounts",scope).json

	def get_stat(self,scope):
		return self.table("stat",scope).json
