import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class DEX_SPOT(CreateAccount):
	def __init__(self,contract_name="dex.spot"):
		self.name = contract_name
		master = new_master_account()
		dex_spot = new_account(master,contract_name,factory=True)
		smart = Contract(dex_spot, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "dex.spot/dex.spot.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "dex.spot/dex.spot.abi")
		smart.deploy()
		self = dex_spot
		self.set_account_permission(add_code=True)
    
	def setup(self):
		dex_spot_init(self)
		return self

	def __str__(self):
		return self.name
            

	def addsingldeal(self,deal_item=[],curr_ts=[],submitter_="admin",expect_asset=True):
		self.pushaction("addsingldeal",{"deal_item":deal_item,"curr_ts":curr_ts,},submitter_,expect_asset=expect_asset) 

	def bashcancel(self,submitter='user1',pair_code='user1',type='user1',side='user1',ids=1,submitter_="admin",expect_asset=True):
		self.pushaction("bashcancel",{"submitter":submitter,"pair_code":pair_code,"type":type,"side":side,"ids":ids,},submitter_,expect_asset=expect_asset) 

	def blacklist(self,targets=[],to_add='true',submitter_="admin",expect_asset=True):
		self.pushaction("blacklist",{"targets":targets,"to_add":to_add,},submitter_,expect_asset=expect_asset) 

	def cancel(self,pair_code='user1',type='user1',side='user1',order_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("cancel",{"pair_code":pair_code,"type":type,"side":side,"order_id":order_id,},submitter_,expect_asset=expect_asset) 

	def cancelall(self,pair_code='user1',type='user1',side='user1',count=1,submitter_="admin",expect_asset=True):
		self.pushaction("cancelall",{"pair_code":pair_code,"type":type,"side":side,"count":count,},submitter_,expect_asset=expect_asset) 

	def delmembergrd(self,account='user1',submitter_="admin",expect_asset=True):
		self.pushaction("delmembergrd",{"account":account,},submitter_,expect_asset=expect_asset) 

	def init(self,submitter_="admin",expect_asset=True):
		self.pushaction("init",{},submitter_,expect_asset=expect_asset) 

	def match(self,matcher='user1',pair_code='user1',max_count=1,memo='x',submitter_="admin",expect_asset=True):
		self.pushaction("match",{"matcher":matcher,"pair_code":pair_code,"max_count":max_count,"memo":memo,},submitter_,expect_asset=expect_asset) 

	def opensympair(self,sympair_code='user1',on_off='true',submitter_="admin",expect_asset=True):
		self.pushaction("opensympair",{"sympair_code":sympair_code,"on_off":on_off,},submitter_,expect_asset=expect_asset) 

	def orderchange(self,order_id=1,order=[],submitter_="admin",expect_asset=True):
		self.pushaction("orderchange",{"order_id":order_id,"order":order,},submitter_,expect_asset=expect_asset) 

	def residuenote(self,order_id=1,quant="0.10000000 AMAX",curr_ts=[],submitter_="admin",expect_asset=True):
		self.pushaction("residuenote",{"order_id":order_id,"quant":quant,"curr_ts":curr_ts,},submitter_,expect_asset=expect_asset) 

	def setconfig(self,conf=[],submitter_="admin",expect_asset=True):
		self.pushaction("setconfig",{"conf":conf,},submitter_,expect_asset=expect_asset) 

	def setmembergrd(self,account='user1',grade=[],submitter_="admin",expect_asset=True):
		self.pushaction("setmembergrd",{"account":account,"grade":grade,},submitter_,expect_asset=expect_asset) 

	def setsympair(self,sympair_code='user1',base_symbol=[],quote_symbol=[],min_base_quant="0.10000000 AMAX",min_quote_quant="0.10000000 AMAX",max_base_quant="0.10000000 AMAX",max_quote_quant="0.10000000 AMAX",taker_fee_ratio=1,maker_fee_ratio=1,min_deal_base_quant="0.10000000 AMAX",min_deal_quote_quant="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("setsympair",{"sympair_code":sympair_code,"base_symbol":base_symbol,"quote_symbol":quote_symbol,"min_base_quant":min_base_quant,"min_quote_quant":min_quote_quant,"max_base_quant":max_base_quant,"max_quote_quant":max_quote_quant,"taker_fee_ratio":taker_fee_ratio,"maker_fee_ratio":maker_fee_ratio,"min_deal_base_quant":min_deal_base_quant,"min_deal_quote_quant":min_deal_quote_quant,},submitter_,expect_asset=expect_asset) 

	def withdraw(self,bank='user1',quant="0.10000000 AMAX",memo='x',submitter_="admin",expect_asset=True):
		self.pushaction("withdraw",{"bank":bank,"quant":quant,"memo":memo,},submitter_,expect_asset=expect_asset) 

	def get_accountconfs(self,scope):
		return self.table("accountconfs",scope).json

	def get_balances(self,scope):
		return self.table("balances",scope).json

	def get_blacklist(self,scope):
		return self.table("blacklist",scope).json

	def get_config(self,scope):
		return self.table("config",scope).json

	def get_deals(self,scope):
		return self.table("deals",scope).json

	def get_feepool(self,scope):
		return self.table("feepool",scope).json

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_order(self,scope):
		return self.table("order",scope).json

	def get_sympair(self,scope):
		return self.table("sympair",scope).json
