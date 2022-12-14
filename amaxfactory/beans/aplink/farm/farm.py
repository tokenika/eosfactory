from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class farm(baseClass):
	contract = 'aplink.farm'
	def lease(self,tenant='user1',land_title='x',land_uri='x',banner_uri ='xx',opened_at=1,closed_at=1,suber='user1'):
		self.response = runaction(self.contract + f""" lease '["{tenant}","{land_title}","{land_uri}","{banner_uri}"]' -p {suber}""")
		return self

	def pick(self,farmer='user1',allot_ids='x',suber='user1'):
		self.response = runaction(self.contract + f""" pick '["{farmer}",{allot_ids}]' -p {suber}""")
		return self

	def allot(self,lease_id=1,farmer='user1',quantity="0.10000000 AMAX",memo='x',suber='user1'):
		self.response = runaction(self.contract + f""" allot '[{lease_id},"{farmer}","{quantity}","{memo}"]' -p {suber}""")
		return self

	def reclaimallot(self,issuer="user1",allot_id=1,memo='x',suber='user1'):
		self.response = runaction(self.contract + f""" reclaimallot '["{issuer}",{allot_id},"{memo}"]' -p {suber}""") 
		return self

	def reclaimlease(self,issuer="user1",lease_id=1,memo='x',suber='user1'):
		self.response = runaction(self.contract + f""" reclaimlease '["{issuer}",{lease_id},"{memo}"]' -p {suber}""") 
		return self

	def init(self,lord='ad',jamfactory='ck',last_lease_id = 1,last_allot_id=4,suber='user1'):
		self.response = runaction(self.contract + f""" init '["{lord}","{jamfactory}",{last_lease_id},{last_allot_id}]' -p {suber}""") 
		return self

	def setstatus(self,land_id=1,status=1,suber='user1'):
		self.response = runaction(self.contract + f""" setstatus '[{land_id},{status}]' -p {suber}""") 
		return self

	def settenant(self,land_id=1,tenant=1,suber='user1'):
		self.response = runaction(self.contract + f""" settenant '[{land_id},"{tenant}"]' -p {suber}""") 
		return self

