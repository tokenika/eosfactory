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
            

	def addonedeal(self,deal_item=[],curr_ts=[],submitter_="admin",expect_asset=True):
		self.pushaction("addonedeal",{"deal_item":deal_item,"curr_ts":curr_ts,},submitter_,expect_asset=expect_asset) 

	def batchcancel(self,submitter='user1',pair_code='user1',type='user1',side='user1',ids=1,submitter_="admin",expect_asset=True):
		self.pushaction("batchcancel",{"submitter":submitter,"pair_code":pair_code,"type":type,"side":side,"ids":ids,},submitter_,expect_asset=expect_asset) 

	def blacklist(self,targets=[],to_add='true',submitter_="admin",expect_asset=True):
		self.pushaction("blacklist",{"targets":targets,"to_add":to_add,},submitter_,expect_asset=expect_asset) 

	def cancel(self,tpcode='user1',type='user1',side='user1',order_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("cancel",{"tpcode":tpcode,"type":type,"side":side,"order_id":order_id,},submitter_,expect_asset=expect_asset) 

	def cancelall(self,pair_code='user1',type='user1',side='user1',count=1,submitter_="admin",expect_asset=True):
		self.pushaction("cancelall",{"pair_code":pair_code,"type":type,"side":side,"count":count,},submitter_,expect_asset=expect_asset) 

	def cancelnotify(self,order_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("cancelnotify",{"order_id":order_id,},submitter_,expect_asset=expect_asset) 

	def cleanall(self,pair_code='user1',count=1,submitter_="admin",expect_asset=True):
		self.pushaction("cleanall",{"pair_code":pair_code,"count":count,},submitter_,expect_asset=expect_asset) 

	def delmembergrd(self,account='user1',submitter_="admin",expect_asset=True):
		self.pushaction("delmembergrd",{"account":account,},submitter_,expect_asset=expect_asset) 

	def entradepair(self,tpcode='user1',on_off='true',submitter_="admin",expect_asset=True):
		self.pushaction("entradepair",{"tpcode":tpcode,"on_off":on_off,},submitter_,expect_asset=expect_asset) 

	def init(self,submitter_="admin",expect_asset=True):
		self.pushaction("init",{},submitter_,expect_asset=expect_asset) 

	def limitbuy(self,submitter='user1',ext_id=1,tpcode='user1',pay_quote_quant="0.10000000 AMAX",base_quant="0.10000000 AMAX",price="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("limitbuy",{"submitter":submitter,"ext_id":ext_id,"tpcode":tpcode,"pay_quote_quant":pay_quote_quant,"base_quant":base_quant,"price":price,},submitter_,expect_asset=expect_asset) 

	def limitsell(self,submitter='user1',ext_id=1,tpcode='user1',pay_base_quant="0.10000000 AMAX",price="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("limitsell",{"submitter":submitter,"ext_id":ext_id,"tpcode":tpcode,"pay_base_quant":pay_base_quant,"price":price,},submitter_,expect_asset=expect_asset) 

	def marketbuy(self,submitter='user1',ext_id=1,tpcode='user1',pay_quote_quant="0.10000000 AMAX",base_quant="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("marketbuy",{"submitter":submitter,"ext_id":ext_id,"tpcode":tpcode,"pay_quote_quant":pay_quote_quant,"base_quant":base_quant,},submitter_,expect_asset=expect_asset) 

	def marketsell(self,submitter='user1',ext_id=1,tpcode='user1',pay_base_quant="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("marketsell",{"submitter":submitter,"ext_id":ext_id,"tpcode":tpcode,"pay_base_quant":pay_base_quant,},submitter_,expect_asset=expect_asset) 

	def match(self,matcher='user1',tpcode='user1',max_count=1,memo='x',submitter_="admin",expect_asset=True):
		self.pushaction("match",{"matcher":matcher,"tpcode":tpcode,"max_count":max_count,"memo":memo,},submitter_,expect_asset=expect_asset) 

	def orderchange(self,order_id=1,order=[],submitter_="admin",expect_asset=True):
		self.pushaction("orderchange",{"order_id":order_id,"order":order,},submitter_,expect_asset=expect_asset) 

	def setconfig(self,conf=[],submitter_="admin",expect_asset=True):
		self.pushaction("setconfig",{"conf":conf,},submitter_,expect_asset=expect_asset) 

	def setmembergrd(self,account='user1',grade=[],submitter_="admin",expect_asset=True):
		self.pushaction("setmembergrd",{"account":account,"grade":grade,},submitter_,expect_asset=expect_asset) 

	def setsymbol(self,trade_symbol='8,AMAX',deposit_symbol=[],withdrawable='true',submitter_="admin",expect_asset=True):
		self.pushaction("setsymbol",{"trade_symbol":trade_symbol,"deposit_symbol":deposit_symbol,"withdrawable":withdrawable,},submitter_,expect_asset=expect_asset) 

	def settradepair(self,tpcode='user1',base_symbol='8,AMAX',quote_symbol='8,AMAX',min_base_quant="0.10000000 AMAX",min_quote_quant="0.10000000 AMAX",max_base_quant="0.10000000 AMAX",max_quote_quant="0.10000000 AMAX",taker_fee_ratio=1,maker_fee_ratio=1,min_trade_base_quant="0.10000000 AMAX",min_trade_quote_quant="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("settradepair",{"tpcode":tpcode,"base_symbol":base_symbol,"quote_symbol":quote_symbol,"min_base_quant":min_base_quant,"min_quote_quant":min_quote_quant,"max_base_quant":max_base_quant,"max_quote_quant":max_quote_quant,"taker_fee_ratio":taker_fee_ratio,"maker_fee_ratio":maker_fee_ratio,"min_trade_base_quant":min_trade_base_quant,"min_trade_quote_quant":min_trade_quote_quant,},submitter_,expect_asset=expect_asset) 

	def withdraw(self,owner='user1',quant="0.10000000 AMAX",memo='x',submitter_="admin",expect_asset=True):
		self.pushaction("withdraw",{"owner":owner,"quant":quant,"memo":memo,},submitter_,expect_asset=expect_asset) 

	def withdrawfee(self,sym='8,AMAX',memo='x',submitter_="admin",expect_asset=True):
		self.pushaction("withdrawfee",{"sym":sym,"memo":memo,},submitter_,expect_asset=expect_asset) 

	def get_accountconfs(self,scope):
		return self.table("accountconfs",scope).json

	def get_accounts(self,scope):
		return self.table("accounts",scope).json

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

	def get_symbolconfs(self,scope):
		return self.table("symbolconfs",scope).json

	def get_tradepairs(self,scope):
		return self.table("tradepairs",scope).json

	def get_tradeprices(self,scope):
		return self.table("tradeprices",scope).json
