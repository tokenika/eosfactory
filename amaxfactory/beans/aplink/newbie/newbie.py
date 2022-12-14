from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class newbie(baseClass):
	contract = 'aplinknewbie'
	def claimreward(self,newbie='user1',suber='user1'):
		self.response = runaction(self.contract + f""" claimreward '[{newbie}]' -p {suber}""") 
		return self

	def recycledb(self,max_rows=1,suber='user1'):
		self.response = runaction(self.contract + f""" recycledb '[{max_rows}]' -p {suber}""") 
		return self

	def rewardinvite(self,to='user1',suber='user1'):
		self.response = runaction(self.contract + f""" rewardinvite '["{to}"]' -p {suber}""") 
		return self

	def setstate(self,enable='true',newbie_reward="0.10000000 AMAX",aplink_token_contract='user1',landid='1',contract="con",suber='user1'):
		self.response = runaction(self.contract + f""" setstate '[{enable},"{newbie_reward}","{aplink_token_contract}",{landid},"{contract}"]' -p {suber}""")
		return self
	def setstate2(self,enable='true',newbie_reward="0.10000000 AMAX",aplink_token_contract='user1',landid='1',contract="con",suber='user1'):
		self.response = runaction(self.contract + f""" setstate '["{newbie_reward}","{aplink_token_contract}","aplink.admin"]' -p {suber}""")
		return self
	def init(self,land_id=1,farm='farmx',suber='user1'):
		self.response = runaction(self.contract + f""" init '[{land_id},"{farm}"]' -p {suber}""")
		return self