from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class XDAOPROPOSE(baseClass):
	contract = 'mdao.propose'
	def addplan(self,owner='user1',proposal_id=1,title='x',desc='x',suber='user1'):
		self.response = runaction(self.contract + f""" addplan '["{owner}",{proposal_id},"{title}","{desc}"]' -p {suber}""") 
		return self

	def cancel(self,owner='user1',proposalid=1,suber='user1'):
		self.response = runaction(self.contract + f""" cancel '["{owner}",{proposalid}]' -p {suber}""") 
		return self

	def create(self,creator='user1',dao_code='user1',title='x',desc='x',suber='user1'):
		self.response = runaction(self.contract + f""" create '["{creator}","{dao_code}","{title}","{desc}"]' -p {suber}""") 
		return self

	def deletepropose(self,id=1,suber='user1'):
		self.response = runaction(self.contract + f""" deletepropose '[{id}]' -p {suber}""") 
		return self

	def deletevote(self,id=1,suber='user1'):
		self.response = runaction(self.contract + f""" deletevote '[{id}]' -p {suber}""") 
		return self

	def execute(self,proposal_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" execute '[{proposal_id}]' -p {suber}""") 
		return self

	def recycledb(self,max_rows=1,suber='user1'):
		self.response = runaction(self.contract + f""" recycledb '[{max_rows}]' -p {suber}""") 
		return self

	def setaction(self,owner='user1',proposal_id=1,action_name='user1',data=1,title='x',suber='user1'):
		self.response = runaction(self.contract + f""" setaction '["{owner}",{proposal_id},"{action_name}",{data},"{title}"]' -p {suber}""") 
		return self

	def startvote(self,executor='user1',proposal_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" startvote '["{executor}",{proposal_id}]' -p {suber}""") 
		return self

	def votefor(self,voter='user1',proposal_id=1,title='x',vote='user1',suber='user1'):
		self.response = runaction(self.contract + f""" votefor '["{voter}",{proposal_id},"{title}","{vote}"]' -p {suber}""") 
		return self

