from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class tgbind(baseClass):
	contract = 'tgbind'
	def bind(self,account='user1',tgid=1,suber='user1'):
		self.response = runaction(self.contract + f""" bind '["{account}",{tgid}]' -p {suber}""") 
		return self

	def confirm(self,tgid=1,suber='user1'):
		self.response = runaction(self.contract + f""" confirm '[{tgid}]' -p {suber}""") 
		return self

	def delbind(self,tgid=1,suber='user1'):
		self.response = runaction(self.contract + f""" delbind '[{tgid}]' -p {suber}""") 
		return self

	def init(self,account='user1',suber='user1'):
		self.response = runaction(self.contract + f""" init '["{account}"]' -p {suber}""") 
		return self

