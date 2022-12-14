import random
import time

from otc.otcbook.otcbook import otcbookv as o
from xchain.mtoken.mtoken import Mtoken
from otc.otcconf.otcconfv import otcconfv as c
from amax.arctoken.arc import arc as a
arc = a()

otcconfv = c()
mtoken = Mtoken()

book = o()


class Testclosedeal:
    # 用户关闭
    def test_1(self):
        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        userBalance = mtoken.getLastRow("user1", 'accounts')['balance']

        book.openorder(owner='merchantx', order_side='buy', pay_methods=["wechat"], va_quantity="10.000000 USDTERC",
                       va_price="6.0000 CNY", va_min_take_quantity="1.000000 USDTERC",
                       va_max_take_quantity="10.000000 USDTERC", memo='x', suber='merchantx').assetResponsePass()
        oid = book.getLastBuyorder()['id']

        merchantx1 = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance1 = merchantx1['balance']
        frozen1 = merchantx1['frozen']
        assert int(balance1) == int(balance) - 10000000
        assert int(frozen1) == int(frozen) + 10000000


        book.opendeal(taker='user1', order_side='buy', order_id=oid, deal_quantity="10.000000 USDTERC",
                      order_sn=random.randint(10000, 500000), session_msg='x', suber='user1').assetResponsePass()
        did = book.getLastDeal()['id']

        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=2, session_msg='x',
                         suber='merchantx').assetResponsePass()
        book.processdeal(account='user1', account_type=3, deal_id=did, action=3, session_msg='x',
                         suber='user1').assetResponsePass()
        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=4, session_msg='x',
                         suber='merchantx').assetResponsePass()
        
        time.sleep(2)
        book.closedeal(account='user1', account_type=3, deal_id=did, session_msg='x',
                       suber='user1').assetResponsePass()
        # book.closeorder(owner='merchantx', order_side='buy',
        #                 order_id=oid, suber='merchantx').assetResponsePass()

        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance2 = merchantx['balance']
        frozen2 = merchantx['frozen']
        assert int(balance2) == int(balance)
        assert frozen == frozen2

        userBalance2 = mtoken.getLastRow("user1", 'accounts')['balance']
        assert userBalance2 == userBalance

    # 管理员关闭
    def test_2(self):
        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        userBalance = mtoken.getLastRow("user1", 'accounts')['balance']

        book.openorder(owner='merchantx', order_side='buy', pay_methods=["wechat"], va_quantity="10.000000 USDTERC",
                       va_price="6.0000 CNY", va_min_take_quantity="1.000000 USDTERC",
                       va_max_take_quantity="10.000000 USDTERC", memo='x', suber='merchantx').assetResponsePass()
        oid = book.getLastBuyorder()['id']

        book.opendeal(taker='user1', order_side='buy', order_id=oid, deal_quantity="10.000000 USDTERC",
                      order_sn=random.randint(10000, 500000), session_msg='x', suber='user1').assetResponsePass()
        did = book.getLastDeal()['id']

        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=2, session_msg='x',
                         suber='merchantx').assetResponsePass()
        book.processdeal(account='user1', account_type=3, deal_id=did, action=3, session_msg='x',
                         suber='user1').assetResponsePass()
        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=4, session_msg='x',
                         suber='merchantx').assetResponsePass()
        book.closedeal(account='ad', account_type=1, deal_id=did, session_msg='x',
                       suber='ad').assetResponsePass()
        book.closeorder(owner='merchantx', order_side='buy',
                        order_id=oid, suber='merchantx').assetResponsePass()

        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance2 = merchantx['balance']
        frozen2 = merchantx['frozen']
        assert int(balance2) == int(balance) - 50000
        assert frozen == frozen2

        userBalance2 = mtoken.getLastRow("user1", 'accounts')['balance']
        assert userBalance2 == userBalance

    # 仲裁关闭

    def test_3(self):

        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        userBalance = mtoken.getLastRow("user1", 'accounts')['balance']

        book.openorder(owner='merchantx', order_side='buy', pay_methods=["wechat"], va_quantity="10.000000 USDTERC",
                       va_price="6.0000 CNY", va_min_take_quantity="1.000000 USDTERC",
                       va_max_take_quantity="10.000000 USDTERC", memo='x', suber='merchantx').assetResponsePass()
        oid = book.getLastBuyorder()['id']

        book.opendeal(taker='user1', order_side='buy', order_id=oid, deal_quantity="10.000000 USDTERC",
                      order_sn=random.randint(10000, 500000), session_msg='x', suber='user1').assetResponsePass()
        did = book.getLastDeal()['id']

        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=2, session_msg='x',
                         suber='merchantx').assetResponsePass()
        book.processdeal(account='user1', account_type=3, deal_id=did, action=3, session_msg='x',
                         suber='user1').assetResponsePass()
        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=4, session_msg='x',
                         suber='merchantx').assetResponsePass()
        book.startarbit(account='user1', account_type=3, deal_id=did, arbiter='casharbitoo1',
                        suber='user1')
        book.closedeal(account='casharbitoo1', account_type=4, deal_id=did, session_msg='x',
                       suber='casharbitoo1').assetResponsePass()
        book.closeorder(owner='merchantx', order_side='buy',
                        order_id=oid, suber='merchantx').assetResponsePass()

        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance2 = merchantx['balance']
        frozen2 = merchantx['frozen']
        assert int(balance2) == int(balance) - 50000
        assert frozen == frozen2

        userBalance2 = mtoken.getLastRow("user1", 'accounts')['balance']
        assert userBalance2 == userBalance

    # 商户关闭

    def test_4(self):
        otcconfv.settimeout(accepted_timeout=0, payed_timeout=0,
                            suber=otcconfv.contract).assetResponsePass()

        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        userBalance = mtoken.getLastRow("user1", 'accounts')['balance']

        book.openorder(owner='merchantx', order_side='buy', pay_methods=["wechat"], va_quantity="10.000000 USDTERC",
                       va_price="6.0000 CNY", va_min_take_quantity="1.000000 USDTERC",
                       va_max_take_quantity="10.000000 USDTERC", memo='x', suber='merchantx').assetResponsePass()
        oid = book.getLastBuyorder()['id']

        book.opendeal(taker='user1', order_side='buy', order_id=oid, deal_quantity="10.000000 USDTERC",
                      order_sn=random.randint(10000, 500000), session_msg='x', suber='user1').assetResponsePass()
        did = book.getLastDeal()['id']

        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=2, session_msg='x',
                         suber='merchantx').assetResponsePass()
        book.processdeal(account='user1', account_type=3, deal_id=did, action=3, session_msg='x',
                         suber='user1').assetResponsePass()
        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=4, session_msg='x',
                         suber='merchantx').assetResponsePass()

        time.sleep(2)
        book.closedeal(account='merchantx', account_type=2, deal_id=did, session_msg='x',
                       suber='merchantx').assetResponsePass()
        book.closeorder(owner='merchantx', order_side='buy',
                        order_id=oid, suber='merchantx').assetResponsePass()

        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance2 = merchantx['balance']
        frozen2 = merchantx['frozen']
        assert int(balance2) == int(balance) - 50000
        assert frozen == frozen2

        userBalance2 = mtoken.getLastRow("user1", 'accounts')['balance']
        assert userBalance2 == userBalance


    #  amax 订单测试
    def test_amax(self):
        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        userBalance = mtoken.getLastRow("user1", 'accounts')['balance']

        book.openorder(owner='merchantx', order_side='buy', pay_methods=["wechat"], va_quantity="10.00000000 AMAXARC",
                       va_price="6.0000 CNY", va_min_take_quantity="1.00000000 AMAXARC",
                       va_max_take_quantity="10.00000000 AMAXARC", memo='x', suber='merchantx').assetResponsePass()
        oid = book.getLastBuyorder()['id']

        merchantx1 = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance1 = merchantx1['balance']
        frozen1 = merchantx1['frozen']
        assert int(balance1) == int(balance) - 1000000000
        assert int(frozen1) == int(frozen) + 1000000000


        book.opendeal(taker='user1', order_side='buy', order_id=oid, deal_quantity="10.00000000 AMAXARC",
                      order_sn=random.randint(10000, 500000), session_msg='x', suber='user1').assetResponsePass()
        did = book.getLastDeal()['id']

        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=2, session_msg='x',
                         suber='merchantx').assetResponsePass()
        book.processdeal(account='user1', account_type=3, deal_id=did, action=3, session_msg='x',
                         suber='user1').assetResponsePass()
        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=4, session_msg='x',
                         suber='merchantx').assetResponsePass()
        book.closedeal(account='user1', account_type=3, deal_id=did, session_msg='x',
                       suber='user1').assetResponsePass()
        book.closeorder(owner='merchantx', order_side='buy',
                        order_id=oid, suber='merchantx').assetResponsePass()

        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance2 = merchantx['balance']
        frozen2 = merchantx['frozen']
        assert int(balance2) == int(balance) - 8000000
        assert frozen == frozen2

        userBalance2 = mtoken.getLastRow("user1", 'accounts')['balance']
        assert userBalance2 == userBalance



    def test_5(self):
        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        userBalance = mtoken.getLastRow("user1", 'accounts')['balance']

        book.openorder(owner='merchantx', order_side='buy', pay_methods=["wechat", "alipay"], va_quantity="40.000000 USDTERC",
                       va_price="5.0000 CNY", va_min_take_quantity="10.000000 USDTERC",
                       va_max_take_quantity="40.000000 USDTERC", memo='x', suber='merchantx').assetResponsePass()
        # oid = book.getLastBuyorder()['id']
        #
        # book.opendeal(taker='user1', order_side='buy', order_id=oid, deal_quantity="10.000000 USDTERC",
        #               order_sn=random.randint(10000, 500000), session_msg='x', suber='user1').assetResponsePass()
        # did = book.getLastDeal()['id']
        #
        # book.processdeal(account='merchantx', account_type=2, deal_id=did, action=2, session_msg='x',
        #                  suber='merchantx').assetResponsePass()
        # book.processdeal(account='user1', account_type=3, deal_id=did, action=3, session_msg='x',
        #                  suber='user1').assetResponsePass()
        # book.processdeal(account='merchantx', account_type=2, deal_id=did, action=4, session_msg='x',
        #                  suber='merchantx').assetResponsePass()
        # book.closedeal(account='user1', account_type=3, deal_id=did, session_msg='x',
        #                suber='user1').assetResponsePass()
        # book.closeorder(owner='merchantx', order_side='buy', order_id=oid, suber='merchantx').assetResponsePass()
        #
        # merchantx = \
        #     book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
        #         'value']
        # balance2 = merchantx['balance']
        # frozen2 = merchantx['frozen']
        # assert int(balance2) == int(balance) - 50000
        # assert frozen == frozen2
        #
        # userBalance2 = mtoken.getLastRow("user1", 'accounts')['balance']
        # assert userBalance2 == userBalance



    # MUSDT 合约otc
    def test_buymu(self):
        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][1][
                'value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        userBalance = mtoken.getLastRow("user1", 'accounts')['balance']
        metrantBalance = mtoken.getLastRow("merchantx", 'accounts')['balance']


        book.openorder(owner='merchantx', order_side='buy', pay_methods=["wechat"], va_quantity="10.000000 USDTARC",
                       va_price="6.0000 CNY", va_min_take_quantity="1.000000 USDTARC",
                       va_max_take_quantity="10.000000 USDTARC", memo='x', suber='merchantx').assetResponsePass()
        oid = book.getLastBuyorder()['id']

        merchantx1 = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][1][
                'value']
        balance1 = merchantx1['balance']
        frozen1 = merchantx1['frozen']
        assert int(balance1) == int(balance) - 10000000
        assert int(frozen1) == int(frozen) + 10000000


        book.opendeal(taker='user1', order_side='buy', order_id=oid, deal_quantity="10.000000 USDTARC",
                      order_sn=random.randint(10000, 500000), session_msg='x', suber='user1').assetResponsePass()
        did = book.getLastDeal()['id']

        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=2, session_msg='x',
                         suber='merchantx').assetResponsePass()
        mtoken.transfer(fromx='user1', to = 'meta.book', quantity = "10.000000 MUSDT", memo = f'process:3:{did}:3', suber = 'user1').assetResponsePass()
        # buy 1 用户下单  2 商户接单 3 用户转币 4 商户转款 5 用户收款
        # 1 from 是用户 to 是合约 ， 2 quantity 是 deal_quantity 3  memo = process:3:{deal_id}:3

        # book.processdeal(account='user1', account_type=3, deal_id=did, action=3, session_msg='x',
        #                  suber='user1').assetResponsePass()
        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=4, session_msg='x',
                         suber='merchantx').assetResponsePass()


        time.sleep(2)
        book.closedeal(account='user1', account_type=3, deal_id=did, session_msg='x',
                       suber='user1').assetResponsePass()
        book.closeorder(owner='merchantx', order_side='buy',
                        order_id=oid, suber='merchantx').assetResponsePass()

        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][1][
                'value']
        balance2 = merchantx['balance']
        frozen2 = merchantx['frozen']
        assert int(balance2) == int(balance) - 40000
        assert frozen == frozen2

        userBalance2 = mtoken.getLastRow("user1", 'accounts')['balance']
        metrantBalance2 = mtoken.getLastRow("merchantx", 'accounts')['balance']

        assert int(str(userBalance2).split(".")[0]) == int(str(userBalance).split(".")[0]) -10
        assert int(str(metrantBalance2).split(".")[0]) == int(str(metrantBalance).split(".")[0]) +10


    def test_sellmu(self):
        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        userBalance = mtoken.getLastRow("user1", 'accounts')['balance']
        metrantBalance = mtoken.getLastRow("merchantx", 'accounts')['balance']

        book.openorder(owner='merchantx', order_side='sell', pay_methods=["wechat"], va_quantity="10.000000 USDTARC",
                       va_price="6.0000 CNY", va_min_take_quantity="1.000000 USDTARC",
                       va_max_take_quantity="10.000000 USDTARC", memo='x', suber='merchantx').assetResponsePass()
        oid = book.getLastSellorder()['id']

        merchantx1 = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance1 = merchantx1['balance']
        frozen1 = merchantx1['frozen']
        assert int(balance1) == int(balance) - 10000000
        assert int(frozen1) == int(frozen) + 10000000


        book.opendeal(taker='user1', order_side='sell', order_id=oid, deal_quantity="10.000000 USDTARC",
                      order_sn=random.randint(10000, 500000), session_msg='x', suber='user1').assetResponsePass()
        did = book.getLastDeal()['id']

        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=2, session_msg='x',
                         suber='merchantx').assetResponsePass()
        book.processdeal(account='user1', account_type=3, deal_id=did, action=3, session_msg='x',
                         suber='user1').assetResponsePass()
        # book.processdeal(account='merchantx', account_type=2, deal_id=did, action=4, session_msg='x',
                        #  suber='merchantx').assetResponsePass()
        
        time.sleep(2)

        mtoken.transfer(fromx='merchantx', to = 'meta.book', quantity = "10.000000 MUSDT", memo = f'process:2:{did}:4', suber = 'merchantx').assetResponsePass()

        time.sleep(2)
        book.closedeal(account='user1', account_type=3, deal_id=did, session_msg='x',
                       suber='user1').assetResponsePass()
        # book.closeorder(owner='merchantx', order_side='sell',
        #                 order_id=oid, suber='merchantx').assetResponsePass()

        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance2 = merchantx['balance']
        frozen2 = merchantx['frozen']
        assert int(balance2) == int(balance) 
        assert frozen == frozen2

        userBalance2 = mtoken.getLastRow("user1", 'accounts')['balance']
        metrantBalance2 = mtoken.getLastRow("merchantx", 'accounts')['balance']
        assert int(str(userBalance2).split(".")[0]) == int(str(userBalance).split(".")[0]) +10
        assert int(str(metrantBalance2).split(".")[0]) == int(str(metrantBalance).split(".")[0]) -10


    def test_buymu_errorcase(self):
        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][1][
                'value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        book.openorder(owner='merchantx', order_side='buy', pay_methods=["wechat"], va_quantity="10.000000 USDTARC",
                       va_price="6.0000 CNY", va_min_take_quantity="1.000000 USDTARC",
                       va_max_take_quantity="10.000000 USDTARC", memo='x', suber='merchantx').assetResponsePass()
        oid = book.getLastBuyorder()['id']

        merchantx1 = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][1][
                'value']
        balance1 = merchantx1['balance']
        frozen1 = merchantx1['frozen']
        assert int(balance1) == int(balance) - 10000000
        assert int(frozen1) == int(frozen) + 10000000


        book.opendeal(taker='user1', order_side='buy', order_id=oid, deal_quantity="10.000000 USDTARC",
                      order_sn=random.randint(10000, 500000), session_msg='x', suber='user1').assetResponsePass()
        did = book.getLastDeal()['id']

        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=2, session_msg='x',
                         suber='merchantx').assetResponsePass()
        mtoken.transfer(fromx='user1', to = 'meta.book', quantity = "10.000000 MUSDT", memo = f'process:2:{did}:3', suber = 'user1').assetResponseFail()
        mtoken.transfer(fromx='user1', to = 'meta.book', quantity = "10.000000 MUSDT", memo = f'process:3:1:3', suber = 'user1').assetResponseFail()
        mtoken.transfer(fromx='user1', to = 'meta.book', quantity = "10.000000 MUSDT", memo = f'process:3:{did}:4', suber = 'user1').assetResponseFail()
        mtoken.transfer(fromx='user1', to = 'meta.book', quantity = "1.000000 MUSDT", memo = f'process:3:{did}:3', suber = 'user1').assetResponseFail()

    def test_sellmu_errorcase(self):
        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][1][
                'value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        userBalance = mtoken.getLastRow("user1", 'accounts')['balance']
        metrantBalance = mtoken.getLastRow("merchantx", 'accounts')['balance']

        book.openorder(owner='merchantx', order_side='sell', pay_methods=["wechat"], va_quantity="10.000000 USDTARC",
                       va_price="6.0000 CNY", va_min_take_quantity="1.000000 USDTARC",
                       va_max_take_quantity="10.000000 USDTARC", memo='x', suber='merchantx').assetResponsePass()
        oid = book.getLastSellorder()['id']

        merchantx1 = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][1][
                'value']
        balance1 = merchantx1['balance']
        frozen1 = merchantx1['frozen']
        assert int(balance1) == int(balance) - 10000000
        assert int(frozen1) == int(frozen) + 10000000


        book.opendeal(taker='user1', order_side='sell', order_id=oid, deal_quantity="10.000000 USDTARC",
                      order_sn=random.randint(10000, 500000), session_msg='x', suber='user1').assetResponsePass()
        did = book.getLastDeal()['id']

        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=2, session_msg='x',
                         suber='merchantx').assetResponsePass()
        book.processdeal(account='user1', account_type=3, deal_id=did, action=3, session_msg='x',
                         suber='user1').assetResponsePass()
        # book.processdeal(account='merchantx', account_type=2, deal_id=did, action=4, session_msg='x',
                        #  suber='merchantx').assetResponsePass()
        mtoken.transfer(fromx='merchantx', to = 'meta.book', quantity = "10.000000 MUSDT", memo = f'process:3:{did}:4', suber = 'merchantx').assetResponseFail()
        mtoken.transfer(fromx='merchantx', to = 'meta.book', quantity = "10.000000 MUSDT", memo = f'process:2:1:4', suber = 'merchantx').assetResponseFail()
        mtoken.transfer(fromx='merchantx', to = 'meta.book', quantity = "10.000000 MUSDT", memo = f'process:2:{did}:5', suber = 'merchantx').assetResponseFail()

        mtoken.transfer(fromx='merchantx', to = 'meta.book', quantity = "1.000000 MUSDT", memo = f'process:2:{did}:4', suber = 'merchantx').assetResponseFail()
        mtoken.transfer(fromx='merchantx', to = 'meta.book', quantity = "10.00000000 METH", memo = f'process:2:{did}:4', suber = 'merchantx').assetResponseFail()
        arc.transfer(fromx='merchantx', to = 'meta.book', quantity = "10.000000 MUSDT", memo = f'process:2:{did}:4', suber = 'merchantx').assetResponseFail()

    def test_deposit(self):
        mtoken.transfer(fromx='merchantx', to = 'meta.book', quantity = "10.00000000 METH", memo = '', suber = 'merchantx').assetResponseFail()
        arc.transfer(fromx='merchantx', to = 'meta.book', quantity = "10.000000 MUSDT", memo = '', suber = 'merchantx').assetResponseFail()
        mtoken.transfer(fromx='merchantx', to = 'meta.book', quantity = "10.000000 MUSDT", memo = 'xx', suber = 'merchantx').assetResponseFail()

        book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][1][
                'value']
        mtoken.transfer(fromx='merchantx', to = 'meta.book', quantity = "10.000000 MUSDT", memo = '', suber = 'merchantx').assetResponsePass()
        book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][1][
                'value']


    def test_closemu_buy(self):
        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        userBalance = mtoken.getLastRow("user1", 'accounts')['balance']
        metrantBalance = mtoken.getLastRow("merchantx", 'accounts')['balance']

        book.openorder(owner='merchantx', order_side='buy', pay_methods=["wechat"], va_quantity="10.000000 USDTARC",
                       va_price="6.0000 CNY", va_min_take_quantity="1.000000 USDTARC",
                       va_max_take_quantity="10.000000 USDTARC", memo='x', suber='merchantx').assetResponsePass()
        oid = book.getLastBuyorder()['id']

        merchantx1 = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance1 = merchantx1['balance']
        frozen1 = merchantx1['frozen']
        assert int(balance1) == int(balance) - 10000000
        assert int(frozen1) == int(frozen) + 10000000

        mtoken.transfer(fromx='user1', to = 'meta.book', quantity = "10.000000 MUSDT", memo = f'opendeal:{oid}:{random.randint(10000, 500000)}:3', suber = 'user1').assetResponsePass()

        # book.opendeal(taker='user1', order_side='sell', order_id=oid, deal_quantity="10.000000 USDTARC",
        #               order_sn=random.randint(10000, 500000), session_msg='x', suber='user1').assetResponsePass()
        did = book.getLastDeal()['id']

        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=2, session_msg='x',
                         suber='merchantx').assetResponsePass()
        # book.processdeal(account='user1', account_type=3, deal_id=did, action=3, session_msg='x',
        #                  suber='user1').assetResponsePass()
        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=4, session_msg='x',
                         suber='merchantx').assetResponsePass()
        # time.sleep(2)

        # mtoken.transfer(fromx='merchantx', to = 'meta.book', quantity = "10.000000 MUSDT", memo = f'close:2:{did}', suber = 'merchantx').assetResponsePass()
    



        time.sleep(2)
        book.closedeal(account='user1', account_type=3, deal_id=did, session_msg='x',
                       suber='user1').assetResponsePass()
        # book.closeorder(owner='merchantx', order_side='buy',
        #                 order_id=oid, suber='merchantx').assetResponsePass()

        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance2 = merchantx['balance']
        frozen2 = merchantx['frozen']
        assert int(balance2) == int(balance) 
        assert frozen == frozen2

        userBalance2 = mtoken.getLastRow("user1", 'accounts')['balance']
        metrantBalance2 = mtoken.getLastRow("merchantx", 'accounts')['balance']
        assert int(str(userBalance2).split(".")[0]) == int(str(userBalance).split(".")[0]) -10
        assert int(str(metrantBalance2).split(".")[0]) == int(str(metrantBalance).split(".")[0]) +10


    def test_closemu(self):
        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        userBalance = mtoken.getLastRow("user1", 'accounts')['balance']
        metrantBalance = mtoken.getLastRow("merchantx", 'accounts')['balance']

        book.openorder(owner='merchantx', order_side='sell', pay_methods=["wechat"], va_quantity="10.000000 USDTARC",
                       va_price="6.0000 CNY", va_min_take_quantity="1.000000 USDTARC",
                       va_max_take_quantity="10.000000 USDTARC", memo='x', suber='merchantx').assetResponsePass()
        oid = book.getLastSellorder()['id']

        merchantx1 = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance1 = merchantx1['balance']
        frozen1 = merchantx1['frozen']
        assert int(balance1) == int(balance) - 10000000
        assert int(frozen1) == int(frozen) + 10000000


        book.opendeal(taker='user1', order_side='sell', order_id=oid, deal_quantity="10.000000 USDTARC",
                      order_sn=random.randint(10000, 500000), session_msg='x', suber='user1').assetResponsePass()
        did = book.getLastDeal()['id']

        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=2, session_msg='x',
                         suber='merchantx').assetResponsePass()
        book.processdeal(account='user1', account_type=3, deal_id=did, action=3, session_msg='x',
                         suber='user1').assetResponsePass()
        # book.processdeal(account='merchantx', account_type=2, deal_id=did, action=4, session_msg='x',
        #                  suber='merchantx').assetResponsePass()
        time.sleep(2)

        mtoken.transfer(fromx='merchantx', to = 'meta.book', quantity = "10.000000 MUSDT", memo = f'close:2:{did}', suber = 'merchantx').assetResponsePass()
    



        time.sleep(2)
        # book.closedeal(account='user1', account_type=3, deal_id=did, session_msg='x',
        #                suber='user1').assetResponsePass()
        # book.closeorder(owner='merchantx', order_side='sell',
        #                 order_id=oid, suber='merchantx').assetResponsePass()

        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance2 = merchantx['balance']
        frozen2 = merchantx['frozen']
        assert int(balance2) == int(balance)
        assert frozen == frozen2

        # userBalance2 = mtoken.getLastRow("user1", 'accounts')['balance']
        # metrantBalance2 = mtoken.getLastRow("merchantx", 'accounts')['balance']
        # assert int(str(userBalance2).split(".")[0]) == int(str(userBalance).split(".")[0]) +10
        # assert int(str(metrantBalance2).split(".")[0]) == int(str(metrantBalance).split(".")[0]) -10


    def test_closemu_errocase(self):
        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][1][
                'value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        userBalance = mtoken.getLastRow("user1", 'accounts')['balance']
        metrantBalance = mtoken.getLastRow("merchantx", 'accounts')['balance']

        book.openorder(owner='merchantx', order_side='sell', pay_methods=["wechat"], va_quantity="10.000000 USDTARC",
                       va_price="6.0000 CNY", va_min_take_quantity="1.000000 USDTARC",
                       va_max_take_quantity="10.000000 USDTARC", memo='x', suber='merchantx').assetResponsePass()
        oid = book.getLastSellorder()['id']

        merchantx1 = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][1][
                'value']
        balance1 = merchantx1['balance']
        frozen1 = merchantx1['frozen']
        assert int(balance1) == int(balance) - 10000000
        assert int(frozen1) == int(frozen) + 10000000


        book.opendeal(taker='user1', order_side='sell', order_id=oid, deal_quantity="10.000000 USDTARC",
                      order_sn=random.randint(10000, 500000), session_msg='x', suber='user1').assetResponsePass()
        did = book.getLastDeal()['id']

        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=2, session_msg='x',
                         suber='merchantx').assetResponsePass()
        book.processdeal(account='user1', account_type=3, deal_id=did, action=3, session_msg='x',
                         suber='user1').assetResponsePass()
        # book.processdeal(account='merchantx', account_type=2, deal_id=did, action=4, session_msg='x',
                        #  suber='merchantx').assetResponsePass()
        time.sleep(2)

        # mtoken.transfer(fromx='merchantx', to = 'meta.book', quantity = "10.000000 MUSDT", memo = f'close:2:{did}', suber = 'merchantx').assetResponsePass()

        mtoken.transfer(fromx='merchantx', to = 'meta.book', quantity = "10.000000 MUSDT", memo = f'close:3:{did}', suber = 'merchantx').assetResponseFail()
        # mtoken.transfer(fromx='user1', to = 'meta.book', quantity = "10.000000 MUSDT", memo = f'close:3:{did}', suber = 'user1').assetResponseFail()
        mtoken.transfer(fromx='merchantx', to = 'meta.book', quantity = "10.000000 MUSDT", memo = f'close:2:3', suber = 'merchantx').assetResponseFail()
        mtoken.transfer(fromx='merchantx', to = 'meta.book', quantity = "1.000000 MUSDT", memo = f'close:2:{did}', suber = 'merchantx').assetResponseFail()


     # 测试手动关闭订单
    def test_closeorder(self):
        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        userBalance = mtoken.getLastRow("user1", 'accounts')['balance']

        book.openorder(owner='merchantx', order_side='buy', pay_methods=["wechat"], va_quantity="20.000000 USDTARC",
                       va_price="6.0000 CNY", va_min_take_quantity="1.000000 USDTARC",
                       va_max_take_quantity="10.000000 USDTARC", memo='x', suber='merchantx').assetResponsePass()
        oid = book.getLastBuyorder()['id']

        merchantx1 = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance1 = merchantx1['balance']
        frozen1 = merchantx1['frozen']
        assert int(balance1) == int(balance) - 20000000
        assert int(frozen1) == int(frozen) + 20000000


        book.opendeal(taker='user1', order_side='buy', order_id=oid, deal_quantity="10.000000 USDTARC",
                      order_sn=random.randint(10000, 500000), session_msg='x', suber='user1').assetResponsePass()
        did = book.getLastDeal()['id']

        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=2, session_msg='x',
                         suber='merchantx').assetResponsePass()
        book.processdeal(account='user1', account_type=3, deal_id=did, action=3, session_msg='x',
                         suber='user1').assetResponsePass()
        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=4, session_msg='x',
                         suber='merchantx').assetResponsePass()
        
        time.sleep(2)
        book.closedeal(account='user1', account_type=3, deal_id=did, session_msg='x',
                       suber='user1').assetResponsePass()
        book.closeorder(owner='merchantx', order_side='buy',
                        order_id=oid, suber='merchantx').assetResponsePass()

        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0][
                'value']
        balance2 = merchantx['balance']
        frozen2 = merchantx['frozen']
        assert int(balance2) == int(balance) - 40000
        assert frozen == frozen2

        userBalance2 = mtoken.getLastRow("user1", 'accounts')['balance']
        assert userBalance2 == userBalance