from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class XDAOINFO(baseClass):
	contract = 'mdao.info'
	def binddapps(self,owner='user1',code='user1',dapps=1,suber='user1'):
		self.response = runaction(self.contract + f""" binddapps '["{owner}","{code}",{dapps}]' -p {suber}""") 
		return self

	def bindgov(self,owner='user1',code='user1',govid=1,suber='user1'):
		self.response = runaction(self.contract + f""" bindgov '["{owner}","{code}",{govid}]' -p {suber}""") 
		return self

	def bindtoken(self,owner='user1',code='user1',token=1,suber='user1'):
		self.response = runaction(self.contract + f""" bindtoken '["{owner}","{code}",{token}]' -p {suber}""") 
		return self

	def bindwal(self,owner='user1',code='user1',walletid=1,suber='user1'):
		self.response = runaction(self.contract + f""" bindwal '["{owner}","{code}",{walletid}]' -p {suber}""") 
		return self

	def createtoken(self,code='user1',owner='user1',taketranratio=1,takegasratio=1,fullname='x',maximum_supply="0.10000000 AMAX",suber='user1'):
		self.response = runaction(self.contract + f""" createtoken '["{code}","{owner}",{taketranratio},{takegasratio},"{fullname}","{maximum_supply}"]' -p {suber}""") 
		return self

	def delparam(self,owner='user1',code='user1',tokens=1,suber='user1'):
		self.response = runaction(self.contract + f""" delparam '["{owner}","{code}","{tokens}"]' -p {suber}""") 
		return self

	def recycledb(self,max_rows=1,suber='user1'):
		self.response = runaction(self.contract + f""" recycledb '[{max_rows}]' -p {suber}""") 
		return self

	def setstrategy(self,owner='user1',code='user1',stgtype='user1',stgid=1,suber='user1'):
		self.response = runaction(self.contract + f""" setstrategy '["{owner}","{code}","{stgtype}",{stgid}]' -p {suber}""") 
		return self

	def updatedao(self,owner='user1',code='user1',logo='x',desc='x',links=1,symcode='x',symcontract='x',groupid='x',suber='user1'):
		self.response = runaction(self.contract + f""" updatedao '["{owner}","{code}","{logo}","{desc}",{links},"{symcode}","{symcontract}","{groupid}"]' -p {suber}""") 
		return self

	def updatestatus(self,code='user1',isenable='true',suber='user1'):
		self.response = runaction(self.contract + f""" updatestatus '["{code}","{isenable}"]' -p {suber}""") 
		return self

	def updatecode(self,admin='',code='user1',newcode='true',suber='user1'):
		self.response = runaction(self.contract + f""" updatecode '["{admin}","{code}","{newcode}"]' -p {suber}""") 
		return self
	
	def deldao(self,admin='',code='user1',suber='user1'):
		self.response = runaction(self.contract + f""" deldao '["{admin}","{code}"]' -p {suber}""") 
		return self

	def transferdao(self,owner='',code='user1',receiver='true',suber='user1'):
		self.response = runaction(self.contract + f""" transferdao '["{owner}","{code}","{receiver}"]' -p {suber}""") 
		return self