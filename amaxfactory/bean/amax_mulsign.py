import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class AMAX_MULSIGN(CreateAccount):
	def __init__(self,contract_name="amax.mulsign"):
		self.name = contract_name
		master = new_master_account()
		amax_mulsign = new_account(master,contract_name,factory=True)
		smart = Contract(amax_mulsign, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.mulsign/amax.mulsign.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.mulsign/amax.mulsign.abi")
		smart.deploy()
		self = amax_mulsign
		self.set_account_permission(add_code=True)
    
	def setup(self):
		amax_mulsign_init(self)
		return self

	def __str__(self):
		return self.name
            

	def cancel(self,issuer='user1',proposal_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("cancel",{"issuer":issuer,"proposal_id":proposal_id,},submitter_,expect_asset=expect_asset) 

	def collectfee(self,from_='user1',to='user1',quantity="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("collectfee",{"from":from_,"to":to,"quantity":quantity,},submitter_,expect_asset=expect_asset) 

	def delmulsigner(self,issuer='user1',wallet_id=1,mulsigner='user1',submitter_="admin",expect_asset=True):
		self.pushaction("delmulsigner",{"issuer":issuer,"wallet_id":wallet_id,"mulsigner":mulsigner,},submitter_,expect_asset=expect_asset) 

	def execute(self,issuer='user1',proposal_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("execute",{"issuer":issuer,"proposal_id":proposal_id,},submitter_,expect_asset=expect_asset) 

	def init(self,fee_collector='user1',wallet_fee="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("init",{"fee_collector":fee_collector,"wallet_fee":wallet_fee,},submitter_,expect_asset=expect_asset) 

	def propose(self,issuer='user1',wallet_id=1,action_name='user1',action_account='user1',packed_action_data=[],excerpt='x',description='x',duration=1,submitter_="admin",expect_asset=True):
		self.pushaction("propose",{"issuer":issuer,"wallet_id":wallet_id,"action_name":action_name,"action_account":action_account,"packed_action_data":packed_action_data,"excerpt":excerpt,"description":description,"duration":duration,},submitter_,expect_asset=expect_asset) 

	def proposeact(self,issuer='user1',wallet_id=1,execution=[],excerpt='x',description='x',duration=1,submitter_="admin",expect_asset=True):
		self.pushaction("proposeact",{"issuer":issuer,"wallet_id":wallet_id,"execution":execution,"excerpt":excerpt,"description":description,"duration":duration,},submitter_,expect_asset=expect_asset) 

	def respond(self,issuer='user1',proposal_id=1,vote=1,submitter_="admin",expect_asset=True):
		self.pushaction("respond",{"issuer":issuer,"proposal_id":proposal_id,"vote":vote,},submitter_,expect_asset=expect_asset) 

	def setfee(self,wallet_id=1,wallet_fee="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("setfee",{"wallet_id":wallet_id,"wallet_fee":wallet_fee,},submitter_,expect_asset=expect_asset) 

	def setmulsigner(self,issuer='user1',wallet_id=1,mulsigner='user1',weight=1,submitter_="admin",expect_asset=True):
		self.pushaction("setmulsigner",{"issuer":issuer,"wallet_id":wallet_id,"mulsigner":mulsigner,"weight":weight,},submitter_,expect_asset=expect_asset) 

	def setmulsignm(self,issuer='user1',wallet_id=1,mulsignm=1,submitter_="admin",expect_asset=True):
		self.pushaction("setmulsignm",{"issuer":issuer,"wallet_id":wallet_id,"mulsignm":mulsignm,},submitter_,expect_asset=expect_asset) 

	def setproexpiry(self,issuer='user1',wallet_id=1,expiry_sec=1,submitter_="admin",expect_asset=True):
		self.pushaction("setproexpiry",{"issuer":issuer,"wallet_id":wallet_id,"expiry_sec":expiry_sec,},submitter_,expect_asset=expect_asset) 

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_proposals(self,scope):
		return self.table("proposals",scope).json

	def get_wallets(self,scope):
		return self.table("wallets",scope).json
