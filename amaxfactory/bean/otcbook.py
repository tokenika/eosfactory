import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class OTCBOOK(CreateAccount):
	def __init__(self,contract_name="otcbook"):
		self.name = contract_name
		master = new_master_account()
		otcbook = new_account(master,contract_name,factory=True)
		smart = Contract(otcbook, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "otcbook/otcbook.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "otcbook/otcbook.abi")
		smart.deploy()
		self = otcbook
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			otcbook_init(self)
		except:
			print("otcbook setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def addarbiter(self,sender='user1',account='user1',email='x',submitter_="admin",expect_asset=True):
		self.pushaction("addarbiter",{"sender":sender,"account":account,"email":email,},submitter_,expect_asset=expect_asset) 

	def cancelarbit(self,account_type=1,account='user1',deal_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("cancelarbit",{"account_type":account_type,"account":account,"deal_id":deal_id,},submitter_,expect_asset=expect_asset) 

	def canceldeal(self,account='user1',account_type=1,deal_id=1,is_taker_black='true',submitter_="admin",expect_asset=True):
		self.pushaction("canceldeal",{"account":account,"account_type":account_type,"deal_id":deal_id,"is_taker_black":is_taker_black,},submitter_,expect_asset=expect_asset) 

	def closearbit(self,account='user1',deal_id=1,arbit_result=1,submitter_="admin",expect_asset=True):
		self.pushaction("closearbit",{"account":account,"deal_id":deal_id,"arbit_result":arbit_result,},submitter_,expect_asset=expect_asset) 

	def closedeal(self,account='user1',account_type=1,deal_id=1,close_msg='x',submitter_="admin",expect_asset=True):
		self.pushaction("closedeal",{"account":account,"account_type":account_type,"deal_id":deal_id,"close_msg":close_msg,},submitter_,expect_asset=expect_asset) 

	def closeorder(self,owner='user1',order_side='user1',order_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("closeorder",{"owner":owner,"order_side":order_side,"order_id":order_id,},submitter_,expect_asset=expect_asset) 

	def dealnotifyv2(self,account='user1',info=[],action_type=1,deal=[],submitter_="admin",expect_asset=True):
		self.pushaction("dealnotifyv2",{"account":account,"info":info,"action_type":action_type,"deal":deal,},submitter_,expect_asset=expect_asset) 

	def delarbiter(self,sender='user1',account='user1',submitter_="admin",expect_asset=True):
		self.pushaction("delarbiter",{"sender":sender,"account":account,},submitter_,expect_asset=expect_asset) 

	def delmerchant(self,sender='user1',merchant_acct='user1',submitter_="admin",expect_asset=True):
		self.pushaction("delmerchant",{"sender":sender,"merchant_acct":merchant_acct,},submitter_,expect_asset=expect_asset) 

	def opendeal(self,taker='user1',order_side='user1',order_id=1,deal_quantity="0.10000000 AMAX",order_sn=1,pay_type='user1',submitter_="admin",expect_asset=True):
		self.pushaction("opendeal",{"taker":taker,"order_side":order_side,"order_id":order_id,"deal_quantity":deal_quantity,"order_sn":order_sn,"pay_type":pay_type,},submitter_,expect_asset=expect_asset) 

	def openorder(self,owner='user1',order_side='user1',pay_methods=[],va_quantity="0.10000000 AMAX",va_price="0.10000000 AMAX",va_min_take_quantity="0.10000000 AMAX",va_max_take_quantity="0.10000000 AMAX",memo='x',submitter_="admin",expect_asset=True):
		self.pushaction("openorder",{"owner":owner,"order_side":order_side,"pay_methods":pay_methods,"va_quantity":va_quantity,"va_price":va_price,"va_min_take_quantity":va_min_take_quantity,"va_max_take_quantity":va_max_take_quantity,"memo":memo,},submitter_,expect_asset=expect_asset) 

	def pauseorder(self,owner='user1',order_side='user1',order_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("pauseorder",{"owner":owner,"order_side":order_side,"order_id":order_id,},submitter_,expect_asset=expect_asset) 

	def processdeal(self,account='user1',account_type=1,deal_id=1,action=1,submitter_="admin",expect_asset=True):
		self.pushaction("processdeal",{"account":account,"account_type":account_type,"deal_id":deal_id,"action":action,},submitter_,expect_asset=expect_asset) 

	def rejectmerch(self,account='user1',reject_reason='x',curr_ts=[],submitter_="admin",expect_asset=True):
		self.pushaction("rejectmerch",{"account":account,"reject_reason":reject_reason,"curr_ts":curr_ts,},submitter_,expect_asset=expect_asset) 

	def remerchant(self,mi=[],submitter_="admin",expect_asset=True):
		self.pushaction("remerchant",{"mi":mi,},submitter_,expect_asset=expect_asset) 

	def resetdeal(self,account='user1',deal_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("resetdeal",{"account":account,"deal_id":deal_id,},submitter_,expect_asset=expect_asset) 

	def resumeorder(self,owner='user1',order_side='user1',order_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("resumeorder",{"owner":owner,"order_side":order_side,"order_id":order_id,},submitter_,expect_asset=expect_asset) 

	def setadmin(self,admin='user1',to_add='true',submitter_="admin",expect_asset=True):
		self.pushaction("setadmin",{"admin":admin,"to_add":to_add,},submitter_,expect_asset=expect_asset) 

	def setblacklist(self,account='user1',duration_second=1,submitter_="admin",expect_asset=True):
		self.pushaction("setblacklist",{"account":account,"duration_second":duration_second,},submitter_,expect_asset=expect_asset) 

	def setconf(self,conf_contract='user1',token_split_contract='user1',token_split_plan_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("setconf",{"conf_contract":conf_contract,"token_split_contract":token_split_contract,"token_split_plan_id":token_split_plan_id,},submitter_,expect_asset=expect_asset) 

	def setdearbiter(self,deal_id=1,new_arbiter='user1',submitter_="admin",expect_asset=True):
		self.pushaction("setdearbiter",{"deal_id":deal_id,"new_arbiter":new_arbiter,},submitter_,expect_asset=expect_asset) 

	def setmerchant(self,sender='user1',mi=[],submitter_="admin",expect_asset=True):
		self.pushaction("setmerchant",{"sender":sender,"mi":mi,},submitter_,expect_asset=expect_asset) 

	def stakechanged(self,account='user1',quantity="0.10000000 AMAX",memo='x',submitter_="admin",expect_asset=True):
		self.pushaction("stakechanged",{"account":account,"quantity":quantity,"memo":memo,},submitter_,expect_asset=expect_asset) 

	def startarbit(self,account='user1',account_type=1,deal_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("startarbit",{"account":account,"account_type":account_type,"deal_id":deal_id,},submitter_,expect_asset=expect_asset) 

	def withdraw(self,owner='user1',quantity="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("withdraw",{"owner":owner,"quantity":quantity,},submitter_,expect_asset=expect_asset) 

	def get_admins(self,scope):
		return self.table("admins",scope).json

	def get_arbiters(self,scope):
		return self.table("arbiters",scope).json

	def get_blacklist(self,scope):
		return self.table("blacklist",scope).json

	def get_buyorders(self,scope):
		return self.table("buyorders",scope).json

	def get_deals(self,scope):
		return self.table("deals",scope).json

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_merchants(self,scope):
		return self.table("merchants",scope).json

	def get_sellorders(self,scope):
		return self.table("sellorders",scope).json
