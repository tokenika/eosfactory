import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class AMAX_NTOKEN(CreateAccount):
	def __init__(self,contract_name="amax.ntoken"):
		self.name = contract_name
		master = new_master_account()
		amax_ntoken = new_account(master,contract_name)
		smart = Contract(amax_ntoken, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.ntoken/amax.ntoken.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.ntoken/amax.ntoken.abi")
		smart.deploy()
		self = amax_ntoken
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			amax_ntoken_init(self)
		except:
			print("amax_ntoken setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def approve(self,spender='user1',sender='user1',token_pid=1,amount=1,suber="admin",expect_asset=True):
		self.pushaction("approve",{"spender":spender,"sender":sender,"token_pid":token_pid,"amount":amount,},suber,expect_asset=expect_asset) 

	def create(self,issuer='user1',maximum_supply=[],symbol=[],token_uri='x',ipowner='user1',suber="admin",expect_asset=True):
		self.pushaction("create",{"issuer":issuer,"maximum_supply":maximum_supply,"symbol":symbol,"token_uri":token_uri,"ipowner":ipowner,},suber,expect_asset=expect_asset) 

	def issue(self,to='user1',quantity=[],memo='x',suber="admin",expect_asset=True):
		self.pushaction("issue",{"to":to,"quantity":quantity,"memo":memo,},suber,expect_asset=expect_asset) 

	def notarize(self,notary='user1',token_id=1,suber="admin",expect_asset=True):
		self.pushaction("notarize",{"notary":notary,"token_id":token_id,},suber,expect_asset=expect_asset) 

	def retire(self,quantity=[],memo='x',suber="admin",expect_asset=True):
		self.pushaction("retire",{"quantity":quantity,"memo":memo,},suber,expect_asset=expect_asset) 

	def setipowner(self,symbid=1,ip_owner='user1',suber="admin",expect_asset=True):
		self.pushaction("setipowner",{"symbid":symbid,"ip_owner":ip_owner,},suber,expect_asset=expect_asset) 

	def setnotary(self,notary='user1',to_add='true',suber="admin",expect_asset=True):
		self.pushaction("setnotary",{"notary":notary,"to_add":to_add,},suber,expect_asset=expect_asset) 

	def transfer(self,from_='user1',to='user1',assets=[],memo='x',suber="admin",expect_asset=True):
		self.pushaction("transfer",{"from":from_,"to":to,"assets":assets,"memo":memo,},suber,expect_asset=expect_asset) 

	def transferfrom(self,owner='user1',from_='user1',to='user1',assets=[],memo='x',suber="admin",expect_asset=True):
		self.pushaction("transferfrom",{"owner":owner,"from":from_,"to":to,"assets":assets,"memo":memo,},suber,expect_asset=expect_asset) 

	def get_accounts(self,scope):
		return self.table("accounts",scope).json

	def get_allowances(self,scope):
		return self.table("allowances",scope).json

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_tokenstats(self,scope):
		return self.table("tokenstats",scope).json
