import random
from base import amcli
from otc.otcbook.otcbook import otcbookv as o
book = o()
from xchain.mtoken.mtoken import Mtoken

mtoken = Mtoken()

class Testcanceldeal:
    # status =1 user 可以关闭
    def test_1(self):
        merchantx = book.getLastRowByIndex(book.contract,'merchants','name','merchantx','merchantx',1)['assets'][0]['value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        book.openorder(owner='merchantx', order_side='buy', pay_methods=["wechat"], va_quantity="200.000000 USDTERC",
                       va_price="6.0000 CNY", va_min_take_quantity="1.000000 USDTERC",
                       va_max_take_quantity="200.000000 USDTERC", memo='x', suber='merchantx').assetResponsePass()
        oid = book.getLastBuyorder()['id']

        book.opendeal(taker='user1', order_side='buy', order_id=oid, deal_quantity="200.000000 USDTERC",
                      order_sn=random.randint(10000, 500000), session_msg='x', suber='abcd12341234').assetResponsePass()
        did = book.getLastDeal()['id']

        book.canceldeal(account='abcd12341234', account_type=3, deal_id=did,
                                           is_taker_black='false', suber='abcd12341234').assetResponsePass()
        book.closeorder(owner='merchantx', order_side='buy', order_id=oid, suber='merchantx').assetResponsePass()
        merchantx = book.getLastRowByIndex(book.contract,'merchants','name','merchantx','merchantx',1)['assets'][0]['value']
        balance2 = merchantx['balance']
        frozen2 = merchantx['frozen']
        assert balance==balance2
        assert frozen==frozen2

        # status=1 merchant cancel
    def test_2(self):
        merchantx = \
        book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0]['value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        book.openorder(owner='merchantx', order_side='buy', pay_methods=["wechat"], va_quantity="10.000000 USDTARC",
                       va_price="6.0000 CNY", va_min_take_quantity="1.000000 USDTARC",
                       va_max_take_quantity="10.000000 USDTARC", memo='x', suber='merchantx').assetResponsePass()
        oid = book.getLastBuyorder()['id']

        mtoken.transfer(fromx='user1', to = 'meta.book', quantity = "10.000000 MUSDT", memo = f'opendeal:{oid}:{random.randint(10000, 500000)}:3', suber = 'user1').assetResponsePass()

        # book.opendeal(taker='abcd12341234', order_side='buy', order_id=oid, deal_quantity="2.000000 USDTERC",
        #               order_sn=random.randint(10000, 500000), session_msg='x', suber='abcd12341234').assetResponsePass()
        did = book.getLastDeal()['id']
        book.canceldeal(account='merchantx', account_type=2, deal_id=did,
                        is_taker_black='false', suber='merchantx').assetResponsePass()
        # book.closeorder(owner='merchantx', order_side='buy', order_id=oid, suber='merchantx').assetResponsePass()
        # merchantx = \
        # book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0]['value']
        # balance2 = merchantx['balance']
        # frozen2 = merchantx['frozen']
        # assert balance == balance2
        # assert frozen == frozen2

    # 测试拉黑
    def test_3(self):
        merchantx = \
        book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantxpro', 'merchantxpro', 1)['assets'][0]['value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        book.openorder(owner='merchantxpro', order_side='buy', pay_methods=["wechat"], va_quantity="2.000000 USDTERC",
                       va_price="6.0000 CNY", va_min_take_quantity="1.000000 USDTERC",
                       va_max_take_quantity="2.000000 USDTERC", memo='x', suber='merchantxpro').assetResponsePass()
        oid = book.getLastBuyorder()['id']

        name = amcli.newaccount("user1")

        book.opendeal(taker=name, order_side='buy', order_id=oid, deal_quantity="2.000000 USDTERC",
                      order_sn=random.randint(10000, 500000), session_msg='x', suber=name).assetResponsePass()
        did = book.getLastDeal()['id']
        book.canceldeal(account='merchantxpro', account_type=2, deal_id=did,
                        is_taker_black='true', suber='merchantxpro').assetResponsePass()
        book.closeorder(owner='merchantxpro', order_side='buy', order_id=oid, suber='merchantxpro').assetResponsePass()
        merchantx = \
        book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantxpro', 'merchantxpro', 1)['assets'][0]['value']
        balance2 = merchantx['balance']
        frozen2 = merchantx['frozen']
        assert balance == balance2
        assert frozen == frozen2


