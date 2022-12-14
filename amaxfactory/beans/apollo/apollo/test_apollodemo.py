from apollo.apollo.apollo import Apollo as a
from nft.ntoken.ntoken import ntoken as n
from amax.cnydtoken.cnyd import CNYD
from xchain.mtoken.mtoken import Mtoken


mtoken = Mtoken()
cnyd = CNYD()
ntoken = n()
apollo = a()


def test_cancelorder(): apollo.cancelorder(maker='merchantx', token_id=200000, order_id=52, suber='merchantx')
def test_cancelbid():apollo.cancelbid(buyer='merchantx',bid_id=52,suber='merchantx').assetResponseFail()

def test_init(): apollo.init(symbol='6,MUSDT',contract='amax.mtoken',suber=apollo.contract)

def test_init2(): apollo.init2(suber=apollo.contract)

def test_takebuyorder(): apollo.takebuybid(issuer='user1', token_id=7, buy_order_id=3, suber='user1')


def test_takeselorder(): apollo.takeselorder(issuer='user1', token_id=1, sell_order_id=1, suber='user1')

def test_transfersell(): ntoken.transfer(fromx='user1', to=apollo.contract, assets=[[2,[200000,7]]], memo='3000000000', suber='user1')

def test_transferbuy(): cnyd.transfer(fromx='amax', to='mart', quantity="100.0000 CNYD", memo='t:7:100', suber='amax')

def test_transferbuy2(): mtoken.transfer(fromx='ad', to=apollo.contract, quantity="210.000000 MUSDT", memo='1:4:100', suber='ad')

def test_transferbuy3(): mtoken.transfer(fromx='ad', to="apollo.buy2", quantity="20.100000 MUSDT", memo='13:5:1', suber='ad')


# 交易
def test_transfer(): ntoken.transfer(fromx='ad', to=apollo.contract, assets=[[100,[1,0]]], memo='2000000', suber='ad')


def test_setorderfee():
    last_id = apollo.getLastRow(apollo.contract,'global')['last_sell_order_idx']
    apollo.setorderfee(order_id=last_id,start_at='2022-08-01T10:34:00.000',end_at='2022-08-29T08:00:00.000',fee='0.100000 MUSDT',suber=apollo.contract).assetResponsePass()
