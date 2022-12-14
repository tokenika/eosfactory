
from otc.otcbook.otcbook import otcbookv as o
from amax.cnydtoken.cnyd import CNYD
from xchain.mtoken.mtoken import Mtoken
import time
import random

mtoken = Mtoken()
cnyd = CNYD()
book = o()
otcbookv = o()


def test_00():
        book.setmerchant(merchant='user1',status=1, merchant_name='测试商户5555', 
                         merchant_detail='merchant_detail',email='xxx@qq.com', memo='', reject_reason="拒绝", by_force="true", suber='ad')



class Testotcv25:

    def test_1_setmerchant(self):
        # pass
        book.setmerchant(merchant='ck',status=1, merchant_name='测试商户ck', 
                         merchant_detail='merchant_detail',email='xxx@qq.com', memo='', reject_reason="x", by_force="true", suber='ad').assetResponsePass()
        # merchant不存在
        book.setmerchant(merchant='ck11',status=1, merchant_name='测试商户ck', 
                         merchant_detail='merchant_detail',email='xxx@qq.com', memo='', reject_reason="x", by_force="true", suber='ad').assetResponseFail()

        # merchant已存在, by_force=false, 报错
        book.setmerchant(merchant='ck',status=1, merchant_name='测试商户ck', 
                         merchant_detail='merchant_detail',email='xxx@qq.com', memo='', reject_reason="x", by_force="false", suber='ad').assetResponseFail()




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







    # 旧测试代码, 可以运行通过
    def test_sellmu(self):
        merchantxpro = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantxpro', 'merchantxpro', 1)['assets'][0][
                'value']
        balance = merchantxpro['balance']
        frozen = merchantxpro['frozen']

        userBalance = mtoken.getLastRow("user1", 'accounts')['balance']
        metrantBalance = mtoken.getLastRow("merchantxpro", 'accounts')['balance']

        book.openorder(owner='merchantxpro', order_side='sell', pay_methods=["wechat"], va_quantity="10.000000 USDTARC",
                       va_price="6.0000 CNY", va_min_take_quantity="1.000000 USDTARC",
                       va_max_take_quantity="10.000000 USDTARC", memo='x', suber='merchantxpro').assetResponsePass()
        oid = book.getLastSellorder()['id']

        merchantxpro1 = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantxpro', 'merchantxpro', 1)['assets'][0][
                'value']
        balance1 = merchantxpro1['balance']
        frozen1 = merchantxpro1['frozen']
        assert int(balance1) == int(balance) - 10000000
        assert int(frozen1) == int(frozen) + 10000000


        book.opendeal(taker='user1', order_side='sell', order_id=oid, deal_quantity="10.000000 USDTARC",
                      order_sn=random.randint(10000, 500000), session_msg='x', suber='user1').assetResponsePass()
        did = book.getLastDeal()['id']

        book.processdeal(account='merchantxpro', account_type=2, deal_id=did, action=2, session_msg='x',
                         suber='merchantxpro').assetResponsePass()
        book.processdeal(account='user1', account_type=3, deal_id=did, action=3, session_msg='x',
                         suber='user1').assetResponsePass()
        # book.processdeal(account='merchantxpro', account_type=2, deal_id=did, action=4, session_msg='x',
                        #  suber='merchantxpro').assetResponsePass()
        
        time.sleep(2)

        mtoken.transfer(fromx='merchantxpro', to = 'meta.book', quantity = "10.000000 MUSDT", memo = f'process:2:{did}:4', suber = 'merchantxpro').assetResponsePass()

        time.sleep(2)
        book.closedeal(account='user1', account_type=3, deal_id=did, session_msg='x',
                       suber='user1').assetResponsePass()
        # book.closeorder(owner='merchantxpro', order_side='sell',
        #                 order_id=oid, suber='merchantxpro').assetResponsePass()

        merchantxpro = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantxpro', 'merchantxpro', 1)['assets'][0][
                'value']
        balance2 = merchantxpro['balance']
        frozen2 = merchantxpro['frozen']
        assert int(balance2) == int(balance) 
        assert frozen == frozen2

        userBalance2 = mtoken.getLastRow("user1", 'accounts')['balance']
        metrantBalance2 = mtoken.getLastRow("merchantxpro", 'accounts')['balance']
        assert int(str(userBalance2).split(".")[0]) == int(str(userBalance).split(".")[0]) +10
        assert int(str(metrantBalance2).split(".")[0]) == int(str(metrantBalance).split(".")[0]) -10


    # 旧代码
    def test_closemu_buy(self):
        merchantxpro = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantxpro', 'merchantxpro', 1)['assets'][0][
                'value']
        balance = merchantxpro['balance']
        frozen = merchantxpro['frozen']

        userBalance = mtoken.getLastRow("user1", 'accounts')['balance']
        metrantBalance = mtoken.getLastRow("merchantxpro", 'accounts')['balance']

        book.openorder(owner='merchantxpro', order_side='buy', pay_methods=["wechat"], va_quantity="10.000000 USDTARC",
                       va_price="6.0000 CNY", va_min_take_quantity="1.000000 USDTARC",
                       va_max_take_quantity="10.000000 USDTARC", memo='x', suber='merchantxpro').assetResponsePass()
        oid = book.getLastBuyorder()['id']

        merchantxpro1 = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantxpro', 'merchantxpro', 1)['assets'][0][
                'value']
        balance1 = merchantxpro1['balance']
        frozen1 = merchantxpro1['frozen']
        assert int(balance1) == int(balance) - 10000000
        assert int(frozen1) == int(frozen) + 10000000

        mtoken.transfer(fromx='user1', to = 'meta.book', quantity = "10.000000 MUSDT", memo = f'opendeal:{oid}:{random.randint(10000, 500000)}:3', suber = 'user1').assetResponsePass()

        # book.opendeal(taker='user1', order_side='sell', order_id=oid, deal_quantity="10.000000 USDTARC",
        #               order_sn=random.randint(10000, 500000), session_msg='x', suber='user1').assetResponsePass()
        did = book.getLastDeal()['id']

        book.processdeal(account='merchantxpro', account_type=2, deal_id=did, action=2, session_msg='x',
                         suber='merchantxpro').assetResponsePass()
        # book.processdeal(account='user1', account_type=3, deal_id=did, action=3, session_msg='x',
        #                  suber='user1').assetResponsePass()
        book.processdeal(account='merchantxpro', account_type=2, deal_id=did, action=4, session_msg='x',
                         suber='merchantxpro').assetResponsePass()
        # time.sleep(2)

        # mtoken.transfer(fromx='merchantxpro', to = 'meta.book', quantity = "10.000000 MUSDT", memo = f'close:2:{did}', suber = 'merchantxpro').assetResponsePass()
    



        time.sleep(2)
        book.closedeal(account='user1', account_type=3, deal_id=did, session_msg='x',
                       suber='user1').assetResponsePass()
        # book.closeorder(owner='merchantxpro', order_side='buy',
        #                 order_id=oid, suber='merchantxpro').assetResponsePass()

        merchantxpro = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantxpro', 'merchantxpro', 1)['assets'][0][
                'value']
        balance2 = merchantxpro['balance']
        frozen2 = merchantxpro['frozen']
        assert int(balance2) == int(balance) 
        assert frozen == frozen2

        userBalance2 = mtoken.getLastRow("user1", 'accounts')['balance']
        metrantBalance2 = mtoken.getLastRow("merchantxpro", 'accounts')['balance']
        assert int(str(userBalance2).split(".")[0]) == int(str(userBalance).split(".")[0]) -10
        assert int(str(metrantBalance2).split(".")[0]) == int(str(metrantBalance).split(".")[0]) +10






