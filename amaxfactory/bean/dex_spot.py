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
            

	def addbalance(self,owner='user1',quant="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("addbalance",{"owner":owner,"quant":quant,},submitter_,expect_asset=expect_asset) 

	def addsymbol(self,trade_symbol='8,AMAX',deposit_symbol=[],submitter_="admin",expect_asset=True):
		self.pushaction("addsymbol",{"trade_symbol":trade_symbol,"deposit_symbol":deposit_symbol,},submitter_,expect_asset=expect_asset) 

	def batchcancel(self,owner='user1',delegated='true',tpcode='user1',type='user1',side='user1',ids=1,submitter_="admin",expect_asset=True):
		self.pushaction("batchcancel",{"owner":owner,"delegated":delegated,"tpcode":tpcode,"type":type,"side":side,"ids":ids,},submitter_,expect_asset=expect_asset) 

	def batchcancelx(self,owner='user1',delegated='true',tpcode='user1',type='user1',side='user1',ids=1,submitter_="admin",expect_asset=True):
		self.pushaction("batchcancelx",{"owner":owner,"delegated":delegated,"tpcode":tpcode,"type":type,"side":side,"ids":ids,},submitter_,expect_asset=expect_asset) 

	def blacklist(self,accounts=[],to_add='true',submitter_="admin",expect_asset=True):
		self.pushaction("blacklist",{"accounts":accounts,"to_add":to_add,},submitter_,expect_asset=expect_asset) 

	def cancelall(self,owner='user1',delegated='true',tpcode='user1',count=1,submitter_="admin",expect_asset=True):
		self.pushaction("cancelall",{"owner":owner,"delegated":delegated,"tpcode":tpcode,"count":count,},submitter_,expect_asset=expect_asset) 

	def delmembergrd(self,account='user1',submitter_="admin",expect_asset=True):
		self.pushaction("delmembergrd",{"account":account,},submitter_,expect_asset=expect_asset) 

	def init(self,submitter_="admin",expect_asset=True):
		self.pushaction("init",{},submitter_,expect_asset=expect_asset) 

	def limitbuy(self,owner='user1',delegated='true',ext_id=1,tpcode='user1',base_quant="0.10000000 AMAX",price="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("limitbuy",{"owner":owner,"delegated":delegated,"ext_id":ext_id,"tpcode":tpcode,"base_quant":base_quant,"price":price,},submitter_,expect_asset=expect_asset) 

	def limitsell(self,owner='user1',delegated='true',ext_id=1,tpcode='user1',pay_base_quant="0.10000000 AMAX",price="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("limitsell",{"owner":owner,"delegated":delegated,"ext_id":ext_id,"tpcode":tpcode,"pay_base_quant":pay_base_quant,"price":price,},submitter_,expect_asset=expect_asset) 

	def marketbuy(self,owner='user1',delegated='true',ext_id=1,tpcode='user1',pay_quote_quant="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("marketbuy",{"owner":owner,"delegated":delegated,"ext_id":ext_id,"tpcode":tpcode,"pay_quote_quant":pay_quote_quant,},submitter_,expect_asset=expect_asset) 

	def marketsell(self,owner='user1',delegated='true',ext_id=1,tpcode='user1',pay_base_quant="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("marketsell",{"owner":owner,"delegated":delegated,"ext_id":ext_id,"tpcode":tpcode,"pay_base_quant":pay_base_quant,},submitter_,expect_asset=expect_asset) 

	def match(self,matcher='user1',tpcode='user1',max_count=1,memo='x',submitter_="admin",expect_asset=True):
		self.pushaction("match",{"matcher":matcher,"tpcode":tpcode,"max_count":max_count,"memo":memo,},submitter_,expect_asset=expect_asset) 

	def notifycancel(self,order_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("notifycancel",{"order_id":order_id,},submitter_,expect_asset=expect_asset) 

	def notifyneword(self,order_id=1,order=[],submitter_="admin",expect_asset=True):
		self.pushaction("notifyneword",{"order_id":order_id,"order":order,},submitter_,expect_asset=expect_asset) 

	def notifysettle(self,deal_item=[],curr_ts=[],submitter_="admin",expect_asset=True):
		self.pushaction("notifysettle",{"deal_item":deal_item,"curr_ts":curr_ts,},submitter_,expect_asset=expect_asset) 

	def purgeall(self,tpcode='user1',type='user1',side='user1',count=1,submitter_="admin",expect_asset=True):
		self.pushaction("purgeall",{"tpcode":tpcode,"type":type,"side":side,"count":count,},submitter_,expect_asset=expect_asset) 

	def setconfig(self,conf=[],submitter_="admin",expect_asset=True):
		self.pushaction("setconfig",{"conf":conf,},submitter_,expect_asset=expect_asset) 

	def setmembergrd(self,account='user1',grade=[],delegated_trader='user1',submitter_="admin",expect_asset=True):
		self.pushaction("setmembergrd",{"account":account,"grade":grade,"delegated_trader":delegated_trader,},submitter_,expect_asset=expect_asset) 

	def setsymbol(self,trade_symbol='8,AMAX',on_off='true',submitter_="admin",expect_asset=True):
		self.pushaction("setsymbol",{"trade_symbol":trade_symbol,"on_off":on_off,},submitter_,expect_asset=expect_asset) 

	def settpcode(self,tpcode='user1',on_off='true',submitter_="admin",expect_asset=True):
		self.pushaction("settpcode",{"tpcode":tpcode,"on_off":on_off,},submitter_,expect_asset=expect_asset) 

	def settradepair(self,base_symbol='8,AMAX',quote_symbol='8,AMAX',info=[],submitter_="admin",expect_asset=True):
		self.pushaction("settradepair",{"base_symbol":base_symbol,"quote_symbol":quote_symbol,"info":info,},submitter_,expect_asset=expect_asset) 

	def settrader(self,owner='user1',delegated_trader='user1',submitter_="admin",expect_asset=True):
		self.pushaction("settrader",{"owner":owner,"delegated_trader":delegated_trader,},submitter_,expect_asset=expect_asset) 

	def withdraw(self,owner='user1',quant="0.10000000 AMAX",memo='x',submitter_="admin",expect_asset=True):
		self.pushaction("withdraw",{"owner":owner,"quant":quant,"memo":memo,},submitter_,expect_asset=expect_asset) 

	def withdrawfee(self,sym='8,AMAX',memo='x',submitter_="admin",expect_asset=True):
		self.pushaction("withdrawfee",{"sym":sym,"memo":memo,},submitter_,expect_asset=expect_asset) 

	def get_accountconfs(self,scope):
		return self.table("accountconfs",scope).json

	def get_accounts(self,scope):
		return self.table("accounts",scope).json

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
