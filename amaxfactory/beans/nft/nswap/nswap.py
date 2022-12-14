from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class NSWAP(baseClass):
	contract = 'nftone.swap'
	def createpool(self,owner='user1',title='x',asset_contract='user1',blindbox_contract='user1',price="0.10000000 AMAX",fee_receiver='user1',allow_to_buy_again='true',opended_at=1,opened_days=1,suber='user1'):
		self.response = runaction(self.contract + f""" createpool '["{owner}","{title}","{asset_contract}","{blindbox_contract}","{price}","{fee_receiver}",{allow_to_buy_again},"{opended_at}",{opened_days}]' -p {suber}""") 
		return self

	def dealtrace(self,trace=1,suber='user1'):
		self.response = runaction(self.contract + f""" dealtrace '["{trace}"]' -p {suber}""") 
		return self

	def editplantime(self,owner='user1',pool_id=1,opended_at=1,closed_at=1,suber='user1'):
		self.response = runaction(self.contract + f""" editplantime '["{owner}",{pool_id},"{opended_at}","{closed_at}"]' -p {suber}""") 
		return self

	def enableplan(self,owner='user1',pool_id=1,enabled='true',suber='user1'):
		self.response = runaction(self.contract + f""" enableplan '["{owner}",{pool_id},"{enabled}"]' -p {suber}""") 
		return self

	def endpool(self,owner='user1',pool_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" endpool '["{owner}",{pool_id}]' -p {suber}""") 
		return self

	def init(self,suber='user1'):
		self.response = runaction(self.contract + f""" init '[]' -p {suber}""") 
		return self

