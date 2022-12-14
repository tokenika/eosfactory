from did.didntoken.didntoken import DIDNTOKEN
didntoken = DIDNTOKEN()


def test_create(): didntoken.create(issuer='ad',maximum_supply=10000000,symbol=[1,0],token_uri='x',ipowner='ad',suber='ad') 
def test_issue(): didntoken.issue(to='ad',quantity=[100000,[1,0]],memo='x',suber='ad') 
def test_notarize(): didntoken.notarize(notary='user1',token_id=1,suber='user1') 
def test_retire(): didntoken.retire(quantity=1,memo='x',suber='user1') 
def test_setacctperms(): didntoken.setacctperms(issuer='ad',to='amax.did',symbol=[1,0],allowsend='true',allowrecv='true',suber='ad') 
def test_setnotary(): didntoken.setnotary(notary='user1',to_add='true',suber='user1') 
def test_transfer(): didntoken.transfer(fromx='ad',to='amax.did',assets=[[10000,[1,0]]],memo='refuel',suber='ad') 
def test_transfer2(): didntoken.transfer(fromx='amax.did2',to='merchantxpro',assets=[[1,[1,0]]],memo='x',suber='amax.did2') 
def test_transfer3(): didntoken.transfer(fromx='merchantxpro',to='amax.did2',assets=[[1,[1,0]]],memo='x',suber='merchantxpro') 
