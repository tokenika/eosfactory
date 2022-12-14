import json

from base.amcli import runaction, gettable
from amaxfactory.beans.base.baseClass import baseClass

class xchain(baseClass):
	contract = 'xchainc'
	def addchain(self,account='user1',chain='user1',base_chain='user1',common_xin_account='x',suber='user1'):
		self.response = runaction(self.contract + f""" addchain '["{account}","{chain}","{base_chain}","{common_xin_account}"]' -p {suber}""") 
		return self

	def addchaincoin(self,account='user1',chain='user1',coin='8,AMAX',fee="0.10000000 AMAX",suber='user1'):
		self.response = runaction(self.contract + f""" addchaincoin '["{chain}","{coin}","{fee}"]' -p {suber}""") 
		return self

	def addcoin(self,account='user1',coin='8,AMAX',suber='user1'):
		self.response = runaction(self.contract + f""" addcoin '["{account}","{coin}"]' -p {suber}""") 
		return self

	def cancelxinord(self,order_id=1,cancel_reason='x',suber='user1'):
		self.response = runaction(self.contract + f""" cancelxinord '[{order_id},"{cancel_reason}"]' -p {suber}""") 
		return self

	def cancelxouord(self,account='user1',order_id=1,cancel_reason='x',suber='user1'):
		self.response = runaction(self.contract + f""" cancelxouord '["{account}",{order_id},"{cancel_reason}"]' -p {suber}""") 
		return self

	def tcheckxinord(self,order_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" checkxinord '[{order_id}]' -p {suber}""") 
		return self

	def checkxouord(self,order_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" checkxouord '[{order_id}]' -p {suber}""") 
		return self

	def delchain(self,account='user1',chain='user1',suber='user1'):
		self.response = runaction(self.contract + f""" delchain '["{account}","{chain}"]' -p {suber}""") 
		return self

	def delchaincoin(self,account='user1',chain='user1',coin='8,AMAX',suber='user1'):
		self.response = runaction(self.contract + f""" delchaincoin '["{chain}","{coin}"]' -p {suber}""") 
		return self

	def delcoin(self,account='user1',coin='8,AMAX',suber='user1'):
		self.response = runaction(self.contract + f""" delcoin '["{account}","{coin}"]' -p {suber}""") 
		return self

	def init(self,admin='user1',maker='user1',checker='user1',fee_collector='user1',suber='user1'):
		self.response = runaction(self.contract + f""" init '["{admin}","{maker}","{checker}","{fee_collector}"]' -p {suber}""") 
		return self

	def mkxinorder(self,to='user1',chain_name='user1',coin_name='8,AMAX',txid='x',xin_from='x',xin_to='x',quantity="0.10000000 AMAX",suber='user1'):
		self.response = runaction(self.contract + f""" mkxinorder '["{to}","{chain_name}","{coin_name}","{txid}","{xin_from}","{xin_to}","{quantity}"]' -p {suber}""") 
		return self

	def reqxintoaddr(self,applicant='user1',applicant_account='user1',base_chain='user1',mulsign_wallet_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" reqxintoaddr '["{applicant}","{applicant_account}","{base_chain}",{mulsign_wallet_id}]' -p {suber}""") 
		return self

	def setaddress(self,applicant='user1',base_chain='user1',mulsign_wallet_id=1,xin_to='x',suber='user1'):
		self.response = runaction(self.contract + f""" setaddress '["{applicant}","{base_chain}",{mulsign_wallet_id},"{xin_to}"]' -p {suber}""") 
		return self

	def setxouconfm(self,order_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" setxouconfm '[{order_id}]' -p {suber}""") 
		return self

	def setxousent(self,order_id=1,txid='x',xout_from='x',suber='user1'):
		self.response = runaction(self.contract + f""" setxousent '[{order_id},"{txid}","{xout_from}"]' -p {suber}""") 
		return self

	def xinorders(self):
		return gettable(self.contract + " " + self.contract + " xinorders -l 10000")
	def xoutorders(self):
		return gettable(self.contract + " " + self.contract + " xoutorders -l 10000")


	def getLastXinorders(self):
		rows = json.loads(self.xinorders())['rows']
		try:
			return rows[-1]
		except:
			return {'id': -1}

	def getLastXoutorders(self):
		rows = json.loads(self.xoutorders())['rows']
		try:
			return rows[-1]
		except:
			return {'id': -1}

