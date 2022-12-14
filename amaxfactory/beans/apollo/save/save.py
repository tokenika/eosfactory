from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class SAVE(baseClass):
	contract = 'amax.save'
	def collectint(self,issuer='user1',owner='user1',save_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" collectint '["{issuer}","{owner}",{save_id}]' -p {suber}""") 
		return self

	def delplan(self,plan_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" delplan '[{plan_id}]' -p {suber}""") 
		return self

	def init(self,admin="ad",ptoken=1,itoken=1,pc=1,suber='user1'):
		self.response = runaction(self.contract + f""" init '["{admin}",{ptoken},{itoken},{pc}]' -p {suber}""") 
		return self

	def setplan(self,plan_id=1,pc=1,suber='user1'):
		self.response = runaction(self.contract + f""" setplan '[{plan_id},{pc}]' -p {suber}""") 
		return self

	def splitshare(self,issuer='user1',owner='user1',suber='user1'):
		self.response = runaction(self.contract + f""" splitshare '["{issuer}","{owner}"]' -p {suber}""") 
		return self

	def withdraw(self,issuer='user1',owner='user1',plan_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" withdraw '["{issuer}","{owner}",{plan_id}]' -p {suber}""") 
		return self

