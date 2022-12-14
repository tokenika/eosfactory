from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class Apollo(baseClass):
	contract = 'apollo111112'
	def cancelorder(self,maker='user1',token_id=1,order_id=1,is_sell_order='true',suber='user1'):
		self.response = runaction(self.contract + f""" cancelorder '["{maker}",{token_id},{order_id},{is_sell_order}]' -p {suber}""")
		return self


	def init(self,symbol='1',contract='xx',suber='user1'):
		self.response = runaction(self.contract + f""" init '["{symbol}","{contract}"]' -p {suber}""")
		return self
	def init2(self,suber='user1'):
		self.response = runaction(self.contract + f""" init '[]' -p {suber}""")
		return self


	def setorderfee(self,order_id=1,start_at='',end_at='',fee='',suber='user1'):
		self.response = runaction(self.contract + f""" setorderfee '[{order_id},"{start_at}","{end_at}","{fee}"]' -p {suber}""") 
		return self

