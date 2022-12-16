import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class VERSO_ITOKEN(CreateAccount):
	def __init__(self,contract_name="verso.itoken"):
		self.name = contract_name
		master = new_master_account()
		verso_itoken = new_account(master,contract_name)
		smart = Contract(verso_itoken, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "verso.itoken/verso.itoken.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "verso.itoken/verso.itoken.abi")
		smart.deploy()
		self = verso_itoken
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			verso_itoken_init(self)
		except:
			print("verso_itoken setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def create(self,issuer='user1',maximum_supply=[],symbol=[],token_uri='x',ipowner='user1',suber="admin",expect_asset=True):
		self.pushaction("create",{"issuer":issuer,"maximum_supply":maximum_supply,"symbol":symbol,"token_uri":token_uri,"ipowner":ipowner,},suber,expect_asset=expect_asset) 

	def issue(self,to='user1',quantity=[],memo='x',suber="admin",expect_asset=True):
		self.pushaction("issue",{"to":to,"quantity":quantity,"memo":memo,},suber,expect_asset=expect_asset) 

	def notarize(self,notary='user1',token_id=1,suber="admin",expect_asset=True):
		self.pushaction("notarize",{"notary":notary,"token_id":token_id,},suber,expect_asset=expect_asset) 

	def retire(self,quantity=[],memo='x',suber="admin",expect_asset=True):
		self.pushaction("retire",{"quantity":quantity,"memo":memo,},suber,expect_asset=expect_asset) 

	def setipowner(self,symb_id=1,ipowner='user1',suber="admin",expect_asset=True):
		self.pushaction("setipowner",{"symb_id":symb_id,"ipowner":ipowner,},suber,expect_asset=expect_asset) 

	def setnotary(self,notary='user1',to_add='true',suber="admin",expect_asset=True):
		self.pushaction("setnotary",{"notary":notary,"to_add":to_add,},suber,expect_asset=expect_asset) 

	def settokenuri(self,symb_id=1,token_uri='x',suber="admin",expect_asset=True):
		self.pushaction("settokenuri",{"symb_id":symb_id,"token_uri":token_uri,},suber,expect_asset=expect_asset) 

	def setwhitelist(self,owner='user1',to_add='true',suber="admin",expect_asset=True):
		self.pushaction("setwhitelist",{"owner":owner,"to_add":to_add,},suber,expect_asset=expect_asset) 

	def transfer(self,from_='user1',to='user1',assets=[],memo='x',suber="admin",expect_asset=True):
		self.pushaction("transfer",{"from":from_,"to":to,"assets":assets,"memo":memo,},suber,expect_asset=expect_asset) 

	def get_accounts(self,scope):
		return self.table("accounts",scope).json

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_tokenstats(self,scope):
		return self.table("tokenstats",scope).json
