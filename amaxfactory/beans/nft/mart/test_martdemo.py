from nft.mart.mart import mart as m
from nft.ntoken.ntoken import ntoken as n
from amax.cnydtoken.cnyd import CNYD
from xchain.mtoken.mtoken import Mtoken


mtoken = Mtoken()
cnyd = CNYD()
ntoken = n()
mart = m()


def test_cancelorder(): mart.cancelorder(maker='merchantx', token_id=200000, order_id=52, suber='merchantx')
def test_cancelbid():mart.cancelbid(buyer='merchantx',bid_id=52,suber='merchantx').assetResponseFail()

def test_init(): mart.init(symbol='6,MUSDT',contract='amax.mtoken',suber=mart.contract)

def test_init2(): mart.init2(suber=mart.contract)

def test_takebuyorder(): mart.takebuybid(issuer='merchantx', token_id=123, buy_order_id=3, suber='merchantx')


def test_takeselorder(): mart.takeselorder(issuer='user1', token_id=1, sell_order_id=1, suber='user1')

def test_transfersell(): ntoken.transfer(fromx='user1', to=mart.contract, assets=[[2,[200000,7]]], memo='3000000000', suber='user1')

def test_transferbuy(): cnyd.transfer(fromx='amax', to='mart', quantity="100.0000 CNYD", memo='t:7:100', suber='amax')

def test_transferbuy2(): mtoken.transfer(fromx='user1', to='martz', quantity="1.000000 MUSDT", memo='200000:1:1000000', suber='user1')
