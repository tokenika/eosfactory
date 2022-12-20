import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class PASS_CUSTODY(CreateAccount):
	def __init__(self,contract_name="pass.custody"):
		self.name = contract_name
		master = new_master_account()
		pass_custody = new_account(master,contract_name,factory=True)
		smart = Contract(pass_custody, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "pass.custody/pass.custody.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "pass.custody/pass.custody.abi")
		smart.deploy()
		self = pass_custody
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			pass_custody_init(self)
		except:
			print("pass_custody setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def addplan(self,owner='user1',title='x',asset_contract='user1',asset_symbol=[],unlock_interval_days=1,unlock_times=[],submitter_="admin",expect_asset=True):
		self.pushaction("addplan",{"owner":owner,"title":title,"asset_contract":asset_contract,"asset_symbol":asset_symbol,"unlock_interval_days":unlock_interval_days,"unlock_times":unlock_times,},submitter_,expect_asset=expect_asset) 

	def endlock(self,locker='user1',plan_id=1,lock_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("endlock",{"locker":locker,"plan_id":plan_id,"lock_id":lock_id,},submitter_,expect_asset=expect_asset) 

	def init(self,submitter_="admin",expect_asset=True):
		self.pushaction("init",{},submitter_,expect_asset=expect_asset) 

	def movetrace(self,trace=[],submitter_="admin",expect_asset=True):
		self.pushaction("movetrace",{"trace":trace,},submitter_,expect_asset=expect_asset) 

	def setconfig(self,plan_fee="0.10000000 AMAX",fee_receiver='user1',submitter_="admin",expect_asset=True):
		self.pushaction("setconfig",{"plan_fee":plan_fee,"fee_receiver":fee_receiver,},submitter_,expect_asset=expect_asset) 

	def setmovwindow(self,plan_id=1,symbol=[],started_at=[],finished_at=[],submitter_="admin",expect_asset=True):
		self.pushaction("setmovwindow",{"plan_id":plan_id,"symbol":symbol,"started_at":started_at,"finished_at":finished_at,},submitter_,expect_asset=expect_asset) 

	def setplanowner(self,owner='user1',plan_id=1,new_owner='user1',submitter_="admin",expect_asset=True):
		self.pushaction("setplanowner",{"owner":owner,"plan_id":plan_id,"new_owner":new_owner,},submitter_,expect_asset=expect_asset) 

	def unlock(self,locker='user1',plan_id=1,lock_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("unlock",{"locker":locker,"plan_id":plan_id,"lock_id":lock_id,},submitter_,expect_asset=expect_asset) 

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_locks(self,scope):
		return self.table("locks",scope).json

	def get_movewindows(self,scope):
		return self.table("movewindows",scope).json

	def get_payaccounts(self,scope):
		return self.table("payaccounts",scope).json

	def get_plans(self,scope):
		return self.table("plans",scope).json
