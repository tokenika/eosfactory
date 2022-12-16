import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class APLINK_FARM(CreateAccount):
	def __init__(self,contract_name="aplink.farm"):
		self.name = contract_name
		master = new_master_account()
		aplink_farm = new_account(master,contract_name)
		smart = Contract(aplink_farm, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "aplink/aplink.farm/aplink.farm.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "aplink/aplink.farm/aplink.farm.abi")
		smart.deploy()
		self = aplink_farm
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			aplink_farm_init(self)
		except:
			print("aplink_farm setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def allot(self,lease_id=1,farmer='user1',quantity="0.10000000 AMAX",memo='x',suber="admin",expect_asset=True):
		self.pushaction("allot",{"lease_id":lease_id,"farmer":farmer,"quantity":quantity,"memo":memo,},suber,expect_asset=expect_asset) 

	def init(self,landlord='user1',jamfactory='user1',last_lease_id=1,last_allot_id=1,suber="admin",expect_asset=True):
		self.pushaction("init",{"landlord":landlord,"jamfactory":jamfactory,"last_lease_id":last_lease_id,"last_allot_id":last_allot_id,},suber,expect_asset=expect_asset) 

	def lease(self,tenant='user1',lese_title='x',land_uri='x',banner_uri='x',suber="admin",expect_asset=True):
		self.pushaction("lease",{"tenant":tenant,"lese_title":lese_title,"land_uri":land_uri,"banner_uri":banner_uri,},suber,expect_asset=expect_asset) 

	def pick(self,farmer='user1',allot_ids=1,suber="admin",expect_asset=True):
		self.pushaction("pick",{"farmer":farmer,"allot_ids":allot_ids,},suber,expect_asset=expect_asset) 

	def reclaimallot(self,issuer='user1',allot_id=1,memo='x',suber="admin",expect_asset=True):
		self.pushaction("reclaimallot",{"issuer":issuer,"allot_id":allot_id,"memo":memo,},suber,expect_asset=expect_asset) 

	def reclaimlease(self,issuer='user1',lease_id=1,memo='x',suber="admin",expect_asset=True):
		self.pushaction("reclaimlease",{"issuer":issuer,"lease_id":lease_id,"memo":memo,},suber,expect_asset=expect_asset) 

	def setlease(self,lease_id=1,land_uri='x',banner_uri='x',suber="admin",expect_asset=True):
		self.pushaction("setlease",{"lease_id":lease_id,"land_uri":land_uri,"banner_uri":banner_uri,},suber,expect_asset=expect_asset) 

	def setstatus(self,lease_id=1,status='user1',suber="admin",expect_asset=True):
		self.pushaction("setstatus",{"lease_id":lease_id,"status":status,},suber,expect_asset=expect_asset) 

	def settenant(self,lease_id=1,tenant='user1',suber="admin",expect_asset=True):
		self.pushaction("settenant",{"lease_id":lease_id,"tenant":tenant,},suber,expect_asset=expect_asset) 

	def get_allots(self,scope):
		return self.table("allots",scope).json

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_leases(self,scope):
		return self.table("leases",scope).json
