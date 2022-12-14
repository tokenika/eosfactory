from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class hotpotbuy(baseClass):
	# contract = 'hbuy'
	contract = "hotpotalgoex"
	def init(self,admin='user1',suber='user1'):
		self.response = runaction(self.contract + f""" init '["{admin}"]' -p {suber}""") 
		return self

	def setadmin(self,admin_type='user1',admin='user1',suber='user1'):
		self.response = runaction(self.contract + f""" setadmin '["{admin_type}","{admin}"]' -p {suber}""") 
		return self

	def setlauncher(self,creator='user1',base_code=1,launcher='user1',recv_memo='x',suber='user1'):
		self.response = runaction(self.contract + f""" setlauncher '["{creator}","{base_code}","{launcher}","{recv_memo}"]' -p {suber}""") 
		return self

	def setlimitsym(self,sym_codes=1,suber='user1'):
		self.response = runaction(self.contract + f""" setlimitsym '[{sym_codes}]' -p {suber}""") 
		return self

	def setmktstatus(self,creator='user1',base_code=1,status='user1',suber='user1'):
		self.response = runaction(self.contract + f""" setmktstatus '["{creator}","{base_code}","{status}"]' -p {suber}""") 
		return self

	def setstatus(self,status_type='user1',suber='user1'):
		self.response = runaction(self.contract + f""" setstatus '["{status_type}"]' -p {suber}""") 
		return self

	def settaxtaker(self,creator='user1',base_code=1,taxker='user1',recv_memo='x',suber='user1'):
		self.response = runaction(self.contract + f""" settaxtaker '["{creator}","{base_code}","{taxker}","{recv_memo}"]' -p {suber}""") 
		return self

	def updateappinf(self,creator='user1',base_code=1,app_info=1,suber='user1'):
		self.response = runaction(self.contract + f""" updateappinf '["{creator}","{base_code}",{app_info}]' -p {suber}""") 
		return self

