from nft.rndnftmart.rndnftmart import RNDNFTMART
rndnftmart = RNDNFTMART()
from xchain.mtoken.mtoken import Mtoken

mtoken = Mtoken()

def test_transfer4(): mtoken.transfer(fromx='merchantx', to = rndnftmart.contract, quantity = "0.010000  MUSDT", memo = 'booth:11', suber = 'merchantx')

def test_closebooth(): rndnftmart.closebooth(
    owner='user1', booth_id=7, suber='ad')


def test_createbooth(): rndnftmart.createbooth(owner='user1', title='盲盒测试3', fund_contract='amax.mtoken',split_id=5, nft_contract='amax.ntoken',
                                             price="0.010000 MUSDT",  opened_at="2022-10-08T03:00:00", opened_days=30, suber=rndnftmart.contract)


def test_dealtrace(): rndnftmart.dealtrace(trace=1, suber='user1')


def test_enablebooth(): rndnftmart.enablebooth(
    owner="user1", booth_id=20, enabled='true', suber="user1")


def test_init(): rndnftmart.init(
    admin='ad', fund_distributor='amax.split2', suber=rndnftmart.contract)


def test_setboothtime(): rndnftmart.setboothtime(
    owner='user1', booth_id=4, opened_at="2022-10-08T03:00:00", closed_at="2022-10-09T03:00:00", suber=rndnftmart.contract)
