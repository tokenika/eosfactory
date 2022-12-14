from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class DID(baseClass):
	contract = 'amax.did'
	def addvendor(self,vendor_name='x',vendor_account='user1',kyc_level=1,user_reward_quant="0.10000000 AMAX",user_charge_amount="0.10000000 AMAX",nft_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" addvendor '["{vendor_name}","{vendor_account}",{kyc_level},"{user_reward_quant}","{user_charge_amount}",{nft_id}]' -p {suber}""") 
		return self

	def chgvendor(self,vendor_id=1,status='user1',suber='user1'):
		self.response = runaction(self.contract + f""" chgvendor '[{vendor_id},"{status}"]' -p {suber}""") 
		return self

	def finishdid(self,order_id=1,msg='',suber='user1'):
		self.response = runaction(self.contract + f""" finishdid '[{order_id},"{msg}"]' -p {suber}""") 
		return self
	def faildid(self,order_id=1,reason='',suber='user1'):
		self.response = runaction(self.contract + f""" faildid '[{order_id},"{reason}"]' -p {suber}""") 
		return self

	def init(self,admin='user1',nft_contract='user1',fee_colletor='user1',lease_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" init '["{admin}","{nft_contract}","{fee_colletor}",{lease_id}]' -p {suber}""") 
		return self

