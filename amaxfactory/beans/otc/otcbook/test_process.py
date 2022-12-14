import random

from otc.otcbook.otcbook import otcbookv as o
from otc.otcsettle.otcsettle import Otcsettle

otcsettle = Otcsettle()

book = o()


class TestOTCv2:
    def test_1(self):
        oid = book.getLastBuyorder()['id'] + 1
        book.openorder(owner='merchantx', order_side='buy', pay_methods=["wechat"], va_quantity="100.0000 CNYDARC",
                       va_price="1.0000 CNY", va_min_take_quantity="100.0000 CNYDARC",
                       va_max_take_quantity="100.0000 CNYDARC", memo='x', suber='merchantx').assetResponsePass()
        assert oid == book.getLastBuyorder()['id']
        print(oid)

        did = book.getLastDeal()['id'] + 1
        book.opendeal(taker='user1', order_side='buy', order_id=oid, deal_quantity="100.0000 CNYDARC",
                      order_sn=random.randint(10000, 500000), session_msg='x', suber='user1').assetResponsePass()
        assert did == book.getLastDeal()['id']

        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=2, session_msg='x',
                         suber='merchantx').assetResponsePass()
        book.processdeal(account='user1', account_type=3, deal_id=did, action=3, session_msg='x',
                         suber='user1').assetResponsePass()
        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=4, session_msg='x',
                         suber='merchantx').assetResponsePass()

        # creator_sttle = otcsettle.getSettle('amax')
        # print(creator_sttle)
        # creator_sum_child_deal = creator_sttle['sum_child_deal']
        # m_settle = otcsettle.getSettle('merchantx')
        # merchant_sum_deal = m_settle['sum_deal']
        # merchant_sum_fee = m_settle['sum_fee']
        # u_settle = otcsettle.getSettle('user1')
        # user_sum_deal = u_settle['sum_deal']
        # user_sum_fee = u_settle['sum_fee']

        # id = otcsettle.getLastReward()['id'] + 1
        book.closedeal(account='user1', account_type=3, deal_id=did, session_msg='x', suber='user1').assetResponsePass()
        #
        # creator_sum_child_deal2 = otcsettle.getSettle('amax')['sum_child_deal']
        # m_settle2 = otcsettle.getSettle('merchantx')
        # merchant_sum_deal2 = m_settle2['sum_deal']
        # merchant_sum_fee2 = m_settle2['sum_fee']
        # u_settle2 = otcsettle.getSettle('user1')
        # user_sum_deal2 = u_settle2['sum_deal']
        # user_sum_fee2 = u_settle2['sum_fee']
        #
        # assert id == otcsettle.getLastReward()['id']
        # assert merchant_sum_deal + 1000000 == merchant_sum_deal2
        # assert merchant_sum_fee + 5000 == merchant_sum_fee2
        # assert user_sum_deal + 1000000 == user_sum_deal2
        # assert user_sum_fee + 5000 == user_sum_fee2
        # assert creator_sum_child_deal + 1000000 == creator_sum_child_deal2

        book.closeorder(owner='merchantx', order_side='buy', order_id=oid, suber='merchantx').assetResponsePass()


    def test_2(self):
        oid = book.getLastBuyorder()['id'] + 1
        book.openorder(owner='merchantx', order_side='buy', pay_methods=["wechat"], va_quantity="200.000000 USDTERC",
                       va_price="6.0000 CNY", va_min_take_quantity="1.000000 USDTERC",
                       va_max_take_quantity="200.000000 USDTERC", memo='x', suber='merchantx').assetResponsePass()
        # book.openorder(owner='merchantx', order_side='buy', pay_methods=["wechat"], va_quantity="100.0000 CNYDARC",
        #                va_price="1.0000 CNY", va_min_take_quantity="100.0000 CNYDARC",
        #                va_max_take_quantity="100.0000 CNYDARC", memo='x', suber='merchantx').assetResponsePass()
        assert oid == book.getLastBuyorder()['id']
        print(oid)

        did = book.getLastDeal()['id'] + 1

        # book.opendeal(taker='user1', order_side='buy', order_id=oid, deal_quantity="100.0000 CNYDARC",
        #               order_sn=random.randint(10000, 500000), session_msg='x', suber='user1').assetResponsePass()
        book.opendeal(taker='abcd12341234', order_side='buy', order_id=oid, deal_quantity="200.000000 USDTERC",
                      order_sn=random.randint(10000, 500000), session_msg='x', suber='abcd12341234').assetResponsePass()

        assert did == book.getLastDeal()['id']

        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=2, session_msg='x',
                         suber='merchantx').assetResponsePass()
        book.processdeal(account='abcd12341234', account_type=3, deal_id=did, action=3, session_msg='x',
                         suber='abcd12341234').assetResponsePass()
        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=4, session_msg='x',
                         suber='merchantx').assetResponsePass()
        book.closedeal(account='abcd12341234', account_type=3, deal_id=did, session_msg='x', suber='abcd12341234').assetResponsePass()
        book.closeorder(owner='merchantx', order_side='buy', order_id=oid, suber='merchantx').assetResponsePass()


    def test_3(self):
        oid=0
        did=0
        # book.processdeal(account='merchantx', account_type=2, deal_id=did, action=2, session_msg='x',
        #                  suber='merchantx').assetResponsePass()
        # book.processdeal(account='user1', account_type=3, deal_id=did, action=3, session_msg='x',
        #                  suber='user1').assetResponsePass()
        # book.processdeal(account='merchantx', account_type=2, deal_id=did, action=4, session_msg='x',
        #                  suber='merchantx').assetResponsePass()
        book.closedeal(account='user1', account_type=3, deal_id=did, session_msg='x',
                       suber='user1').assetResponsePass()
        book.closeorder(owner='merchantx', order_side='buy', order_id=oid, suber='merchantx').assetResponsePass()