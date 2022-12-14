from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class redpack(baseClass):
	contract = 'did.redpack3'
	def addfee(self,fee="0.10000000 AMAX",contract='user1',min=4,did_contract='x',did_id=1, suber='user1'):
		self.response = runaction(self.contract + f""" addfee '["{fee}","{contract}",{min},"{did_contract}",{did_id}]' -p {suber}""")
		return self

	def cancel(self,pack_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" cancel '[{pack_id}]' -p {suber}""")
		return self

	def claim(self,claimer='user1',pack_id=1,pwhash='x',name='name',suber='user1'):
		self.response = runaction(self.contract + f""" claim '["{claimer}",{pack_id},"{pwhash}","{name}"]' -p {suber}""")
		return self

	def delfee(self,coin='8,AMAX',suber='user1'):
		self.response = runaction(self.contract + f""" delfee '["{coin}"]' -p {suber}""") 
		return self

	def setconf(self,admin='user1',hours=1,suber='user1'):
		self.response = runaction(self.contract + f""" setconf '["{admin}",{hours}]' -p {suber}""") 
		return self

