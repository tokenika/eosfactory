from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class apl(baseClass):
	contract = 'aplink.token'
	def burn(self,predator='user1',victim='user1',quantity="0.10000000 AMAX",suber='user1'):
		self.response = runaction(self.contract + f""" burn '["{predator}","{victim}","{quantity}"]' -p {suber}""") 
		return self

	def create(self,issuer='user1',maximum_supply="0.10000000 AMAX",suber='user1'):
		self.response = runaction(self.contract + f""" create '["{issuer}","{maximum_supply}"]' -p {suber}""") 
		return self

	def issue(self,to='user1',quantity="0.10000000 AMAX",memo='x',suber='user1'):
		self.response = runaction(self.contract + f""" issue '["{to}","{quantity}","{memo}"]' -p {suber}""") 
		return self

	def notifyreward(self,predator='user1',victim='user1',reward_quantity="0.10000000 AMAX",suber='user1'):
		self.response = runaction(self.contract + f""" notifyreward '["{predator}","{victim}","{reward_quantity}"]' -p {suber}""") 
		return self

	def open(self,owner='user1',symbol='8,AMAX',ram_payer='user1',suber='user1'):
		self.response = runaction(self.contract + f""" open '["{owner}","{symbol}","{ram_payer}"]' -p {suber}""") 
		return self

	def retire(self,quantity="0.10000000 AMAX",memo='x',suber='user1'):
		self.response = runaction(self.contract + f""" retire '["{quantity}","{memo}"]' -p {suber}""") 
		return self

	def setacctperms(self,issuer='amax',to='aplink.farm',symbol='4,APL',allowsend='true',allowrecv='true',suber='amax'):
		self.response = runaction(self.contract + f""" setacctperms '["{issuer}","{to}","{symbol}",{allowsend},{allowrecv}]' -p {suber}""")
		return self

	def transfer(self,fromx='user1',to='user1',quantity="0.10000000 AMAX",memo='x',suber='user1'):
		self.response = runaction(self.contract + f""" transfer '["{fromx}","{to}","{quantity}","{memo}"]' -p {suber}""")
		return self

