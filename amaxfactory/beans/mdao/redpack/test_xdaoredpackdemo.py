import imp
from mdao.redpack.xdaoredpack import XDAOREDPACK
xdaoredpack = XDAOREDPACK()
from amax.amaxtoken.amax import AMAX
amax = AMAX()
from amax.cnydtoken.cnyd import CNYD
cnyd = CNYD()
from xchain.mtoken.mtoken import Mtoken

mtoken = Mtoken()

def test_createRedpack():
    code = 'aaa15'
    amax.transfer(fromx='ad', to=xdaoredpack.contract, quantity="1.00000000 AMAX", memo=f'{code}:2:11:{code}', suber='ad')
    xdaoredpack.claim(claimer='fee',
                                    code=code, pwhash=code, suber='ad')

def test_transferCNYD(): 
    code = 'a1'
    cnyd.transfer(fromx='amax', to=xdaoredpack.contract, quantity="1.0000 CNYD", memo=f'{code}:1:0:{code}', suber='amax')
    xdaoredpack.claim(claimer='user1',
                                    code={code}, pwhash={code}, suber='ad')

def test_transfer(): 
    code = 'a5'
    mtoken.transfer(fromx='ad', to = xdaoredpack.contract, quantity = "1.000000 MUSDT", memo = f'{code}:1:11:{code}', suber = 'ad')
    xdaoredpack.claim(claimer='user1',code=code, pwhash=code, suber='ad')

def test_addfee(): 
    xdaoredpack.addfee(fee="0.00000000 AMAX", contract='amax.token',min=4,did_contract="did.ntoken2",did_id=1, suber=xdaoredpack.contract)
    xdaoredpack.addfee(fee="0.1000 CNYD", contract='cnyd.token',min=2,did_contract="did.ntoken2",did_id=1, suber=xdaoredpack.contract)
    xdaoredpack.addfee(fee="0.000000 MUSDT", contract='amax.mtoken',min=4,did_contract="did.ntoken2",did_id=1, suber=xdaoredpack.contract)
    xdaoredpack.addfee(fee="0.00000000 METH", contract='amax.mtoken',min=5,did_contract="did.ntoken2",did_id=1, suber=xdaoredpack.contract)
    xdaoredpack.addfee(fee="0.00000000 MBTC", contract='amax.mtoken',min=6,did_contract="did.ntoken2",did_id=1, suber=xdaoredpack.contract)


def test_cancel(): xdaoredpack.cancel(code='user1', suber='user1')
def test_claim(): xdaoredpack.claim(claimer='fee',
                                    code='12', pwhash='xxx', suber='ad')


def test_delfee(): 
    xdaoredpack.delfee(coin='6,MUSDTT', suber=xdaoredpack.contract)
    # xdaoredpack.delfee(coin='8,METH', suber=xdaoredpack.contract)
    # xdaoredpack.delfee(coin='8,MBTC', suber=xdaoredpack.contract)
    # xdaoredpack.delfee(coin='8,AMAX', suber=xdaoredpack.contract)

def test_delredpacks(): xdaoredpack.delredpacks(code='0', suber=xdaoredpack.contract)
def test_setconf(): xdaoredpack.init(admin='ad', hours=24,send_did='true' ,suber=xdaoredpack.contract)
