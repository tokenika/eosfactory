from aplink.apltoken.apl import apl as a
apl= a()

def test_burn(): apl.burn(predator='user1',victim='user1',quantity="0.10000000 AMAX",suber='user1')
def test_create(): apl.create(issuer='ad',maximum_supply="100000000000.0000 APL",suber=apl.contract) 
def test_issue(): apl.issue(to='ad',quantity="100000000000.0000 APL",memo='x',suber='ad') 
def test_notifyreward(): apl.notifyreward(predator='user1',victim='user1',reward_quantity="0.10000000 AMAX",suber='user1') 
def test_open(): apl.open(owner='user1',symbol='8,AMAX',ram_payer='user1',suber='user1') 
def test_retire(): apl.retire(quantity="0.10000000 AMAX",memo='x',suber='user1') 
def test_setacctperms(): apl.setacctperms(issuer='ad',to='ad',symbol='4,APL',allowsend='true',allowrecv='true',suber='ad')
def test_transfer(): apl.transfer(fromx='ad',to='merchantxpro',quantity="10000.0000 APL",memo='3',suber='ad')





