from nft.rndnftmart.rndnftmart import RNDNFTMART
rndnftmart = RNDNFTMART()
from xchain.mtoken.mtoken import Mtoken

mtoken = Mtoken()

from nft.ntoken.ntoken import ntoken as n

ntoken = n()

from did.didntoken.didntoken import DIDNTOKEN
didntoken = DIDNTOKEN()



def test_transfer4(): 
    id = 20
    mtoken.transfer(fromx='merchantx', to = rndnftmart.contract, quantity = "0.010000  MUSDT", memo = f'booth:{20}', suber = 'merchantx')


def test_transfer(): 
    didntoken.transfer(fromx='ad',to=rndnftmart.contract,assets=[[1,[1,0]]],memo='booth:20',suber='ad') 


def test_closebooth(): 
    id = 18
    rndnftmart.createbooth(owner='user1', title='盲盒测试3', fund_contract='amax.mtoken',split_id=5, nft_contract='amax.ntoken',
                                             price="0.010000 MUSDT",  opened_at="2022-10-08T03:00:00", opened_days=30, suber=rndnftmart.contract)
    # ntoken.transfer(fromx='ad', to='user1', assets=[[4,[11004,0]]], memo='booth:6', suber='ad')
    # ntoken.transfer(fromx='user1', to='rndnft.mart4', assets=[[4,[11004,0]]], memo=f'booth:{id}', suber='user1')
    # ntoken.transfer(fromx='ad', to='user1', assets=[[4,[11004,0]]], memo='booth:6', suber='ad')
    # ntoken.transfer(fromx='user1', to='rndnft.mart4', assets=[[4,[11004,0]]], memo=f'booth:{id}', suber='user1')
    # ntoken.transfer(fromx='ad', to='user1', assets=[[2,[11001,0]]], memo='booth:6', suber='ad')
    # ntoken.transfer(fromx='user1', to='rndnft.mart4', assets=[[2,[11001,0]]], memo=f'booth:{id}', suber='user1')
    # ntoken.transfer(fromx='ad', to='user1', assets=[[2,[11001,0]]], memo='booth:6', suber='ad')
    # ntoken.transfer(fromx='user1', to='rndnft.mart4', assets=[[2,[11001,0]]], memo=f'booth:{id}', suber='user1')
    # rndnftmart.enablebooth(owner="user1", booth_id=id, enabled='true', suber="user1")
    rndnftmart.closebooth(owner='user1', booth_id=id, suber='ad')


def test_ontransfernft():
    id = 20
    ntoken.transfer(fromx='ad', to='user1', assets=[[4,[11001,0]]], memo='booth:6', suber='ad')
    ntoken.transfer(fromx='user1', to='rndnft.mart4', assets=[[4,[11001,0]]], memo=f'booth:20', suber='user1')


def test_createbooth(): rndnftmart.createbooth(owner='user1', title='盲盒测试3', fund_contract='amax.mtoken',split_id=5, nft_contract='amax.ntoken',
                                             price="0.010000 MUSDT",  opened_at="2022-10-08T03:00:00", opened_days=30, suber=rndnftmart.contract)


def test_dealtrace(): rndnftmart.dealtrace(trace=1, suber='user1')


def test_enablebooth(): 
    id = 20
    # rndnftmart.createbooth(owner='user1', title='盲盒测试3', fund_contract='amax.mtoken',split_id=5, nft_contract='amax.ntoken',
    #                                          price="0.010000 MUSDT",  opened_at="2022-10-08T03:00:00", opened_days=30, suber=rndnftmart.contract)
    rndnftmart.enablebooth(owner="user1", booth_id=id, enabled='3', suber="ad")
    # ntoken.transfer(fromx='ad', to='user1', assets=[[4,[11004,0]]], memo='booth:6', suber='ad')
    # ntoken.transfer(fromx='user1', to='rndnft.mart4', assets=[[4,[11004,0]]], memo=f'booth:{id}', suber='user1')

def test_init(): rndnftmart.init(
    admin='ad', fund_distributor='amax.split2', suber=rndnftmart.contract)


def test_setboothtime(): rndnftmart.setboothtime(
    owner='user1', booth_id=20, opened_at="2022-10-08T03:00:00", closed_at="2022-10-30T03:00:00", suber=rndnftmart.contract)
