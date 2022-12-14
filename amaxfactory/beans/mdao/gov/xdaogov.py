from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class XDAOGOV(baseClass):
	contract = 'mdao.gov'
	def create(self,dao_code='user1',propose_strategy_id=1,vote_strategy_id=1,require_participation=1,require_pass=1,update_interval=1,voting_period=1,suber='user1'):
		self.response = runaction(self.contract + f""" create '["{dao_code}",{propose_strategy_id},{vote_strategy_id},{require_participation},{require_pass},{update_interval},{voting_period}]' -p {suber}""") 
		return self

	def deletegov(self,dao_code='user1',suber='user1'):
		self.response = runaction(self.contract + f""" deletegov '["{dao_code}"]' -p {suber}""") 
		return self

	def setlocktime(self,dao_code='user1',lock_time=1,suber='user1'):
		self.response = runaction(self.contract + f""" setlocktime '["{dao_code}",{lock_time}]' -p {suber}""") 
		return self

	def setpropmodel(self,dao_code='user1',propose_model='user1',suber='user1'):
		self.response = runaction(self.contract + f""" setpropmodel '["{dao_code}","{propose_model}"]' -p {suber}""") 
		return self

	def setproposestg(self,dao_code='user1',propose_strategy_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" setproposestg '["{dao_code}",{propose_strategy_id}]' -p {suber}""") 
		return self

	def setvotestg(self,dao_code='user1',vote_strategy_id=1,require_participation=1,require_pass=1,suber='user1'):
		self.response = runaction(self.contract + f""" setvotestg '["{dao_code}",{vote_strategy_id},{require_participation},{require_pass}]' -p {suber}""") 
		return self

	def setvotetime(self,dao_code='user1',vote_time=1,suber='user1'):
		self.response = runaction(self.contract + f""" setvotetime '["{dao_code}",{vote_time}]' -p {suber}""") 
		return self

