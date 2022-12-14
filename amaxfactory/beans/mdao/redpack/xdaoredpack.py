from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class XDAOREDPACK(baseClass):
	# contract = 'did.redpack4'
	contract = 'xredpack'

	def addfee(self,fee="0.10000000 AMAX",contract='user1',min=4,did_contract='x',did_id=1, suber='user1'):
		self.response = runaction(self.contract + f""" addfee '["{fee}","{contract}",{min},"{did_contract}",{did_id}]' -p {suber}""")
		return self


	def cancel(self,code='user1',suber='user1'):
		self.response = runaction(self.contract + f""" cancel '["{code}"]' -p {suber}""") 
		return self

	def claim(self,claimer='user1',code='user1',pwhash='x',suber='user1'):
		self.response = runaction(self.contract + f""" claimredpack '["{claimer}","{code}","{pwhash}"]' -p {suber}""") 
		return self

	def delfee(self,coin='8,AMAX',suber='user1'):
		self.response = runaction(self.contract + f""" delfee '["{coin}"]' -p {suber}""") 
		return self

	def delredpacks(self,code='user1',suber='user1'):
		self.response = runaction(self.contract + f""" delredpacks '["{code}"]' -p {suber}""") 
		return self

	def init(self,admin='user1',hours=1,send_did='',suber='user1'):
		self.response = runaction(self.contract + f""" init '["{admin}",{hours},{send_did}]' -p {suber}""") 
		return self

