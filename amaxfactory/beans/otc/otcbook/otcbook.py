import json

from base.amcli import runaction, gettable
from amaxfactory.beans.base.baseClass import baseClass

class otcbookv(baseClass):
	contract = 'meta.book'


	def addarbiter(self,account='user1',email=1,suber='user1'):
		self.response = runaction(self.contract + f""" addarbiter '["{account}","{email}"]' -p {suber}""") 
		return self

	def delarbiter(self,account='user1',suber='user1'):
		self.response = runaction(self.contract + f""" delarbiter '["{account}"]' -p {suber}""") 
		return self

	def ƒ(self,account_type=1,account='user1',deal_id=1,session_msg='x',suber='user1'):
		self.response = runaction(self.contract + f""" cancelarbit '[{account_type},"{account}",{deal_id},"{session_msg}"]' -p {suber}""") 
		return self

	def canceldeal(self,account='user1',account_type=1,deal_id=1,is_taker_black='true',suber='user1'):
		self.response = runaction(self.contract + f""" canceldeal '["{account}",{account_type},{deal_id},{is_taker_black}]' -p {suber}""")
		return self

	def closearbit(self,account='user1',deal_id=1,arbit_result=1,session_msg='x',suber='user1'):
		self.response = runaction(self.contract + f""" closearbit '["{account}",{deal_id},{arbit_result},"{session_msg}"]' -p {suber}""") 
		return self

	def closedeal(self,account='user1',account_type=1,deal_id=1,session_msg='x',suber='user1'):
		self.response = runaction(self.contract + f""" closedeal '["{account}",{account_type},{deal_id},"{session_msg}"]' -p {suber}""") 
		return self

	def closeorder(self,owner='user1',order_side='user1',order_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" closeorder '["{owner}","{order_side}",{order_id}]' -p {suber}""") 
		return self

	def enbmerchant(self,owner='user1',stats='true',suber='user1'):
		self.response = runaction(self.contract + f""" enbmerchant '["{owner}",{stats}]' -p {suber}""") 
		return self

	def notification(self,account='user1',info=1,memo='x',suber='user1'):
		self.response = runaction(self.contract + f""" notification '["{account}","{info}","{memo}"]' -p {suber}""") 
		return self

	def opendeal(self,taker='user1',order_side='user1',order_id=1,deal_quantity="0.10000000 AMAX",order_sn=1,session_msg='x',suber='user1'):
		self.response = runaction(self.contract + f""" opendeal '["{taker}","{order_side}",{order_id},"{deal_quantity}",{order_sn},"{session_msg}"]' -p {suber}""") 
		return self

	def openorder(self,owner='user1',order_side='user1',pay_methods=1,va_quantity="0.10000000 AMAX",va_price="0.10000000 AMAX",va_min_take_quantity="0.10000000 AMAX",va_max_take_quantity="0.10000000 AMAX",memo='x',suber='user1'):
		self.response = runaction(self.contract + f""" openorder '["{owner}","{order_side}",{pay_methods},"{va_quantity}","{va_price}","{va_min_take_quantity}","{va_max_take_quantity}","{memo}"]' -p {suber}""")
		return self

	def pauseorder(self,owner='user1',order_side='user1',order_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" pauseorder '["{owner}","{order_side}",{order_id}]' -p {suber}""") 
		return self

	def processdeal(self,account='user1',account_type=1,deal_id=1,action=1,session_msg='x',suber='user1'):
		self.response = runaction(self.contract + f""" processdeal '["{account}",{account_type},{deal_id},{action},"{session_msg}"]' -p {suber}""") 
		return self

	def resetdeal(self,account='user1',deal_id=1,session_msg='x',suber='user1'):
		self.response = runaction(self.contract + f""" resetdeal '["{account}",{deal_id},"{session_msg}"]' -p {suber}""") 
		return self

	def resumeorder(self,owner='user1',order_side='user1',order_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" resumeorder '["{owner}","{order_side}",{order_id}]' -p {suber}""") 
		return self

	def setblacklist(self,account='user1',duration_second=1,suber='user1'):
		self.response = runaction(self.contract + f""" setblacklist '["{account}",{duration_second}]' -p {suber}""") 
		return self

	def setconf(self,conf_contract='user1',suber='user1'):
		self.response = runaction(self.contract + f""" setconf '["{conf_contract}"]' -p {suber}""") 
		return self

	def setmerchant(self,merchant='user1',status=14,merchant_name='x',merchant_detail='x',email='x',memo='x',reject_reason='',by_force=1,suber='user1'):
		self.response = runaction(self.contract + f""" setmerchant '[["{merchant}","{merchant_name}",{status},"{merchant_detail}","{email}","{memo}","{reject_reason}"],{by_force}]' -p {suber}""") 
		return self

	def remerchant(self,merchant='user1',status=1,merchant_name='x',merchant_detail='x',email='x',memo='x',reject_reason='',suber='user1'):
		self.response = runaction(self.contract + f""" remerchant '[["{merchant}","{merchant_name}",{status},"{merchant_detail}","{email}","{memo}","{reject_reason}"]]' -p {suber}""") 
		return self
		
	def stakechanged(self,account='user1',quantity="0.10000000 AMAX",memo='x',suber='user1'):
		self.response = runaction(self.contract + f""" stakechanged '["{account}","{quantity}","{memo}"]' -p {suber}""") 
		return self

	def startarbit(self,account='user1',account_type=1,deal_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" startarbit '["{account}",{account_type},{deal_id}]' -p {suber}""") 
		return self

	def withdraw(self,owner='user1',quantity="0.10000000 AMAX",suber='user1'):
		self.response = runaction(self.contract + f""" withdraw '["{owner}","{quantity}"]' -p {suber}""") 
		return self


	def buyorders(self):
		return gettable(self.contract + " " + self.contract + " buyorders -l 1000 -L 1050")


	def sellorders(self):
		return gettable(self.contract + " " + self.contract + " sellorders  -l 1000 -L 1000")


	def deals(self):
		return gettable(self.contract + " " + self.contract + " deals  -l 1000 -L 1150")


	def getLastBuyorder(self):
		return json.loads(self.buyorders())['rows'][-1]


	def getLastSellorder(self):
		return json.loads(self.sellorders())['rows'][-1]


	def getLastDeal(self):
		return json.loads(self.deals())['rows'][-1]

	