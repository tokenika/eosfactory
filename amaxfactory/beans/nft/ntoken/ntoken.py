from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class ntoken(baseClass):
	# contract = 'versoitoken1'
	# contract = 'did.ntoken2'

	# contract = 'pass.ntoken'
	contract = 'amax.ntoken'

	def create(self,issuer='user1',maximum_supply=1,symbol=1,token_uri='x',ipowner='user1',suber='user1'):
		self.response = runaction(self.contract + f""" create '["{issuer}","{maximum_supply}",{symbol},"{token_uri}","{ipowner}"]' -p {suber}""")
		return self

	def issue(self,to='user1',quantity=1,memo='x',suber='user1'):
		self.response = runaction(self.contract + f""" issue '["{to}",{quantity},"{memo}"]' -p {suber}""")
		return self

	def notarize(self,notary='user1',token_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" notarize '["{notary}",{token_id}]' -p {suber}""") 
		return self

	def retire(self,quantity=1,memo='x',suber='user1'):
		self.response = runaction(self.contract + f""" retire '[{quantity},"{memo}"]' -p {suber}""")
		return self

	def setnotary(self,notary='user1',add='true',suber='user1'):
		self.response = runaction(self.contract + f""" setnotary '["{notary}",{add}]' -p {suber}""")
		return self

	def transfer(self,fromx='user1',to='user1',assets=1,memo='x',suber='user1'):
		self.response = runaction(self.contract + f""" transfer '["{fromx}","{to}",{assets},"{memo}"]' -p {suber}""")
		return self

	def setwhitelist(self,owner="user1",to_add="true",suber="user1"):
		self.response = runaction(self.contract + f""" setwhitelist '["{owner}",{to_add}]' -p {suber}""")
		return self