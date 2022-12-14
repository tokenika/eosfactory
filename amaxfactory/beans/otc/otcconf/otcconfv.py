from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class otcconfv(baseClass):
	# contract = 'confx1'
	contract = 'meta.conf'

	def init(self,admin='user1',suber='user1'):
		self.response = runaction(self.contract + f""" init '["{admin}"]' -p {suber}""") 
		return self

	def setappname(self,otc_name='user1',suber='user1'):
		self.response = runaction(self.contract + f""" setappname '["{otc_name}"]' -p {suber}""") 
		return self

	def setfarm(self,farmname='user1',farm_id=1,symbol='',farm_scale=1,suber='user1'):
		self.response = runaction(self.contract + f""" setfarm '["{farmname}",{farm_id},"{symbol}",{farm_scale}]' -p {suber}""") 
		return self

	def setmanager(self,type='user1',account='user1',suber='user1'):
		self.response = runaction(self.contract + f""" setmanager '["{type}","{account}"]' -p {suber}""") 
		return self

	def setsettlelv(self,configs=1,suber='user1'):
		self.response = runaction(self.contract + f""" setsettlelv '[{configs}]' -p {suber}""")
		return self

	def setstatus(self,status=1,suber='user1'):
		self.response = runaction(self.contract + f""" setstatus '[{status}]' -p {suber}""") 
		return self

	def setswapstep(self,rates=1,suber='user1'):
		self.response = runaction(self.contract + f""" setswapstep '[{rates}]' -p {suber}""")
		return self

	def settimeout(self,accepted_timeout=1,payed_timeout=1,suber='user1'):
		self.response = runaction(self.contract + f""" settimeout '[{accepted_timeout},{payed_timeout}]' -p {suber}""") 
		return self

