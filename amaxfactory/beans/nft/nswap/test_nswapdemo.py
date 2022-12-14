from time import sleep
from nft.nswap.nswap import NSWAP
nswap = NSWAP()
from kverso.vntoken.vntoken import VNTOKEN
vntoken = VNTOKEN()


from xchain.mtoken.mtoken import Mtoken

mtoken = Mtoken()



def test_createpool(): nswap.createpool(owner='ad', title='test one', asset_contract='amax.mtoken', blindbox_contract='verso.ntoken',
                                        price="10.000000 MUSDT", fee_receiver='fee', allow_to_buy_again='true', opended_at="2022-09-20T09:22:00", opened_days=10, suber='ad')


def test_dealtrace(): nswap.dealtrace(trace=1, suber='user1')


def test_editplantime(): nswap.editplantime(owner='user1', pool_id=1,
                                            opended_at=1, closed_at=1, suber='user1')
def test_enableplan(): nswap.enableplan(
    owner='user1', pool_id=1, enabled='true', suber='user1')


def test_endpool(): nswap.endpool(owner='user1', pool_id=1, suber='user1')
def test_init(): nswap.init(suber='user1')


def test_transfer1(): vntoken.transfer(fromx='ad', to='nftone.swap', assets=[[10,[100,0]]], memo='mint:2', suber='ad')

def test_transfer2(): vntoken.transfer(fromx='ad', to='nftone.swap', assets=[[10,[101,0]]], memo='mint_loop:2', suber='ad')


def test_transfer4(): 
    mtoken.transfer(fromx='ad', to = 'nftone.swap', quantity = "10.000000  MUSDT", memo = 'open:2', suber = 'ad')
    sleep(2)
    mtoken.transfer(fromx='ad', to = 'nftone.swap', quantity = "10.000000  MUSDT", memo = 'open:2', suber = 'ad')
    sleep(2)
    mtoken.transfer(fromx='ad', to = 'nftone.swap', quantity = "10.000000  MUSDT", memo = 'open:2', suber = 'ad')
