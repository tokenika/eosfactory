import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class AMAX_XCHAIN(CreateAccount):
	def __init__(self,contract_name="amax.xchain"):
		self.name = contract_name
		master = new_master_account()
		amax_xchain = new_account(master,contract_name,factory=True)
		smart = Contract(amax_xchain, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.xchain/amax.xchain.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.xchain/amax.xchain.abi")
		smart.deploy()
		self = amax_xchain
		self.set_account_permission(add_code=True)
    
	def setup(self):
		amax_xchain_init(self)
		return self

	def __str__(self):
		return self.name
            

	def addchain(self,chain='user1',base_chain='user1',common_xin_account='x',submitter_="admin",expect_asset=True):
		self.pushaction("addchain",{"chain":chain,"base_chain":base_chain,"common_xin_account":common_xin_account,},submitter_,expect_asset=expect_asset) 

	def addchaincoin(self,chain='user1',coin='8,AMAX',fee="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("addchaincoin",{"chain":chain,"coin":coin,"fee":fee,},submitter_,expect_asset=expect_asset) 

	def addcoin(self,coin='8,AMAX',submitter_="admin",expect_asset=True):
		self.pushaction("addcoin",{"coin":coin,},submitter_,expect_asset=expect_asset) 

	def cancelxinord(self,order_id=1,cancel_reason='x',submitter_="admin",expect_asset=True):
		self.pushaction("cancelxinord",{"order_id":order_id,"cancel_reason":cancel_reason,},submitter_,expect_asset=expect_asset) 

	def cancelxouord(self,order_id=1,cancel_reason='x',submitter_="admin",expect_asset=True):
		self.pushaction("cancelxouord",{"order_id":order_id,"cancel_reason":cancel_reason,},submitter_,expect_asset=expect_asset) 

	def checkxinord(self,order_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("checkxinord",{"order_id":order_id,},submitter_,expect_asset=expect_asset) 

	def checkxouord(self,order_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("checkxouord",{"order_id":order_id,},submitter_,expect_asset=expect_asset) 

	def delchain(self,chain='user1',submitter_="admin",expect_asset=True):
		self.pushaction("delchain",{"chain":chain,},submitter_,expect_asset=expect_asset) 

	def delchaincoin(self,chain='user1',coin='8,AMAX',submitter_="admin",expect_asset=True):
		self.pushaction("delchaincoin",{"chain":chain,"coin":coin,},submitter_,expect_asset=expect_asset) 

	def delcoin(self,coin='8,AMAX',submitter_="admin",expect_asset=True):
		self.pushaction("delcoin",{"coin":coin,},submitter_,expect_asset=expect_asset) 

	def getacctchain(self,account='user1',base_chain='user1',submitter_="admin",expect_asset=True):
		self.pushaction("getacctchain",{"account":account,"base_chain":base_chain,},submitter_,expect_asset=expect_asset) 

	def getxintoaddr(self,xin_to_addr='x',submitter_="admin",expect_asset=True):
		self.pushaction("getxintoaddr",{"xin_to_addr":xin_to_addr,},submitter_,expect_asset=expect_asset) 

	def init(self,admin='user1',maker='user1',checker='user1',fee_collector='user1',submitter_="admin",expect_asset=True):
		self.pushaction("init",{"admin":admin,"maker":maker,"checker":checker,"fee_collector":fee_collector,},submitter_,expect_asset=expect_asset) 

	def mkxinorder(self,to='user1',chain_name='user1',coin_name='8,AMAX',txid='x',xin_from='x',xin_to='x',quantity="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("mkxinorder",{"to":to,"chain_name":chain_name,"coin_name":coin_name,"txid":txid,"xin_from":xin_from,"xin_to":xin_to,"quantity":quantity,},submitter_,expect_asset=expect_asset) 

	def reqxintoaddr(self,applicant='user1',applicant_account='user1',base_chain='user1',mulsign_wallet_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("reqxintoaddr",{"applicant":applicant,"applicant_account":applicant_account,"base_chain":base_chain,"mulsign_wallet_id":mulsign_wallet_id,},submitter_,expect_asset=expect_asset) 

	def resetxout(self,order_id=1,xout_order_statu='user1',submitter_="admin",expect_asset=True):
		self.pushaction("resetxout",{"order_id":order_id,"xout_order_statu":xout_order_statu,},submitter_,expect_asset=expect_asset) 

	def setaddress(self,applicant='user1',base_chain='user1',mulsign_wallet_id=1,xin_to='x',submitter_="admin",expect_asset=True):
		self.pushaction("setaddress",{"applicant":applicant,"base_chain":base_chain,"mulsign_wallet_id":mulsign_wallet_id,"xin_to":xin_to,},submitter_,expect_asset=expect_asset) 

	def setaplfarm(self,symb='x',apl="0.10000000 AMAX",to_add='true',submitter_="admin",expect_asset=True):
		self.pushaction("setaplfarm",{"symb":symb,"apl":apl,"to_add":to_add,},submitter_,expect_asset=expect_asset) 

	def setchaincoin(self,chaincoin_id=1,new_chain_name='user1',submitter_="admin",expect_asset=True):
		self.pushaction("setchaincoin",{"chaincoin_id":chaincoin_id,"new_chain_name":new_chain_name,},submitter_,expect_asset=expect_asset) 

	def setfeerate(self,fee_rate=1,submitter_="admin",expect_asset=True):
		self.pushaction("setfeerate",{"fee_rate":fee_rate,},submitter_,expect_asset=expect_asset) 

	def setxouconfm(self,order_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("setxouconfm",{"order_id":order_id,},submitter_,expect_asset=expect_asset) 

	def setxousent(self,order_id=1,txid='x',xout_from='x',submitter_="admin",expect_asset=True):
		self.pushaction("setxousent",{"order_id":order_id,"txid":txid,"xout_from":xout_from,},submitter_,expect_asset=expect_asset) 

	def xinaddrmapid(self,account='user1',base_chain='user1',submitter_="admin",expect_asset=True):
		self.pushaction("xinaddrmapid",{"account":account,"base_chain":base_chain,},submitter_,expect_asset=expect_asset) 

	def get_chaincoins(self,scope):
		return self.table("chaincoins",scope).json

	def get_chains(self,scope):
		return self.table("chains",scope).json

	def get_coins(self,scope):
		return self.table("coins",scope).json

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_global1(self,scope):
		return self.table("global1",scope).json

	def get_xinaddrmap(self,scope):
		return self.table("xinaddrmap",scope).json

	def get_xinorders(self,scope):
		return self.table("xinorders",scope).json

	def get_xoutorders(self,scope):
		return self.table("xoutorders",scope).json
