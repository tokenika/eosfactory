import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class ORDERBOOKDEX(CreateAccount):
	def __init__(self,contract_name="orderbookdex"):
		self.name = contract_name
		master = new_master_account()
		orderbookdex = new_account(master,contract_name)
		smart = Contract(orderbookdex, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "orderbookdex/orderbookdex.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "orderbookdex/orderbookdex.abi")
		smart.deploy()
		self = orderbookdex
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			orderbookdex_init(self)
		except:
			print("orderbookdex setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def adddexdeal(self,deal_items=[],curr_ts=[],submitter_="admin",expect_asset=True):
		self.pushaction("adddexdeal",{"deal_items":deal_items,"curr_ts":curr_ts,},submitter_,expect_asset=expect_asset) 

	def buy(self,user='user1',sympair_id=1,quantity="0.10000000 AMAX",price="0.10000000 AMAX",external_id=1,order_config_ex=[],submitter_="admin",expect_asset=True):
		self.pushaction("buy",{"user":user,"sympair_id":sympair_id,"quantity":quantity,"price":price,"external_id":external_id,"order_config_ex":order_config_ex,},submitter_,expect_asset=expect_asset) 

	def cancel(self,pair_id=1,side='user1',order_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("cancel",{"pair_id":pair_id,"side":side,"order_id":order_id,},submitter_,expect_asset=expect_asset) 

	def cleandata(self,max_count=1,submitter_="admin",expect_asset=True):
		self.pushaction("cleandata",{"max_count":max_count,},submitter_,expect_asset=expect_asset) 

	def delsympair(self,sympair_id=1,submitter_="admin",expect_asset=True):
		self.pushaction("delsympair",{"sympair_id":sympair_id,},submitter_,expect_asset=expect_asset) 

	def init(self,submitter_="admin",expect_asset=True):
		self.pushaction("init",{},submitter_,expect_asset=expect_asset) 

	def match(self,matcher='user1',pair_id=1,max_count=1,memo='x',submitter_="admin",expect_asset=True):
		self.pushaction("match",{"matcher":matcher,"pair_id":pair_id,"max_count":max_count,"memo":memo,},submitter_,expect_asset=expect_asset) 

	def neworder(self,user='user1',sympair_id=1,order_side='user1',limit_quant="0.10000000 AMAX",frozen_quant="0.10000000 AMAX",price="0.10000000 AMAX",external_id=1,order_config_ex=[],submitter_="admin",expect_asset=True):
		self.pushaction("neworder",{"user":user,"sympair_id":sympair_id,"order_side":order_side,"limit_quant":limit_quant,"frozen_quant":frozen_quant,"price":price,"external_id":external_id,"order_config_ex":order_config_ex,},submitter_,expect_asset=expect_asset) 

	def onoffsympair(self,sympair_id=1,on_off='true',submitter_="admin",expect_asset=True):
		self.pushaction("onoffsympair",{"sympair_id":sympair_id,"on_off":on_off,},submitter_,expect_asset=expect_asset) 

	def sell(self,user='user1',sympair_id=1,quantity="0.10000000 AMAX",price="0.10000000 AMAX",external_id=1,order_config_ex=[],submitter_="admin",expect_asset=True):
		self.pushaction("sell",{"user":user,"sympair_id":sympair_id,"quantity":quantity,"price":price,"external_id":external_id,"order_config_ex":order_config_ex,},submitter_,expect_asset=expect_asset) 

	def setconfig(self,conf=[],submitter_="admin",expect_asset=True):
		self.pushaction("setconfig",{"conf":conf,},submitter_,expect_asset=expect_asset) 

	def setsympair(self,asset_symbol=[],coin_symbol=[],min_asset_quant="0.10000000 AMAX",min_coin_quant="0.10000000 AMAX",only_accept_coin_fee='true',enabled='true',submitter_="admin",expect_asset=True):
		self.pushaction("setsympair",{"asset_symbol":asset_symbol,"coin_symbol":coin_symbol,"min_asset_quant":min_asset_quant,"min_coin_quant":min_coin_quant,"only_accept_coin_fee":only_accept_coin_fee,"enabled":enabled,},submitter_,expect_asset=expect_asset) 

	def withdraw(self,user='user1',bank='user1',quant="0.10000000 AMAX",memo='x',submitter_="admin",expect_asset=True):
		self.pushaction("withdraw",{"user":user,"bank":bank,"quant":quant,"memo":memo,},submitter_,expect_asset=expect_asset) 

	def get_config(self,scope):
		return self.table("config",scope).json

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_order(self,scope):
		return self.table("order",scope).json

	def get_queue(self,scope):
		return self.table("queue",scope).json

	def get_rewards(self,scope):
		return self.table("rewards",scope).json

	def get_sympair(self,scope):
		return self.table("sympair",scope).json
