import os
from amaxfactory.core.account import CreateAccount
import amaxfactory.shell.account as account
import amaxfactory.shell.contract as contract
from amaxfactory.bean.bean_init import *

Contract = contract.Contract

new_account = account.new_account
create_master_account = account.create_master_account
new_master_account = account.new_master_account

class AMAX_SYSTEM(CreateAccount):
	def __init__(self,contract_name="amax.system"):
		self.name = contract_name
		master = new_master_account()
		amax_system = new_account(master,contract_name,factory=True)
		smart = Contract(amax_system, 
			wasm_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.system/amax.system.wasm",
			abi_file=os.getenv("FACTORY_DIR") + "/templates/wasm/" + "amax.system/amax.system.abi")
		smart.deploy()
		self = amax_system
		self.set_account_permission(add_code=True)
    
	def setup(self):
		try:
			amax_system_init(self)
		except:
			print("amax_system setup function not implemented!!")
		return self

	def __str__(self):
		return self.name
            

	def activate(self,feature_digest=[],submitter_="admin",expect_asset=True):
		self.pushaction("activate",{"feature_digest":feature_digest,},submitter_,expect_asset=expect_asset) 

	def bidname(self,bidder='user1',newname='user1',bid="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("bidname",{"bidder":bidder,"newname":newname,"bid":bid,},submitter_,expect_asset=expect_asset) 

	def bidrefund(self,bidder='user1',newname='user1',submitter_="admin",expect_asset=True):
		self.pushaction("bidrefund",{"bidder":bidder,"newname":newname,},submitter_,expect_asset=expect_asset) 

	def buyram(self,payer='user1',receiver='user1',quant="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("buyram",{"payer":payer,"receiver":receiver,"quant":quant,},submitter_,expect_asset=expect_asset) 

	def buyrambytes(self,payer='user1',receiver='user1',bytes=1,submitter_="admin",expect_asset=True):
		self.pushaction("buyrambytes",{"payer":payer,"receiver":receiver,"bytes":bytes,},submitter_,expect_asset=expect_asset) 

	def buyrex(self,from_='user1',amount="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("buyrex",{"from":from_,"amount":amount,},submitter_,expect_asset=expect_asset) 

	def canceldelay(self,canceling_auth=[],trx_id=[],submitter_="admin",expect_asset=True):
		self.pushaction("canceldelay",{"canceling_auth":canceling_auth,"trx_id":trx_id,},submitter_,expect_asset=expect_asset) 

	def cfgpowerup(self,args=[],submitter_="admin",expect_asset=True):
		self.pushaction("cfgpowerup",{"args":args,},submitter_,expect_asset=expect_asset) 

	def claimrewards(self,owner='user1',submitter_="admin",expect_asset=True):
		self.pushaction("claimrewards",{"owner":owner,},submitter_,expect_asset=expect_asset) 

	def closerex(self,owner='user1',submitter_="admin",expect_asset=True):
		self.pushaction("closerex",{"owner":owner,},submitter_,expect_asset=expect_asset) 

	def cnclrexorder(self,owner='user1',submitter_="admin",expect_asset=True):
		self.pushaction("cnclrexorder",{"owner":owner,},submitter_,expect_asset=expect_asset) 

	def consolidate(self,owner='user1',submitter_="admin",expect_asset=True):
		self.pushaction("consolidate",{"owner":owner,},submitter_,expect_asset=expect_asset) 

	def defcpuloan(self,from_='user1',loan_num=1,amount="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("defcpuloan",{"from":from_,"loan_num":loan_num,"amount":amount,},submitter_,expect_asset=expect_asset) 

	def defnetloan(self,from_='user1',loan_num=1,amount="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("defnetloan",{"from":from_,"loan_num":loan_num,"amount":amount,},submitter_,expect_asset=expect_asset) 

	def delegatebw(self,from_='user1',receiver='user1',stake_net_quantity="0.10000000 AMAX",stake_cpu_quantity="0.10000000 AMAX",transfer='true',submitter_="admin",expect_asset=True):
		self.pushaction("delegatebw",{"from":from_,"receiver":receiver,"stake_net_quantity":stake_net_quantity,"stake_cpu_quantity":stake_cpu_quantity,"transfer":transfer,},submitter_,expect_asset=expect_asset) 

	def deleteauth(self,account='user1',permission='user1',submitter_="admin",expect_asset=True):
		self.pushaction("deleteauth",{"account":account,"permission":permission,},submitter_,expect_asset=expect_asset) 

	def deposit(self,owner='user1',amount="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("deposit",{"owner":owner,"amount":amount,},submitter_,expect_asset=expect_asset) 

	def fundcpuloan(self,from_='user1',loan_num=1,payment="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("fundcpuloan",{"from":from_,"loan_num":loan_num,"payment":payment,},submitter_,expect_asset=expect_asset) 

	def fundnetloan(self,from_='user1',loan_num=1,payment="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("fundnetloan",{"from":from_,"loan_num":loan_num,"payment":payment,},submitter_,expect_asset=expect_asset) 

	def init(self,version=1,core='8,AMAX',submitter_="admin",expect_asset=True):
		self.pushaction("init",{"version":version,"core":core,},submitter_,expect_asset=expect_asset) 

	def linkauth(self,account='user1',code='user1',type='user1',requirement='user1',submitter_="admin",expect_asset=True):
		self.pushaction("linkauth",{"account":account,"code":code,"type":type,"requirement":requirement,},submitter_,expect_asset=expect_asset) 

	def mvfrsavings(self,owner='user1',rex="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("mvfrsavings",{"owner":owner,"rex":rex,},submitter_,expect_asset=expect_asset) 

	def mvtosavings(self,owner='user1',rex="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("mvtosavings",{"owner":owner,"rex":rex,},submitter_,expect_asset=expect_asset) 

	def newaccount(self,creator='user1',name='user1',owner=[],active=[],submitter_="admin",expect_asset=True):
		self.pushaction("newaccount",{"creator":creator,"name":name,"owner":owner,"active":active,},submitter_,expect_asset=expect_asset) 

	def onblock(self,header=[],submitter_="admin",expect_asset=True):
		self.pushaction("onblock",{"header":header,},submitter_,expect_asset=expect_asset) 

	def onerror(self,sender_id=1,sent_trx=[],submitter_="admin",expect_asset=True):
		self.pushaction("onerror",{"sender_id":sender_id,"sent_trx":sent_trx,},submitter_,expect_asset=expect_asset) 

	def powerup(self,payer='user1',receiver='user1',days=1,net_frac=[],cpu_frac=[],max_payment="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("powerup",{"payer":payer,"receiver":receiver,"days":days,"net_frac":net_frac,"cpu_frac":cpu_frac,"max_payment":max_payment,},submitter_,expect_asset=expect_asset) 

	def powerupexec(self,user='user1',max=1,submitter_="admin",expect_asset=True):
		self.pushaction("powerupexec",{"user":user,"max":max,},submitter_,expect_asset=expect_asset) 

	def refund(self,owner='user1',submitter_="admin",expect_asset=True):
		self.pushaction("refund",{"owner":owner,},submitter_,expect_asset=expect_asset) 

	def regproducer(self,producer='user1',producer_key=[],url='x',location=1,submitter_="admin",expect_asset=True):
		self.pushaction("regproducer",{"producer":producer,"producer_key":producer_key,"url":url,"location":location,},submitter_,expect_asset=expect_asset) 

	def regproducer2(self,producer='user1',producer_authority=[],url='x',location=1,submitter_="admin",expect_asset=True):
		self.pushaction("regproducer2",{"producer":producer,"producer_authority":producer_authority,"url":url,"location":location,},submitter_,expect_asset=expect_asset) 

	def regproxy(self,proxy='user1',isproxy='true',submitter_="admin",expect_asset=True):
		self.pushaction("regproxy",{"proxy":proxy,"isproxy":isproxy,},submitter_,expect_asset=expect_asset) 

	def rentcpu(self,from_='user1',receiver='user1',loan_payment="0.10000000 AMAX",loan_fund="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("rentcpu",{"from":from_,"receiver":receiver,"loan_payment":loan_payment,"loan_fund":loan_fund,},submitter_,expect_asset=expect_asset) 

	def rentnet(self,from_='user1',receiver='user1',loan_payment="0.10000000 AMAX",loan_fund="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("rentnet",{"from":from_,"receiver":receiver,"loan_payment":loan_payment,"loan_fund":loan_fund,},submitter_,expect_asset=expect_asset) 

	def rexexec(self,user='user1',max=1,submitter_="admin",expect_asset=True):
		self.pushaction("rexexec",{"user":user,"max":max,},submitter_,expect_asset=expect_asset) 

	def rmvproducer(self,producer='user1',submitter_="admin",expect_asset=True):
		self.pushaction("rmvproducer",{"producer":producer,},submitter_,expect_asset=expect_asset) 

	def sellram(self,account='user1',bytes=[],submitter_="admin",expect_asset=True):
		self.pushaction("sellram",{"account":account,"bytes":bytes,},submitter_,expect_asset=expect_asset) 

	def sellrex(self,from_='user1',rex="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("sellrex",{"from":from_,"rex":rex,},submitter_,expect_asset=expect_asset) 

	def setabi(self,account='user1',abi=[],submitter_="admin",expect_asset=True):
		self.pushaction("setabi",{"account":account,"abi":abi,},submitter_,expect_asset=expect_asset) 

	def setacctcpu(self,account='user1',cpu_weight=[],submitter_="admin",expect_asset=True):
		self.pushaction("setacctcpu",{"account":account,"cpu_weight":cpu_weight,},submitter_,expect_asset=expect_asset) 

	def setacctnet(self,account='user1',net_weight=[],submitter_="admin",expect_asset=True):
		self.pushaction("setacctnet",{"account":account,"net_weight":net_weight,},submitter_,expect_asset=expect_asset) 

	def setacctram(self,account='user1',ram_bytes=[],submitter_="admin",expect_asset=True):
		self.pushaction("setacctram",{"account":account,"ram_bytes":ram_bytes,},submitter_,expect_asset=expect_asset) 

	def setalimits(self,account='user1',ram_bytes=[],net_weight=[],cpu_weight=[],submitter_="admin",expect_asset=True):
		self.pushaction("setalimits",{"account":account,"ram_bytes":ram_bytes,"net_weight":net_weight,"cpu_weight":cpu_weight,},submitter_,expect_asset=expect_asset) 

	def setcode(self,account='user1',vmtype=1,vmversion=1,code=[],submitter_="admin",expect_asset=True):
		self.pushaction("setcode",{"account":account,"vmtype":vmtype,"vmversion":vmversion,"code":code,},submitter_,expect_asset=expect_asset) 

	def setinflation(self,inflation_start_time=[],initial_inflation_per_block="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("setinflation",{"inflation_start_time":inflation_start_time,"initial_inflation_per_block":initial_inflation_per_block,},submitter_,expect_asset=expect_asset) 

	def setparams(self,params=[],submitter_="admin",expect_asset=True):
		self.pushaction("setparams",{"params":params,},submitter_,expect_asset=expect_asset) 

	def setpriv(self,account='user1',is_priv=1,submitter_="admin",expect_asset=True):
		self.pushaction("setpriv",{"account":account,"is_priv":is_priv,},submitter_,expect_asset=expect_asset) 

	def setram(self,max_ram_size=1,submitter_="admin",expect_asset=True):
		self.pushaction("setram",{"max_ram_size":max_ram_size,},submitter_,expect_asset=expect_asset) 

	def setramrate(self,bytes_per_block=1,submitter_="admin",expect_asset=True):
		self.pushaction("setramrate",{"bytes_per_block":bytes_per_block,},submitter_,expect_asset=expect_asset) 

	def setrex(self,balance="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("setrex",{"balance":balance,},submitter_,expect_asset=expect_asset) 

	def undelegatebw(self,from_='user1',receiver='user1',unstake_net_quantity="0.10000000 AMAX",unstake_cpu_quantity="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("undelegatebw",{"from":from_,"receiver":receiver,"unstake_net_quantity":unstake_net_quantity,"unstake_cpu_quantity":unstake_cpu_quantity,},submitter_,expect_asset=expect_asset) 

	def unlinkauth(self,account='user1',code='user1',type='user1',submitter_="admin",expect_asset=True):
		self.pushaction("unlinkauth",{"account":account,"code":code,"type":type,},submitter_,expect_asset=expect_asset) 

	def unregprod(self,producer='user1',submitter_="admin",expect_asset=True):
		self.pushaction("unregprod",{"producer":producer,},submitter_,expect_asset=expect_asset) 

	def unstaketorex(self,owner='user1',receiver='user1',from_net="0.10000000 AMAX",from_cpu="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("unstaketorex",{"owner":owner,"receiver":receiver,"from_net":from_net,"from_cpu":from_cpu,},submitter_,expect_asset=expect_asset) 

	def updateauth(self,account='user1',permission='user1',parent='user1',auth=[],submitter_="admin",expect_asset=True):
		self.pushaction("updateauth",{"account":account,"permission":permission,"parent":parent,"auth":auth,},submitter_,expect_asset=expect_asset) 

	def updaterex(self,owner='user1',submitter_="admin",expect_asset=True):
		self.pushaction("updaterex",{"owner":owner,},submitter_,expect_asset=expect_asset) 

	def updtrevision(self,revision=1,submitter_="admin",expect_asset=True):
		self.pushaction("updtrevision",{"revision":revision,},submitter_,expect_asset=expect_asset) 

	def voteproducer(self,voter='user1',proxy='user1',producers=[],submitter_="admin",expect_asset=True):
		self.pushaction("voteproducer",{"voter":voter,"proxy":proxy,"producers":producers,},submitter_,expect_asset=expect_asset) 

	def withdraw(self,owner='user1',amount="0.10000000 AMAX",submitter_="admin",expect_asset=True):
		self.pushaction("withdraw",{"owner":owner,"amount":amount,},submitter_,expect_asset=expect_asset) 

	def get_abihash(self,scope):
		return self.table("abihash",scope).json

	def get_bidrefunds(self,scope):
		return self.table("bidrefunds",scope).json

	def get_cpuloan(self,scope):
		return self.table("cpuloan",scope).json

	def get_delband(self,scope):
		return self.table("delband",scope).json

	def get_global(self,scope):
		return self.table("global",scope).json

	def get_namebids(self,scope):
		return self.table("namebids",scope).json

	def get_netloan(self,scope):
		return self.table("netloan",scope).json

	def get_powup_order(self,scope):
		return self.table("powup.order",scope).json

	def get_powup_state(self,scope):
		return self.table("powup.state",scope).json

	def get_producers(self,scope):
		return self.table("producers",scope).json

	def get_rammarket(self,scope):
		return self.table("rammarket",scope).json

	def get_refunds(self,scope):
		return self.table("refunds",scope).json

	def get_retbuckets(self,scope):
		return self.table("retbuckets",scope).json

	def get_rexbal(self,scope):
		return self.table("rexbal",scope).json

	def get_rexfund(self,scope):
		return self.table("rexfund",scope).json

	def get_rexpool(self,scope):
		return self.table("rexpool",scope).json

	def get_rexqueue(self,scope):
		return self.table("rexqueue",scope).json

	def get_rexretpool(self,scope):
		return self.table("rexretpool",scope).json

	def get_userres(self,scope):
		return self.table("userres",scope).json

	def get_voters(self,scope):
		return self.table("voters",scope).json