def test_openorder(): otcbookv.openorder(owner='merchantxpro', order_side='buy', pay_methods=["alipay", "wechat"],
                                         va_quantity="10.000000 USDTTRC", va_price="2.1000 CNY",
                                         va_min_take_quantity="10.000000 USDTTRC", va_max_take_quantity="10.000000 USDTTRC",
                                         memo='memo-openorder', suber='merchantxpro')

def test_openorder2(): otcbookv.openorder(owner='merchantxpro', order_side='sell', pay_methods=["alipay", "wechat"],
                                         va_quantity="10.000000 USDTTRC", va_price="2.1100 CNY",
                                         va_min_take_quantity="10.000000 USDTTRC", va_max_take_quantity="10.000000 USDTTRC",
                                         memo='memo-openorder', suber='merchantxpro')


def test_openorderbuymu(): otcbookv.openorder(owner='merchantxpro', order_side='buy', pay_methods=["alipay", "wechat"],
                                         va_quantity="10.000000 USDTARC", va_price="2.2000 CNY",
                                         va_min_take_quantity="10.000000 USDTARC", va_max_take_quantity="10.000000 USDTARC",
                                         memo='memo-MU', suber='merchantxpro')


def test_openordersellmu(): otcbookv.openorder(owner='merchantxpro', order_side='sell', pay_methods=["alipay", "wechat"],
                                         va_quantity="10.000000 USDTARC", va_price="2.2100 CNY",
                                         va_min_take_quantity="10.000000 USDTARC", va_max_take_quantity="10.000000 USDTARC",
                                         memo='memo-MU', suber='merchantxpro')



def test_opendeal(): otcbookv.opendeal(taker='user1', order_side='buy', order_id=1024, deal_quantity="10.000000 USDTTRC",
                                       order_sn=random.randint(10000, 500000), session_msg='x', suber='user1')

def test_opendeal2(): otcbookv.opendeal(taker='user1', order_side='sell', order_id=1015, deal_quantity="10.000000 USDTTRC",
                                       order_sn=random.randint(10000, 500000), session_msg='x', suber='user1')


