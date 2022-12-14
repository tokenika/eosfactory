from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class mart(baseClass):
	contract = 'martz'
	def cancelorder(self,maker='user1',token_id=1,order_id=1,is_sell_order='true',suber='user1'):
		self.response = runaction(self.contract + f""" cancelorder '["{maker}",{token_id},{order_id},{is_sell_order}]' -p {suber}""")
		return self

	def cancelbid(self,buyer='user1',bid_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" cancelbid '["{buyer}",{bid_id}]' -p {suber}""")
		return self

	def init(self,symbol='1',contract='xx',suber='user1'):
		self.response = runaction(self.contract + f""" init '["{symbol}","{contract}","ad",0.02,"ad",0.02]' -p {suber}""")
		return self
	def init2(self,suber='user1'):
		self.response = runaction(self.contract + f""" init '[]' -p {suber}""")
		return self
	def takebuybid(self,issuer='user1',token_id=1,buy_order_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" takebuybid '["{issuer}",{token_id},{buy_order_id}]' -p {suber}""")
		return self

	def takeselorder(self,issuer='user1',token_id=1,sell_order_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" takeselorder '["{issuer}",{token_id},{sell_order_id}]' -p {suber}""") 
		return self

