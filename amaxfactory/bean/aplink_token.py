import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class APLINK_TOKEN(CreateAccount):
	def __init__(self,contract_name="aplink.token"):
		self.name = contract_name
		master = new_master_account()
		aplink_token = new_account(master,contract_name)
		smart = Contract(aplink_token, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "aplink.token/aplink.token.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "aplink.token/aplink.token.abi")
		smart.deploy()
		self = aplink_token
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			aplink_token_init(self)
		except:
			print("aplink_token setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def burn(self,predator='user1',victim='user1',quantity="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("burn",{"predator":predator,"victim":victim,"quantity":quantity,},submitter_,expect_asset=expect_asset) 

	def create(self,issuer='user1',maximum_supply="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("create",{"issuer":issuer,"maximum_supply":maximum_supply,},submitter_,expect_asset=expect_asset) 

	def issue(self,to='user1',quantity="0.10000000 AMAX",memo='x',submitter_="admin",expect_asset=True):
		self.pushaction("issue",{"to":to,"quantity":quantity,"memo":memo,},submitter_,expect_asset=expect_asset) 

	def notifyreward(self,predator='user1',victim='user1',reward_quantity="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("notifyreward",{"predator":predator,"victim":victim,"reward_quantity":reward_quantity,},submitter_,expect_asset=expect_asset) 

	def open(self,owner='user1',symbol='8,AMAX',ram_payer='user1',submitter_="admin",expect_asset=True):
		self.pushaction("open",{"owner":owner,"symbol":symbol,"ram_payer":ram_payer,},submitter_,expect_asset=expect_asset) 

	def retire(self,quantity="0.10000000 AMAX",memo='x',submitter_="admin",expect_asset=True):
		self.pushaction("retire",{"quantity":quantity,"memo":memo,},submitter_,expect_asset=expect_asset) 

	def setacctperms(self,issuer='user1',to='user1',symbol='8,AMAX',allowsend='true',allowrecv='true',submitter_="admin",expect_asset=True):
		self.pushaction("setacctperms",{"issuer":issuer,"to":to,"symbol":symbol,"allowsend":allowsend,"allowrecv":allowrecv,},submitter_,expect_asset=expect_asset) 

	def transfer(self,from_='user1',to='user1',quantity="0.10000000 AMAX",memo='x',submitter_="admin",expect_asset=True):
		self.pushaction("transfer",{"from":from_,"to":to,"quantity":quantity,"memo":memo,},submitter_,expect_asset=expect_asset) 

	def get_accounts(self,scope):
		return self.table("accounts",scope).json

	def get_stat(self,scope):
		return self.table("stat",scope).json
