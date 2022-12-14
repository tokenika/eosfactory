from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class RNDNFTMART(baseClass):
	contract = 'rndnft.mart4'
	def closebooth(self,owner='user1',booth_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" closebooth '["{owner}",{booth_id}]' -p {suber}""") 
		return self

	def createbooth(self,owner='user1',title='x',nft_contract='user1',fund_contract='user1',split_id=1,price="0.10000000 AMAX",opened_at=1,opened_days=1,suber='user1'):
		self.response = runaction(self.contract + f""" createbooth '["{owner}","{title}","{nft_contract}","{fund_contract}",{split_id},"{price}","{opened_at}",{opened_days}]' -p {suber}""") 
		return self

	def dealtrace(self,trace=1,suber='user1'):
		self.response = runaction(self.contract + f""" dealtrace '["{trace}"]' -p {suber}""") 
		return self

	def enablebooth(self,owner='user1',booth_id=1,enabled='true',suber='user1'):
		self.response = runaction(self.contract + f""" enablebooth '["{owner}",{booth_id},{enabled}]' -p {suber}""") 
		return self

	def init(self,admin='user1',fund_distributor='user1',suber='user1'):
		self.response = runaction(self.contract + f""" init '["{admin}","{fund_distributor}"]' -p {suber}""") 
		return self

	def setboothtime(self,owner='user1',booth_id=1,opened_at=1,closed_at=1,suber='user1'):
		self.response = runaction(self.contract + f""" setboothtime '["{owner}",{booth_id},"{opened_at}","{closed_at}"]' -p {suber}""") 
		return self

