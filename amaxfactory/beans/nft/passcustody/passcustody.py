from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class PASSCUSTODY(baseClass):
	contract = 'p2.lock'
	def addplan(self,owner='user1',title='x',asset_contract='user1',asset_symbol=1,unlock_interval_days=1,unlock_times=1,suber='user1'):
		self.response = runaction(self.contract + f""" addplan '["{owner}","{title}","{asset_contract}",{asset_symbol},{unlock_interval_days},"{unlock_times}"]' -p {suber}""") 
		return self

	def endissue(self,issuer='user1',plan_id=1,issue_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" endissue '["{issuer}",{plan_id},{issue_id}]' -p {suber}""") 
		return self

	def init(self,suber='user1'):
		self.response = runaction(self.contract + f""" init ']' -p {suber}""") 
		return self

	def setconfig(self,plan_fee="0.10000000 AMAX",fee_receiver='user1',suber='user1'):
		self.response = runaction(self.contract + f""" setconfig '["{plan_fee}","{fee_receiver}"]' -p {suber}""") 
		return self

	def setplanowner(self,owner='user1',plan_id=1,new_owner='user1',suber='user1'):
		self.response = runaction(self.contract + f""" setplanowner '["{owner}",{plan_id},"{new_owner}"]' -p {suber}""") 
		return self

	def unlock(self,unlocker='user1',plan_id=1,issue_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" unlock '["{unlocker}",{plan_id},{issue_id}]' -p {suber}""") 
		return self


	def setwindow(self,plan_id=1,start_at='true',finish_at='',symbol=[],suber='user1'):
		self.response = runaction(self.contract + f""" setmovwindow '[{plan_id},{symbol},"{start_at}","{finish_at}"]' -p {suber}""") 
		return self
