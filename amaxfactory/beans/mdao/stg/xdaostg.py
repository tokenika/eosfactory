from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass

class XDAOSTG(baseClass):
	contract = 'mdao.stg'
	def balancestg(self,creator='user1',stg_name='x',weight_value=1,type='user1',ref_contract='user1',ref_sym=1,suber='user1'):
		self.response = runaction(self.contract + f""" balancestg '["{creator}","{stg_name}",{weight_value},"{type}","{ref_contract}",{ref_sym}]' -p {suber}""") 
		return self

	def create(self,creator='user1',stg_name='x',stg_algo='x',type='user1',ref_contract='user1',ref_sym=1,suber='user1'):
		self.response = runaction(self.contract + f""" create '["{creator}","{stg_name}","{stg_algo}","{type}","{ref_contract}",{ref_sym}]' -p {suber}""") 
		return self

	def publish(self,creator='user1',stg_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" publish '["{creator}",{stg_id}]' -p {suber}""") 
		return self

	def remove(self,creator='user1',stg_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" remove '["{creator}",{stg_id}]' -p {suber}""") 
		return self

	def setalgo(self,creator='user1',stg_id=1,stg_algo='x',suber='user1'):
		self.response = runaction(self.contract + f""" setalgo '["{creator}",{stg_id},"{stg_algo}"]' -p {suber}""") 
		return self

	def testalgo(self,account='user1',stg_id=1,suber='user1'):
		self.response = runaction(self.contract + f""" testalgo '["{account}",{stg_id}]' -p {suber}""") 
		return self

	def thresholdstg(self,creator='user1',stg_name='x',threshold_value=1,type='user1',ref_contract='user1',ref_sym=1,suber='user1'):
		self.response = runaction(self.contract + f""" thresholdstg '["{creator}","{stg_name}",{threshold_value},"{type}","{ref_contract}",{ref_sym}]' -p {suber}""") 
		return self

	def verify(self,creator='user1',stg_id=1,value=1,expect_weight=1,suber='user1'):
		self.response = runaction(self.contract + f""" verify '["{creator}",{stg_id},{value},{expect_weight}]' -p {suber}""") 
		return self

