import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class DID_NTOKEN(CreateAccount):
	def __init__(self,contract_name="did.ntoken"):
		self.name = contract_name
		master = new_master_account()
		did_ntoken = new_account(master,contract_name,factory=True)
		smart = Contract(did_ntoken, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "did.ntoken/did.ntoken.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "did.ntoken/did.ntoken.abi")
		smart.deploy()
		self = did_ntoken
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			did_ntoken_init(self)
		except:
			print("did_ntoken setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def create(self,issuer='user1',maximum_supply=[],symbol=[],token_uri='x',ipowner='user1',submitter_="admin",expect_asset=True):
		self.pushaction("create",{"issuer":issuer,"maximum_supply":maximum_supply,"symbol":symbol,"token_uri":token_uri,"ipowner":ipowner,},submitter_,expect_asset=expect_asset) 

	def issue(self,to='user1',quantity=[],memo='x',submitter_="admin",expect_asset=True):
		self.pushaction("issue",{"to":to,"quantity":quantity,"memo":memo,},submitter_,expect_asset=expect_asset) 

	def notarize(self,notary='user1',token_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("notarize",{"notary":notary,"token_id":token_id,},submitter_,expect_asset=expect_asset) 

	def retire(self,quantity=[],memo='x',submitter_="admin",expect_asset=True):
		self.pushaction("retire",{"quantity":quantity,"memo":memo,},submitter_,expect_asset=expect_asset) 

	def setacctperms(self,issuer='user1',to='user1',symbol=[],allowsend='true',allowrecv='true',submitter_="admin",expect_asset=True):
		self.pushaction("setacctperms",{"issuer":issuer,"to":to,"symbol":symbol,"allowsend":allowsend,"allowrecv":allowrecv,},submitter_,expect_asset=expect_asset) 

	def setnotary(self,notary='user1',to_add='true',submitter_="admin",expect_asset=True):
		self.pushaction("setnotary",{"notary":notary,"to_add":to_add,},submitter_,expect_asset=expect_asset) 

	def transfer(self,from_='user1',to='user1',assets=[],memo='x',submitter_="admin",expect_asset=True):
		self.pushaction("transfer",{"from":from_,"to":to,"assets":assets,"memo":memo,},submitter_,expect_asset=expect_asset) 

	def get_accounts(self,scope):
		return self.table("accounts",scope).json

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_tokenstats(self,scope):
		return self.table("tokenstats",scope).json
