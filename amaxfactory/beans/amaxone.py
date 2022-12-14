from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class amaxone(baseClass):
	contract = 'amax.one4'
	def addswapconf(self,account='user1',amount=1,swap_tokens="0.10000000 AMAX",swap_tokens_after_adscheck="0.10000000 AMAX",total_amount="0.10000000 AMAX",remain_amount="0.10000000 AMAX",suber='user1'):
		self.response = runaction(self.contract + f""" addswapconf '["{account}",{amount},"{swap_tokens}","{swap_tokens_after_adscheck}","{total_amount}","{remain_amount}"]' -p {suber}""") 
		return self

	def aplswaplog(self,miner='user1',recd_apls="0.10000000 AMAX",swap_tokens="0.10000000 AMAX",ads_id='x',created_at=1,suber='user1'):
		self.response = runaction(self.contract + f""" aplswaplog '["{miner}","{recd_apls}","{swap_tokens}","{ads_id}","{created_at}"]' -p {suber}""") 
		return self

	def confirmads(self,id=1,suber='user1'):
		self.response = runaction(self.contract + f""" confirmads '[{id}]' -p {suber}""") 
		return self

	def delswapconf(self,account='user1',amount=1,suber='user1'):
		self.response = runaction(self.contract + f""" delswapconf '["{account}",{amount}]' -p {suber}""") 
		return self

	def init(self,admin='user1',mine_token_contract='user1',started_at=1,ended_at=1,suber='user1'):
		self.response = runaction(self.contract + f""" init '["{admin}","{mine_token_contract}","{started_at}","{ended_at}"]' -p {suber}""") 
		return self

	def onswapexpird(self,id=1,suber='user1'):
		self.response = runaction(self.contract + f""" onswapexpird '[{id}]' -p {suber}""") 
		return self

