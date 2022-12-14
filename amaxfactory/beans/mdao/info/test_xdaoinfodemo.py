from mdao.info.xdaoinfo import XDAOINFO
xdaoinfo = XDAOINFO()
from amax.amaxtoken.amax import AMAX
amax = AMAX()


def test_createDao():
    amax.transfer(fromx='ad', to=xdaoinfo.contract, quantity="1.00000000 AMAX", memo='amax.dao|amax DAO|amax.dao|https://amaxscan.io/amax.png', suber='ad')


def test_binddapps(): xdaoinfo.binddapps(
    owner='user1', code='xedkdcjm.dao', dapps="XXX", suber='user1')


def test_bindgov(): xdaoinfo.bindgov(
    owner='user1', code='user1', govid=1, suber='user1')


def test_bindtoken(): xdaoinfo.bindtoken(
    owner='ad', code='ereaagb1.dao', token='["6,MUSDT","amax.mtoken"]', suber='ad')


def test_bindwal(): xdaoinfo.bindwal(
    owner='user1', code='user1', walletid=1, suber='user1')


def test_createtoken(): xdaoinfo.createtoken(code='user1', owner='user1', taketranratio=1,
                                             takegasratio=1, fullname='x', maximum_supply="0.10000000 AMAX", suber='user1')
def test_delparam(): xdaoinfo.delparam(
    owner='user1', code='user1', tokens=1, suber='user1')


def test_recycledb(): xdaoinfo.recycledb(max_rows=1, suber='user1')


def test_setstrategy(): xdaoinfo.setstrategy(
    owner='user1', code='user1', stgtype='user1', stgid=1, suber='user1')


def test_updatedao(): xdaoinfo.updatedao(owner='ad', code='cpmzvlz1.dao', logo='https://amaxscan.io/amax.png',
                                         desc='amax.dao', links=[], symcode='', symcontract='', groupid='!weTQgZHoqBcnTgOelF:xdao.land', suber='ad')


def test_updatestatus(): xdaoinfo.updatestatus(
    code='amax.dao', isenable='false', suber='ad')


def test_updatecode(): xdaoinfo.updatecode(
    admin="ad",code='user1xx4.dao', newcode='user1xx5.dao', suber='ad')

def test_deldao(): xdaoinfo.deldao(admin="ad",code='user1xx5.dao', suber='ad')


def test_transferdao(): xdaoinfo.transferdao(
    owner="merchantx",code='user1xxx.dao', receiver='merchantx2', suber='merchantx')
