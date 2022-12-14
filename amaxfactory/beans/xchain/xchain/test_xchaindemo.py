from xchain.xchain.xchain import xchain as x
from xchain.mtoken.mtoken import Mtoken

mtoken = Mtoken()
xchain = x()


def test_addchain(): xchain.addchain(account='ad', chain='xxx', base_chain='xxx', common_xin_account='',
                                     suber='user1')


def test_addchaincoin(): xchain.addchaincoin(chain='eth', coin='6,MUSDT', fee="4.000000 MUSDT",
                                             suber='ad')


def test_addcoin(): xchain.addcoin(account='user1', coin='8,AMAX', suber='user1')


def test_cancelxinord(): xchain.cancelxinord(
    order_id=1, cancel_reason='x', suber='user1')


def test_cancelxouord(): xchain.cancelxouord(
    account='user1', order_id=1, cancel_reason='x', suber='user1')


def test_checkxinord(): xchain.checkxinord(order_id=1, suber='user1')


def test_checkxouord(): xchain.checkxouord(order_id=1, suber='user1')


def test_delchain(): xchain.delchain(
    account='user1', chain='user1', suber='user1')


def test_delchaincoin(): xchain.delchaincoin(
    chain='eth', coin='8,METH', suber='ad')


def test_delcoin(): xchain.delcoin(account='ad', coin='6,MBNB', suber='ad')


def test_init(): xchain.init(admin='ad', maker='mk', checker='ck',
                             fee_collector='fee', suber=xchain.contract)


def test_mkxinorder(): xchain.mkxinorder(to='user1', chain_name='user1', coin_name='8,AMAX', txid='x', xin_from='x',
                                         xin_to='x', quantity="0.10000000 AMAX", suber='user1')


def test_reqxintoaddr(): xchain.reqxintoaddr(applicant='merchantxpro', applicant_account='merchantxpro', base_chain='tron',
                                             mulsign_wallet_id=0, suber='merchantxpro')


def test_setaddress(): xchain.setaddress(applicant='mk', base_chain='eth', mulsign_wallet_id=0, xin_to='xxxx',
                                         suber='mk')


def test_setxouconfm(): xchain.setxouconfm(order_id=1, suber='user1')


def test_setxousent(): xchain.setxousent(
    order_id=1, txid='x', xout_from='x', suber='user1')


def test_5(): mtoken.transfer(fromx='user1', to='xchainc',
                              quantity="2.000000 MUSDT", memo='addressxx:bsc:6,MUSDT:0:memoxx', suber='user1')
