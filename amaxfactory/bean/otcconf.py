import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class OTCCONF(CreateAccount):
	def __init__(self,contract_name="otcconf"):
		self.name = contract_name
		master = new_master_account()
		otcconf = new_account(master,contract_name,factory=True)
		smart = Contract(otcconf, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "otcconf/otcconf.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "otcconf/otcconf.abi")
		smart.deploy()
		self = otcconf
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			otcconf_init(self)
		except:
			print("otcconf setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def addcoin(self,is_buy='true',coin='8,AMAX',stake_coin='8,AMAX',contract_name='user1',submitter_="admin",expect_asset=True):
		self.pushaction("addcoin",{"is_buy":is_buy,"coin":coin,"stake_coin":stake_coin,"contract_name":contract_name,},submitter_,expect_asset=expect_asset) 

	def deletecoin(self,is_buy='true',coin='8,AMAX',contract_name='user1',submitter_="admin",expect_asset=True):
		self.pushaction("deletecoin",{"is_buy":is_buy,"coin":coin,"contract_name":contract_name,},submitter_,expect_asset=expect_asset) 

	def init(self,admin='user1',submitter_="admin",expect_asset=True):
		self.pushaction("init",{"admin":admin,},submitter_,expect_asset=expect_asset) 

	def setappname(self,otc_name='user1',contract_name='user1',submitter_="admin",expect_asset=True):
		self.pushaction("setappname",{"otc_name":otc_name,"contract_name":contract_name,},submitter_,expect_asset=expect_asset) 

	def setconf(self,conf=[],submitter_="admin",expect_asset=True):
		self.pushaction("setconf",{"conf":conf,},submitter_,expect_asset=expect_asset) 

	def setfarm(self,farmname='user1',farm_lease_id=1,symcode=[],farm_scale=1,contract_name='user1',submitter_="admin",expect_asset=True):
		self.pushaction("setfarm",{"farmname":farmname,"farm_lease_id":farm_lease_id,"symcode":symcode,"farm_scale":farm_scale,"contract_name":contract_name,},submitter_,expect_asset=expect_asset) 

	def setfeepct(self,feepct=1,contract_name='user1',submitter_="admin",expect_asset=True):
		self.pushaction("setfeepct",{"feepct":feepct,"contract_name":contract_name,},submitter_,expect_asset=expect_asset) 

	def setmanager(self,type='user1',account='user1',contract_name='user1',submitter_="admin",expect_asset=True):
		self.pushaction("setmanager",{"type":type,"account":account,"contract_name":contract_name,},submitter_,expect_asset=expect_asset) 

	def setsettlelv(self,configs=[],contract_name='user1',submitter_="admin",expect_asset=True):
		self.pushaction("setsettlelv",{"configs":configs,"contract_name":contract_name,},submitter_,expect_asset=expect_asset) 

	def setstatus(self,status='user1',contract_name='user1',submitter_="admin",expect_asset=True):
		self.pushaction("setstatus",{"status":status,"contract_name":contract_name,},submitter_,expect_asset=expect_asset) 

	def setswapstep(self,rates=[],contract_name='user1',submitter_="admin",expect_asset=True):
		self.pushaction("setswapstep",{"rates":rates,"contract_name":contract_name,},submitter_,expect_asset=expect_asset) 

	def settimeout(self,accepted_timeout=1,payed_timeout=1,contract_name='user1',submitter_="admin",expect_asset=True):
		self.pushaction("settimeout",{"accepted_timeout":accepted_timeout,"payed_timeout":payed_timeout,"contract_name":contract_name,},submitter_,expect_asset=expect_asset) 

	def get_fiatconf(self,scope):
		return self.table("fiatconf",scope).json

	def get_global(self,scope):
		return self.table("global",scope).json
