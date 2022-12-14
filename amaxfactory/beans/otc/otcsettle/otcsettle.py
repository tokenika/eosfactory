import json
from time import sleep

from base.amcli import runaction, gettable
from amaxfactory.beans.base.baseClass import baseClass

class Otcsettle(baseClass):
	contract = 'meta.settle'
	def deal(self,deal_id=1,merchant='user1',user='user1',quantity="0.10000000 AMAX",fee="0.10000000 AMAX",arbit_status=1,start_at=1,end_at=1,suber='user1'):
		self.response = runaction(self.contract + f""" deal '[{deal_id},"{merchant}","{user}","{quantity}","{fee}",{arbit_status},"{start_at}","{end_at}"]' -p {suber}""")
		return self

	def pick(self,reciptian='user1',rewards=1,suber='user1'):
		self.response = runaction(self.contract + f""" claim '["{reciptian}",{rewards}]' -p {suber}""") 
		return self


	def setadmin(self,admin='user1',market='user1',swap='user1',suber='user1'):
		self.response = runaction(self.contract + f""" setadmin '["{admin}","{market}","{swap}"]' -p {suber}""") 
		return self

	def setconf(self,conf=1,suber='user1'):
		self.response = runaction(self.contract + f""" setconf '["{conf}"]' -p {suber}""")
		return self

	def setlevel(self,user='user1',level=1,suber='user1'):
		self.response = runaction(self.contract + f""" setlevel '["{user}",{level}]' -p {suber}""") 
		return self

	def getRewards(self):
		sleep(0.1)
		return gettable(self.contract + " " + self.contract + " rewards -l 10000")

	def getSettles(self):
		sleep(0.1)
		return gettable(self.contract + " " + self.contract + " settles -l 10000")

	def getSettle(self, name):
		for settle in json.loads(self.getSettles())['rows']:
			if name == settle['account']:
				return settle
		return {}

	def getLastReward(self):
		rows = json.loads(self.getRewards())['rows']
		try:
			return rows[-1]
		except:
			return {'id': -1}