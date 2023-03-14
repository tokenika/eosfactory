import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class MDAO_INFO(CreateAccount):
	def __init__(self,contract_name="mdao.info"):
		self.name = contract_name
		master = new_master_account()
		mdao_info = new_account(master,contract_name,factory=True)
		smart = Contract(mdao_info, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "mdao.info/mdao.info.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "mdao.info/mdao.info.abi")
		smart.deploy()
		self = mdao_info
		self.set_account_permission(add_code=True)
    
	def setup(self):
		mdao_info_init(self)
		return self

	def __str__(self):
		return self.name
            

	def binddapps(self,owner='user1',code='user1',dapps=[],submitter_="admin",expect_asset=True):
		self.pushaction("binddapps",{"owner":owner,"code":code,"dapps":dapps,},submitter_,expect_asset=expect_asset) 

	def bindntoken(self,owner='user1',code='user1',ntoken=[],submitter_="admin",expect_asset=True):
		self.pushaction("bindntoken",{"owner":owner,"code":code,"ntoken":ntoken,},submitter_,expect_asset=expect_asset) 

	def bindtoken(self,owner='user1',code='user1',token=[],submitter_="admin",expect_asset=True):
		self.pushaction("bindtoken",{"owner":owner,"code":code,"token":token,},submitter_,expect_asset=expect_asset) 

	def deldao(self,admin='user1',code='user1',submitter_="admin",expect_asset=True):
		self.pushaction("deldao",{"admin":admin,"code":code,},submitter_,expect_asset=expect_asset) 

	def transferdao(self,owner='user1',code='user1',receiver='user1',submitter_="admin",expect_asset=True):
		self.pushaction("transferdao",{"owner":owner,"code":code,"receiver":receiver,},submitter_,expect_asset=expect_asset) 

	def updatecode(self,admin='user1',code='user1',new_code='user1',submitter_="admin",expect_asset=True):
		self.pushaction("updatecode",{"admin":admin,"code":code,"new_code":new_code,},submitter_,expect_asset=expect_asset) 

	def updatedao(self,owner='user1',code='user1',logo='x',desc='x',links=[],symcode='x',symcontract='x',groupid='x',submitter_="admin",expect_asset=True):
		self.pushaction("updatedao",{"owner":owner,"code":code,"logo":logo,"desc":desc,"links":links,"symcode":symcode,"symcontract":symcontract,"groupid":groupid,},submitter_,expect_asset=expect_asset) 

	def updatestatus(self,code='user1',isenable='true',submitter_="admin",expect_asset=True):
		self.pushaction("updatestatus",{"code":code,"isenable":isenable,},submitter_,expect_asset=expect_asset) 

	def get_infos(self,scope):
		return self.table("infos",scope).json
