from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class PASSLOCK(baseClass):
	contract = 'p2.lock'
	def addplan(self,owner='user1',title='x',asset_contract='p2.lock',asset_symbol=1,unlock_interval_days=5,unlock_times=1,suber='user1'):
		self.response = runaction(self.contract + f""" addplan '["{owner}","{title}","{asset_contract}",{asset_symbol},"{unlock_interval_days}","{unlock_times}"]' -p {suber}""") 
		return self

	def enableplan(self,owner='user1',plan_id=1,enabled='true',suber='user1'):
		self.response = runaction(self.contract + f""" enableplan '["{owner}",{plan_id},"{enabled}"]' -p {suber}""") 
		return self

	def setwindow(self,plan_id=1,start_at='true',finish_at='',symbol=[],suber='user1'):
		self.response = runaction(self.contract + f""" setmovwindow '[{plan_id},{symbol},"{start_at}","{finish_at}"]' -p {suber}""") 
		return self

	def init(self,nft_contract='amax.ptoken' , suber='user1'):
		self.response = runaction(self.contract + f""" init '[{nft_contract}]' -p {suber}""") 
		return self

	def setplanowner(self,owner='user1',plan_id=1,new_owner='user1',suber='user1'):
		self.response = runaction(self.contract + f""" setplanowner '["{owner}",{plan_id},"{new_owner}"]' -p {suber}""") 
		return self

	def unlock(self,owner='user1',plan_id=1,lock_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" unlock '["{owner}",{plan_id},{lock_id}]' -p {suber}""") 
		return self

