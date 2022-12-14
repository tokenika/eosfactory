from mdao.gov.xdaogov import XDAOGOV

xdaogov = XDAOGOV()

def test_create(): xdaogov.create(dao_code='user1',propose_strategy_id=1,vote_strategy_id=1,require_participation=1,require_pass=1,update_interval=1,voting_period=1,suber='user1') 

def test_deletegov(): xdaogov.deletegov(dao_code='user1',suber='user1') 

def test_setlocktime(): xdaogov.setlocktime(dao_code='user1',lock_time=1,suber='user1') 

def test_setpropmodel(): xdaogov.setpropmodel(dao_code='user1',propose_model='user1',suber='user1') 

def test_setproposestg(): xdaogov.setproposestg(dao_code='user1',propose_strategy_id=1,suber='user1') 

def test_setvotestg(): xdaogov.setvotestg(dao_code='user1',vote_strategy_id=1,require_participation=1,require_pass=1,suber='user1') 

def test_setvotetime(): xdaogov.setvotetime(dao_code='user1',vote_time=1,suber='user1') 
