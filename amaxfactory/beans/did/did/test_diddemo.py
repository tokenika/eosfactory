from did.did.did import DID
did = DID()
from amax.amaxtoken.amax import AMAX
amax = AMAX()

def test_addvendor(): did.addvendor(vendor_name='alibaba', vendor_account='alibaba', kyc_level=1, 
                                    user_reward_quant="10.0000 APL", user_charge_amount="0.02000000 AMAX", nft_id=[1,0], suber='ad')


def test_chgvendor(): 
    # did.chgvendor(vendor_id=2, status='running', suber=did.contract)
    did.chgvendor(vendor_id=2, status='running', suber='ad')


def test_finishdid(): did.finishdid(order_id=3,msg='xx', suber='ad')

def test_faildid(): did.faildid(order_id=3,reason='reason', suber='ad')


def test_init(): did.init(admin='ad', nft_contract='did.ntoken',
                          fee_colletor='fee',lease_id=2, suber=did.contract)

def test_transfer(): amax.transfer(fromx='merchantx', to = 'amax.did', quantity = "0.02000000 AMAX", memo = 'alibaba:1:md5x1xx1', suber = 'merchantx')
