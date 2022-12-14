from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class RNDNFTSWAP(baseClass):
	contract = 'rndnft.swap1'
	def closebooth(self,owner='user1',quote_nft_contract='',symbol_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" closebooth '["{owner}","{quote_nft_contract}",{symbol_id}]' -p {suber}""") 
		return self

	def createbooth(self,owner='user1',title="t_title",base_nft_contract='',quote_nft_contract='',quote_nft_price='',
	opened_at='',close_at='',suber='user1'):
		self.response = runaction(self.contract + f""" createbooth '[["{owner}","{title}","{base_nft_contract}","{quote_nft_contract}",
		{quote_nft_price},"{opened_at}","{close_at}"]]' -p {suber}""") 
		return self


	def enablebooth(self,owner='user1',quote_nft_contract='',symbol_id=1,enabled='true',suber='user1'):
		self.response = runaction(self.contract + f""" enablebooth '["{owner}","{quote_nft_contract}",{symbol_id},{enabled}]' -p {suber}""") 
		return self

	def init(self,admin='user1',suber='user1'):
		self.response = runaction(self.contract + f""" init '["{admin}"]' -p {suber}""") 
		return self

	def setboothtime(self,owner='user1',quote_nft_contract='',symbol_id=1,opened_at=1,closed_at=1,suber='user1'):
		self.response = runaction(self.contract + f""" setboothtime '["{owner}","{quote_nft_contract}",{symbol_id},"{opened_at}","{closed_at}"]' -p {suber}""") 
		return self


	def dealtrace(self,trace=1,suber='user1'):
		self.response = runaction(self.contract + f""" dealtrace '["{trace}"]' -p {suber}""") 
		return self