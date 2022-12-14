from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class XDAOCONF(baseClass):
	contract = 'mdao.conf'
	def daoconf(self,feetaker='user1',appinfo=1,status='user1',daoupgfee="0.10000000 AMAX",suber='user1'):
		self.response = runaction(self.contract + f""" daoconf '["{feetaker}","{appinfo}","{status}","{daoupgfee}"]' -p {suber}""") 
		return self

	def init(self,feetaker='user1',appinfo=1,daoupgfee="0.10000000 AMAX",admin='user1',status="running",suber='user1'):
		self.response = runaction(self.contract + f""" init '["{feetaker}",{appinfo},"{daoupgfee}","{admin}","{status}"]' -p {suber}""") 
		return self

	def setmanager(self,managetype='user1',manager='user1',suber='user1'):
		self.response = runaction(self.contract + f""" setmanager '["{managetype}","{manager}"]' -p {suber}""") 
		return self

	def reset(self,suber='user1'):
		self.response = runaction(self.contract + f""" reset ']' -p {suber}""") 
		return self

	def seatconf(self,amctokenmax=1,evmtokenmax=1,dappmax=1,suber='user1'):
		self.response = runaction(self.contract + f""" seatconf '[{amctokenmax},{evmtokenmax},{dappmax}]' -p {suber}""") 
		return self

	def setlimitcode(self,symbolcode=1,suber='user1'):
		self.response = runaction(self.contract + f""" setlimitcode '["{symbolcode}"]' -p {suber}""") 
		return self

