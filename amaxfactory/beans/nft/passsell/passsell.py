from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class PASSSELL(baseClass):
	contract = 'pa.mart'
	#contract = 'pass.mart'
	def addpass(self,owner='user1',title='x',nft_symbol=1,gift_symbol="",price="0.10000000 AMAX",started_at=1,ended_at=1,buy_lock_plan_id=1,token_split_plan_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" addpass '["{owner}","{title}",{nft_symbol},{gift_symbol},"{price}","{started_at}","{ended_at}",{buy_lock_plan_id},{token_split_plan_id}]' -p {suber}""") 
		return self

	def cancelplan(self,owner='user1',product_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" cancelplan '[{product_id}]' -p {suber}""") 
		return self

	def delprod(self,product_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" delprod '[{product_id}]' -p {suber}""") 
		return self

	def claimrewards(self,owner='user1',product_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" claimrewards '["{owner}",{product_id}]' -p {suber}""") 
		return self

	def dealtrace(self,trace=1,suber='user1'):
		self.response = runaction(self.contract + f""" dealtrace '["{trace}"]' -p {suber}""") 
		return self

	def init(self,admin='ad',nft_contract='',gift_nft_contract='',custody_contract='',token_split_contract='',suber='user1'):
		self.response = runaction(self.contract + f""" init '["{admin}","{nft_contract}","{gift_nft_contract}","{custody_contract}","{token_split_contract}"]' -p {suber}""") 
		return self

	def setaccouts(self,nft_contract='user1',lock_contract='user1',partner_name='user1',storage_account='user1',orther='fee',suber='user1'):
		self.response = runaction(self.contract + f""" setaccouts '["{nft_contract}","{lock_contract}","{partner_name}","{storage_account}","{orther}"]' -p {suber}""") 
		return self

	def setendtime(self,pass_id='user1',sell_ended_at='',suber='user1'):
		self.response = runaction(self.contract + f""" setendtime '[{pass_id},"{sell_ended_at}"]' -p {suber}""") 
		return self

	def setclaimday(self,admin='user1',days=1,suber='user1'):
		self.response = runaction(self.contract + f""" setclaimday '["{admin}",{days}]' -p {suber}""") 
		return self

	def setrates(self,owner='user1',first_rate=1,second_rate=1,partner_rate=1,suber='user1'):
		self.response = runaction(self.contract + f""" setrates '["{owner}",{first_rate},{second_rate},{partner_rate}]' -p {suber}""") 
		return self

	def setrule(self,owner='user1',product_id=1,rule=1,suber='user1'):
		self.response = runaction(self.contract + f""" setrule '["{owner}",{product_id},"{rule}"]' -p {suber}""") 
		return self

	def setowner(self,pass_id=5,owner='user1',suber='user1'):
		self.response = runaction(self.contract + f""" setowner '[{pass_id},"{owner}"]' -p {suber}""") 
		return self

	def closepass(self,pass_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" closepass '[{pass_id}]' -p {suber}""") 
		return self