def test_opendeal4(): otcbookv.opendeal(taker='user1', order_side='sell', order_id=1016, deal_quantity="10.000000 USDTARC",
                                       order_sn=random.randint(10000, 500000), session_msg='x', suber='user1')

def test_processdeal2(): otcbookv.processdeal(account='merchantxpro', account_type=2, deal_id=1012, action=2, session_msg='接单',
                                             suber='merchantxpro')


def test_processdeal3(): otcbookv.processdeal(account='user1', account_type=3, deal_id=1012, action=3, session_msg='用户转币',
                                             suber='user1')


def test_processdeal4(): otcbookv.processdeal(account='merchantxpro', account_type=2, deal_id=1012, action=4, session_msg='商户转款',
                                             suber='merchantxpro')     



def test_canceldeal(): otcbookv.canceldeal(account='user1', account_type=3, deal_id=1047,
                                           is_taker_black='false', suber='user1')

def test_canceldeal1(): otcbookv.canceldeal(account='merchantxpro', account_type=2, deal_id=1048,
                                           is_taker_black='false', suber='merchantxpro')


def test_closedeal(): otcbookv.closedeal(account='user1', account_type=3, deal_id=1017, session_msg='确认收款,结束',
                                             suber='user1')


def test_startarbit(): otcbookv.startarbit(account='user1', account_type=3, deal_id=1011,suber='user1')


def test_startarbit1(): otcbookv.startarbit(account='merchantxpro', account_type=2, deal_id=1010,suber='merchantxpro')

def test_addarbiter(): otcbookv.addarbiter(account='ad', email='x', suber='ad')


def test_closearbit(): otcbookv.closearbit(account='ad', deal_id=1011,
                                           arbit_result=1, session_msg='end:1', suber='ad')



def test_tt0(): mtoken.transfer(fromx='user1', to = 'meta.book', quantity = "10.000000 MUSDT", memo = f'opendeal:1018:{random.randint(10000, 500000)}:3', suber = 'user1')


def test_tt1() : book.processdeal(account='merchantxpro', account_type=2, deal_id=1021, action=2, session_msg='x',
                         suber='merchantxpro').assetResponsePass()
def test_tt2() : book.processdeal(account='merchantxpro', account_type=2, deal_id=1021, action=4, session_msg='x',
                         suber='merchantxpro').assetResponsePass()

def test_closedeal11(): otcbookv.closedeal(account='user1', account_type=3, deal_id=1021, session_msg='确认收款,结束',
                                             suber='user1')


 #orderid=14
 # 旧代码-用于调试
def test_closemu_buy():
        merchantxpro = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantxpro', 'merchantxpro', 1)['assets'][0][
                'value']
        balance = merchantxpro['balance']
        frozen = merchantxpro['frozen']

        userBalance = mtoken.getLastRow("user1", 'accounts')['balance']
        metrantBalance = mtoken.getLastRow("merchantxpro", 'accounts')['balance']

        book.openorder(owner='merchantxpro', order_side='buy', pay_methods=["wechat"], va_quantity="10.000000 USDTARC",
                       va_price="4.4500 CNY", va_min_take_quantity="1.000000 USDTARC",
                       va_max_take_quantity="10.000000 USDTARC", memo='x', suber='merchantxpro').assetResponsePass()
        oid = book.getLastBuyorder()['id']

        merchantxpro1 = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantxpro', 'merchantxpro', 1)['assets'][0][
                'value']
        balance1 = merchantxpro1['balance']
        frozen1 = merchantxpro1['frozen']
        assert int(balance1) == int(balance) - 10000000
        assert int(frozen1) == int(frozen) + 10000000

        #mtoken.transfer(fromx='user1', to = 'meta.book', quantity = "10.000000 MUSDT", memo = f'opendeal:{oid}:{random.randint(10000, 500000)}:3', suber = 'user1')









        ''''''''''
        did = book.getLastDeal()['id']

        book.processdeal(account='merchantxpro', account_type=2, deal_id=did, action=2, session_msg='x',
                         suber='merchantxpro').assetResponsePass()

        book.processdeal(account='merchantxpro', account_type=2, deal_id=did, action=4, session_msg='x',
                         suber='merchantxpro').assetResponsePass()


        time.sleep(2)
        book.closedeal(account='user1', account_type=3, deal_id=did, session_msg='x',
                       suber='user1').assetResponsePass()


        merchantxpro = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantxpro', 'merchantxpro', 1)['assets'][0][
                'value']
        balance2 = merchantxpro['balance']
        frozen2 = merchantxpro['frozen']
        assert int(balance2) == int(balance) 
        assert frozen == frozen2

        userBalance2 = mtoken.getLastRow("user1", 'accounts')['balance']
        metrantBalance2 = mtoken.getLastRow("merchantxpro", 'accounts')['balance']
        assert int(str(userBalance2).split(".")[0]) == int(str(userBalance).split(".")[0]) -10
        assert int(str(metrantBalance2).split(".")[0]) == int(str(metrantBalance).split(".")[0]) +10
'''''''''''