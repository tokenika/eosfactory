from redpackcase.redpack import redpack as r
from amax.cnydtoken.cnyd import CNYD
from xchain.mtoken.mtoken import Mtoken

mtoken = Mtoken()
cnyd = CNYD()

redpack = r()

def test_setconf(): redpack.setconf(admin='ad', hours=24, suber=redpack.contract)

def test_addfee(): redpack.addfee(fee="0.00000000 AMAX", contract='amax.token',min=4,did_contract="did.ntoken2",did_id=1, suber=redpack.contract)
def test_addfee2(): redpack.addfee(fee="0.1000 CNYD", contract='cnyd.token',min=2,did_contract="did.ntoken2",did_id=1, suber=redpack.contract)
def test_addfee3(): redpack.addfee(fee="0.000000 MUSDT", contract='amax.mtoken',min=4,did_contract="did.ntoken2",did_id=1, suber=redpack.contract)
def test_addfee4(): redpack.addfee(fee="0.00000000 METH", contract='amax.mtoken',min=5,did_contract="did.ntoken2",did_id=1, suber=redpack.contract)
def test_addfee5(): redpack.addfee(fee="0.00000000 MBTC", contract='amax.mtoken',min=6,did_contract="did.ntoken2",did_id=1, suber=redpack.contract)

def test_delfee(): redpack.delfee(coin='4,CNYD', suber=redpack.contract)

def test_create(): cnyd.transfer(fromx='user1', to=redpack.contract, quantity="10.0000 CNYD", memo='xxx:1:0', suber='user1')

def test_create2(): mtoken.transfer(fromx='merchantx', to = redpack.contract, quantity = "10.000000  MUSDT", memo = 'xxx:2:11:12', suber = 'merchantx')


def test_cancel(): redpack.cancel( pack_id=99, suber='ad')


def test_claim1(): redpack.claim(claimer='merchantx', pack_id=4, pwhash='xx', suber='ad')
def test_claim2(): redpack.claim(claimer='merchantx2', pack_id=4, pwhash='xxx',name='mx2', suber='ad')
def test_claim3(): redpack.claim(claimer='weiweitest11', pack_id=52, pwhash='xxx',name='weiwei', suber='ad')






