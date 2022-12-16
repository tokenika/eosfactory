import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class MDAO_PROPOSE(CreateAccount):
	def __init__(self,contract_name="mdao.propose"):
		self.name = contract_name
		master = new_master_account()
		mdao_propose = new_account(master,contract_name)
		smart = Contract(mdao_propose, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "mdao.propose/mdao.propose.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "mdao.propose/mdao.propose.abi")
		smart.deploy()
		self = mdao_propose
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			mdao_propose_init(self)
		except:
			print("mdao_propose setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def addplan(self,owner='user1',proposal_id=1,title='x',desc='x',suber="admin",expect_asset=True):
		self.pushaction("addplan",{"owner":owner,"proposal_id":proposal_id,"title":title,"desc":desc,},suber,expect_asset=expect_asset) 

	def cancel(self,owner='user1',proposalid=1,suber="admin",expect_asset=True):
		self.pushaction("cancel",{"owner":owner,"proposalid":proposalid,},suber,expect_asset=expect_asset) 

	def create(self,creator='user1',dao_code='user1',title='x',desc='x',suber="admin",expect_asset=True):
		self.pushaction("create",{"creator":creator,"dao_code":dao_code,"title":title,"desc":desc,},suber,expect_asset=expect_asset) 

	def execute(self,proposal_id=1,suber="admin",expect_asset=True):
		self.pushaction("execute",{"proposal_id":proposal_id,},suber,expect_asset=expect_asset) 

	def setaction(self,owner='user1',proposal_id=1,action_name='user1',data=[],title='x',suber="admin",expect_asset=True):
		self.pushaction("setaction",{"owner":owner,"proposal_id":proposal_id,"action_name":action_name,"data":data,"title":title,},suber,expect_asset=expect_asset) 

	def startvote(self,creator='user1',proposal_id=1,suber="admin",expect_asset=True):
		self.pushaction("startvote",{"creator":creator,"proposal_id":proposal_id,},suber,expect_asset=expect_asset) 

	def votefor(self,voter='user1',proposal_id=1,title='x',vote='user1',suber="admin",expect_asset=True):
		self.pushaction("votefor",{"voter":voter,"proposal_id":proposal_id,"title":title,"vote":vote,},suber,expect_asset=expect_asset) 

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_proposals(self,scope):
		return self.table("proposals",scope).json

	def get_votes(self,scope):
		return self.table("votes",scope).json
