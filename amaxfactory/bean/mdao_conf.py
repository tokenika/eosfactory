import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class MDAO_CONF(CreateAccount):
	def __init__(self,contract_name="mdao.conf"):
		self.name = contract_name
		master = new_master_account()
		mdao_conf = new_account(master,contract_name,factory=True)
		smart = Contract(mdao_conf, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "mdao.conf/mdao.conf.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "mdao.conf/mdao.conf.abi")
		smart.deploy()
		self = mdao_conf
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			mdao_conf_init(self)
		except:
			print("mdao_conf setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def init(self,fee_taker='user1',app_info=[],dao_upg_fee="0.10000000 AMAX",admin='user1',status='user1',submitter_="admin",expect_asset=True):
		self.pushaction("init",{"fee_taker":fee_taker,"app_info":app_info,"dao_upg_fee":dao_upg_fee,"admin":admin,"status":status,},submitter_,expect_asset=expect_asset) 

	def migrate(self,submitter_="admin",expect_asset=True):
		self.pushaction("migrate",{},submitter_,expect_asset=expect_asset) 

	def setmanager(self,manage_type='user1',manager='user1',submitter_="admin",expect_asset=True):
		self.pushaction("setmanager",{"manage_type":manage_type,"manager":manager,},submitter_,expect_asset=expect_asset) 

	def setmetaverse(self,enable_metaverse='true',submitter_="admin",expect_asset=True):
		self.pushaction("setmetaverse",{"enable_metaverse":enable_metaverse,},submitter_,expect_asset=expect_asset) 

	def setseat(self,dappmax=1,submitter_="admin",expect_asset=True):
		self.pushaction("setseat",{"dappmax":dappmax,},submitter_,expect_asset=expect_asset) 

	def setsystem(self,token_contract='user1',ntoken_contract='user1',stake_delay_days=1,submitter_="admin",expect_asset=True):
		self.pushaction("setsystem",{"token_contract":token_contract,"ntoken_contract":ntoken_contract,"stake_delay_days":stake_delay_days,},submitter_,expect_asset=expect_asset) 

	def settokenfee(self,quantity="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("settokenfee",{"quantity":quantity,},submitter_,expect_asset=expect_asset) 

	def get_global(self,scope):
		return self.table("global",scope).json
