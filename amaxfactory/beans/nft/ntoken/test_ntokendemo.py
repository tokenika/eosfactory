from nft.ntoken.ntoken import ntoken as n

ntoken = n()

# ntoken.contract = 'verso.ntoken'

#  创建
def test_create(): ntoken.create(issuer='user1', maximum_supply=100000000, symbol=[10086,100], token_uri='x1xxxxx', ipowner='user1',
                                 suber='user1')

# 铸造
def test_issue(): ntoken.issue(to='user1', quantity=[100000000,[10086,100]], memo='x', suber='user1')

# 公证
def test_notarize(): ntoken.notarize(notary='user1', token_id=565, suber='user1')

# 销毁
def test_retire(): ntoken.retire(quantity=[1,[565,0]], memo='x', suber='user1')

# 设置公证人
def test_setnotary(): ntoken.setnotary(notary='user1', add='true', suber=ntoken.contract)

# 交易
def test_transferx(): 
    ntoken.transfer(fromx='ad', to='user1', assets=[[4,[11004,0]]], memo='booth:6', suber='ad')
    ntoken.transfer(fromx='user1', to='rndnft.mart4', assets=[[4,[11004,0]]], memo='booth:11', suber='user1')


def test_transfer2(): ntoken.transfer(fromx='ad', to='user1', assets=[[1000,[10086,100]]], memo='lock:user1:1:0', suber='ad')



def test_transfer3(): ntoken.transfer(fromx='ad', to='user1', assets=[[100,[1,0]]], memo='refuel:1', suber='ad')

def test_setwhitelist():
    ntoken.setwhitelist(owner="amax.did2",to_add="true",suber=ntoken.contract)