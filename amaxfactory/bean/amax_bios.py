import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class AMAX_BIOS(CreateAccount):
	def __init__(self,contract_name="amax.bios"):
		self.name = contract_name
		master = new_master_account()
		amax_bios = new_account(master,contract_name,factory=True)
		smart = Contract(amax_bios, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.bios/amax.bios.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.bios/amax.bios.abi")
		smart.deploy()
		self = amax_bios
		self.set_account_permission(add_code=True)
    
	def setup(self):
		amax_bios_init(self)
		return self

	def __str__(self):
		return self.name
            

	def activate(self,feature_digest=[],submitter_="admin",expect_asset=True):
		self.pushaction("activate",{"feature_digest":feature_digest,},submitter_,expect_asset=expect_asset) 

	def canceldelay(self,canceling_auth=[],trx_id=[],submitter_="admin",expect_asset=True):
		self.pushaction("canceldelay",{"canceling_auth":canceling_auth,"trx_id":trx_id,},submitter_,expect_asset=expect_asset) 

	def deleteauth(self,account='user1',permission='user1',submitter_="admin",expect_asset=True):
		self.pushaction("deleteauth",{"account":account,"permission":permission,},submitter_,expect_asset=expect_asset) 

	def linkauth(self,account='user1',code='user1',type='user1',requirement='user1',submitter_="admin",expect_asset=True):
		self.pushaction("linkauth",{"account":account,"code":code,"type":type,"requirement":requirement,},submitter_,expect_asset=expect_asset) 

	def newaccount(self,creator='user1',name='user1',owner=[],active=[],submitter_="admin",expect_asset=True):
		self.pushaction("newaccount",{"creator":creator,"name":name,"owner":owner,"active":active,},submitter_,expect_asset=expect_asset) 

	def onerror(self,sender_id=1,sent_trx=[],submitter_="admin",expect_asset=True):
		self.pushaction("onerror",{"sender_id":sender_id,"sent_trx":sent_trx,},submitter_,expect_asset=expect_asset) 

	def reqactivated(self,feature_digest=[],submitter_="admin",expect_asset=True):
		self.pushaction("reqactivated",{"feature_digest":feature_digest,},submitter_,expect_asset=expect_asset) 

	def reqauth(self,from_='user1',submitter_="admin",expect_asset=True):
		self.pushaction("reqauth",{"from":from_,},submitter_,expect_asset=expect_asset) 

	def setabi(self,account='user1',abi=[],submitter_="admin",expect_asset=True):
		self.pushaction("setabi",{"account":account,"abi":abi,},submitter_,expect_asset=expect_asset) 

	def setalimits(self,account='user1',ram_bytes=[],net_weight=[],cpu_weight=[],submitter_="admin",expect_asset=True):
		self.pushaction("setalimits",{"account":account,"ram_bytes":ram_bytes,"net_weight":net_weight,"cpu_weight":cpu_weight,},submitter_,expect_asset=expect_asset) 

	def setcode(self,account='user1',vmtype=1,vmversion=1,code=[],submitter_="admin",expect_asset=True):
		self.pushaction("setcode",{"account":account,"vmtype":vmtype,"vmversion":vmversion,"code":code,},submitter_,expect_asset=expect_asset) 

	def setparams(self,params=[],submitter_="admin",expect_asset=True):
		self.pushaction("setparams",{"params":params,},submitter_,expect_asset=expect_asset) 

	def setpriv(self,account='user1',is_priv=1,submitter_="admin",expect_asset=True):
		self.pushaction("setpriv",{"account":account,"is_priv":is_priv,},submitter_,expect_asset=expect_asset) 

	def setprods(self,schedule=[],submitter_="admin",expect_asset=True):
		self.pushaction("setprods",{"schedule":schedule,},submitter_,expect_asset=expect_asset) 

	def unlinkauth(self,account='user1',code='user1',type='user1',submitter_="admin",expect_asset=True):
		self.pushaction("unlinkauth",{"account":account,"code":code,"type":type,},submitter_,expect_asset=expect_asset) 

	def updateauth(self,account='user1',permission='user1',parent='user1',auth=[],submitter_="admin",expect_asset=True):
		self.pushaction("updateauth",{"account":account,"permission":permission,"parent":parent,"auth":auth,},submitter_,expect_asset=expect_asset) 

	def get_abihash(self,scope):
		return self.table("abihash",scope).json
