from kverso.vntoken.vntoken import VNTOKEN
vntoken = VNTOKEN()


def test_create(): vntoken.create(issuer='user1', maximum_supply=30000, symbol=[2002,0],
                                  token_uri='2002', ipowner='user1', token_type="kuzi", suber='user1')


def test_issue(): vntoken.issue(to='user1', quantity=[3000,[2002,0]], memo='x', suber='user1')
def test_notarize(): vntoken.notarize(notary='user1', token_id=199, suber='user1')
def test_retire(): vntoken.retire(quantity=[1,[199,0]], memo='x', suber='user1')


def test_setnotary(): vntoken.setnotary(
    notary='user1', to_add='true', suber=vntoken.contract)


def test_transfer(): vntoken.transfer(fromx='user1', to='pa.mart', assets=[[2002,[2002,0]]], memo='refuel:4', suber='user1')
