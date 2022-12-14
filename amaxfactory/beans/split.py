from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class SPLIT(baseClass):
	contract = 'amax.split'
	def addplan(self,plan_sender_contract='user1',token_symbol='8,AMAX',split_by_rate='true',suber='user1'):
		self.response = runaction(self.contract + f""" addplan '["{plan_sender_contract}","{token_symbol}",{split_by_rate}]' -p {suber}""") 
		return self

	def delplan(self,plan_sender_contract='user1',plan_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" delplan '["{plan_sender_contract}",{plan_id}]' -p {suber}""") 
		return self

	def init(self,suber='user1'):
		self.response = runaction(self.contract + f""" init '[]' -p {suber}""") 
		return self

	def setplan(self,plan_sender_contract='user1',plan_id=1,conf=1,suber='user1'):
		self.response = runaction(self.contract + f""" setplan '["{plan_sender_contract}",{plan_id},{conf}]' -p {suber}""") 
		return self

