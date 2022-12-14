import random

from otc.otcbook.otcbook import otcbookv as o
from xchain.mtoken.mtoken import Mtoken
mtoken = Mtoken()

book = o()


class Testcancelarbit:
    # 仲裁2结果，关闭交易，退回押金
    def test_1(self):
        merchantx = \
        book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0]['value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        userBalance = mtoken.getLastRow("user1",'accounts')['balance']

        book.openorder(owner='merchantx', order_side='buy', pay_methods=["wechat"], va_quantity="10.000000 USDTERC",
                       va_price="6.0000 CNY", va_min_take_quantity="1.000000 USDTERC",
                       va_max_take_quantity="10.000000 USDTERC", memo='x', suber='merchantx').assetResponsePass()
        oid = book.getLastBuyorder()['id']

        book.opendeal(taker='user1', order_side='buy', order_id=oid, deal_quantity="10.000000 USDTERC",
                      order_sn=random.randint(10000, 500000), session_msg='x', suber='user1').assetResponsePass()
        did = book.getLastDeal()['id']

        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=2, session_msg='x',
                         suber='merchantx').assetResponsePass()
        book.startarbit(account='user1', account_type=3, deal_id=did, arbiter='merchantx',
                            suber='user1')
        book.closearbit(account='ad', deal_id=did, arbit_result=0, suber='ad')
        # book.processdeal(account='user1', account_type=3, deal_id=did, action=3, session_msg='x',
        #                  suber='user1').assetResponsePass()
        # book.processdeal(account='merchantx', account_type=2, deal_id=did, action=4, session_msg='x',
        #                  suber='merchantx').assetResponsePass()
        book.closeorder(owner='merchantx', order_side='buy', order_id=oid, suber='merchantx').assetResponsePass()

        merchantx = \
        book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0]['value']
        balance2 = merchantx['balance']
        frozen2 = merchantx['frozen']
        assert balance == balance2
        assert frozen == frozen2

        userBalance2 = mtoken.getLastRow("user1",'accounts')['balance']
        assert userBalance2==userBalance

 # 仲裁2结果，关闭交易，退回押金
    def test_2(self):
        merchantx = \
        book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0]['value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        userBalance = mtoken.getLastRow("user1",'accounts')['balance']

        book.openorder(owner='merchantx', order_side='buy', pay_methods=["wechat"], va_quantity="10.000000 USDTERC",
                       va_price="6.0000 CNY", va_min_take_quantity="1.000000 USDTERC",
                       va_max_take_quantity="10.000000 USDTERC", memo='x', suber='merchantx').assetResponsePass()
        oid = book.getLastBuyorder()['id']

        book.opendeal(taker='user1', order_side='buy', order_id=oid, deal_quantity="10.000000 USDTERC",
                      order_sn=random.randint(10000, 500000), session_msg='x', suber='user1').assetResponsePass()
        did = book.getLastDeal()['id']

        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=2, session_msg='x',
                         suber='merchantx').assetResponsePass()
        book.startarbit(account='user1', account_type=3, deal_id=did, arbiter='ad',
                            suber='user1')
        book.closearbit(account='ad', deal_id=did, arbit_result=1, suber='ad')
        # book.processdeal(account='user1', account_type=3, deal_id=did, action=3, session_msg='x',
        #                  suber='user1').assetResponsePass()
        # book.processdeal(account='merchantx', account_type=2, deal_id=did, action=4, session_msg='x',
        #                  suber='merchantx').assetResponsePass()
        book.closeorder(owner='merchantx', order_side='buy', order_id=oid, suber='merchantx').assetResponsePass()

        merchantx = \
        book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0]['value']
        balance2 = merchantx['balance']
        frozen2 = merchantx['frozen']
        assert int(balance2) == int(balance) - 10**7
        assert frozen == frozen2

        userBalance2 = mtoken.getLastRow("user1",'accounts')['balance']
        assert userBalance2!=userBalance

   # 仲裁3结果，关闭交易，退回押金
    def test_3(self):
        merchantx = \
        book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0]['value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        userBalance = mtoken.getLastRow("user1",'accounts')['balance']

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
        book.startarbit(account='user1', account_type=3, deal_id=did, arbiter='ad',
                            suber='user1')
        # book.closearbit(account='ad', deal_id=did, arbit_result=0, suber='ad')

        # book.processdeal(account='merchantx', account_type=2, deal_id=did, action=4, session_msg='x',
        #                  suber='merchantx').assetResponsePass()
        # book.closeorder(owner='merchantx', order_side='buy', order_id=oid, suber='merchantx').assetResponsePass()

        # merchantx = \
        # book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0]['value']
        # balance2 = merchantx['balance']
        # frozen2 = merchantx['frozen']
        # assert balance == balance2
        # assert frozen == frozen2

        # userBalance2 = mtoken.getLastRow("user1",'accounts')['balance']
        # assert userBalance2==userBalance

 # 仲裁3结果，关闭交易，退回押金
    def test_4(self):
        merchantx = \
        book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0]['value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        userBalance = mtoken.getLastRow("user1",'accounts')['balance']

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
        book.startarbit(account='user1', account_type=3, deal_id=did, arbiter='ad',
                            suber='user1')
        book.closearbit(account='ad', deal_id=did, arbit_result=1, suber='ad')

        # book.processdeal(account='merchantx', account_type=2, deal_id=did, action=4, session_msg='x',
        #                  suber='merchantx').assetResponsePass()
        book.closeorder(owner='merchantx', order_side='buy', order_id=oid, suber='merchantx').assetResponsePass()

        merchantx = \
        book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0]['value']
        balance2 = merchantx['balance']
        frozen2 = merchantx['frozen']
        assert int(balance2) == int(balance) - 10**7
        assert frozen == frozen2

        userBalance2 = mtoken.getLastRow("user1",'accounts')['balance']
        assert userBalance2!=userBalance



 # 仲裁4结果，关闭交易，退回押金
    def test_5(self):
        merchantx = \
        book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0]['value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        userBalance = mtoken.getLastRow("user1",'accounts')['balance']

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
        book.startarbit(account='user1', account_type=3, deal_id=did, arbiter='ad',
                            suber='user1')
        book.closearbit(account='ad', deal_id=did, arbit_result=0, suber='ad')


        book.closeorder(owner='merchantx', order_side='buy', order_id=oid, suber='merchantx').assetResponsePass()

        merchantx = \
        book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0]['value']
        balance2 = merchantx['balance']
        frozen2 = merchantx['frozen']
        assert balance == balance2
        assert frozen == frozen2

        userBalance2 = mtoken.getLastRow("user1",'accounts')['balance']
        assert userBalance2==userBalance

 # 仲裁4结果，关闭交易，退回押金
    def test_6(self):
        merchantx = \
        book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0]['value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        userBalance = mtoken.getLastRow("user1",'accounts')['balance']

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
        book.startarbit(account='user1', account_type=3, deal_id=did, arbiter='ad',
                            suber='user1')
        book.closearbit(account='ad', deal_id=did, arbit_result=1, suber='ad')

        book.closeorder(owner='merchantx', order_side='buy', order_id=oid, suber='merchantx').assetResponsePass()

        merchantx = \
        book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][0]['value']
        balance2 = merchantx['balance']
        frozen2 = merchantx['frozen']
        assert int(balance2) == int(balance) - 10**7
        assert frozen == frozen2

        userBalance2 = mtoken.getLastRow("user1",'accounts')['balance']
        assert userBalance2!=userBalance