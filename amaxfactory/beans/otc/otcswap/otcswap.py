from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class OTCSWAP(baseClass):
	contract = 'meta.swap'
	def setconf(self,conf='user1',suber='user1'):
		self.response = runaction(self.contract + f""" setconf '["{conf}"]' -p {suber}""")
		return self

	def settleto(self,user='user1',fee="0.10000000 AMAX",quantity="0.10000000 AMAX",suber='user1'):
		self.response = runaction(self.contract + f""" settleto '["{user}","{fee}","{quantity}"]' -p {suber}""") 
		return self

