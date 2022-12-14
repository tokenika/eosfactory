from hashlib import blake2b
from otc.otcswap.otcswap import OTCSWAP
from otc.otcbook.otcbook import otcbookv as o
from xchain.mtoken.mtoken import Mtoken
from otc.otcconf.otcconfv import otcconfv as c
from amax.arctoken.arc import arc as a
from base import amcli

arc = a()
import random

otcconfv = c()
mtoken = Mtoken()

book = o()
otcswap = OTCSWAP()

class TestSettleto:
    def test_1(self):
        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][1][
                'value']
        balance = merchantx['balance']
        frozen = merchantx['frozen']

        userBalance = mtoken.getLastRow("abcd12341234", 'accounts')['balance']

        book.openorder(owner='merchantx', order_side='buy', pay_methods=["wechat"], va_quantity="15.000000 USDTERC",
                       va_price="6.0000 CNY", va_min_take_quantity="1.000000 USDTERC",
                       va_max_take_quantity="15.000000 USDTERC", memo='x', suber='merchantx').assetResponsePass()
        oid = book.getLastBuyorder()['id']

        book.opendeal(taker='abcd12341234', order_side='buy', order_id=oid, deal_quantity="15.000000 USDTERC",
                      order_sn=random.randint(10000, 500000), session_msg='x', suber='abcd12341234').assetResponsePass()
        did = book.getLastDeal()['id']

        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=2, session_msg='x',
                         suber='merchantx').assetResponsePass()
        book.processdeal(account='abcd12341234', account_type=3, deal_id=did, action=3, session_msg='x',
                         suber='abcd12341234').assetResponsePass()
        book.processdeal(account='merchantx', account_type=2, deal_id=did, action=4, session_msg='x',
                         suber='merchantx').assetResponsePass()
        book.closedeal(account='abcd12341234', account_type=3, deal_id=did, session_msg='x',
                       suber='abcd12341234').assetResponsePass()
        book.closeorder(owner='merchantx', order_side='buy',
                        order_id=oid, suber='merchantx').assetResponsePass()

        merchantx = \
            book.getLastRowByIndex(book.contract, 'merchants', 'name', 'merchantx', 'merchantx', 1)['assets'][1][
                'value']
        balance2 = merchantx['balance']
        frozen2 = merchantx['frozen']
        assert int(balance2) == int(balance) - 75000
        assert frozen == frozen2

        userBalance2 = mtoken.getLastRow("abcd12341234", 'accounts')['balance']
        assert userBalance2 == userBalance
    
    
    def test_transfer(self): 
        newuser = amcli.newaccount("user1")
        arc.transfer(fromx='ad',to=newuser,quantity="100.0000 BALC",memo='',suber='ad').assetResponsePass()
        arc.transfer(fromx=newuser,to=otcswap.contract,quantity="10.0000 BALC",memo='',suber=newuser).assetResponseFail()
        
        otcswap.settleto(user=newuser,fee="0.500000 MUSDT",quantity="100.000000 MUSDT",suber=book.contract)
        arc.transfer(fromx=newuser,to=otcswap.contract,quantity="1.0000 BALC",memo='',suber=newuser).assetResponseFail()

        arc.transfer(fromx=newuser,to=otcswap.contract,quantity="0.0750 BALC",memo='',suber=newuser).assetResponsePass()
        arc.transfer(fromx=newuser,to=otcswap.contract,quantity="0.0700 BALC",memo='',suber=newuser).assetResponseFail()
        
        account = otcswap.getLastRowByIndex(otcswap.contract,'accounts','i64',newuser,newuser,1)
        balance = account['balance']
        sum = account['sum']
        assert balance == 0
        assert sum == 750
        
        otcswap.settleto(user=newuser,fee="0.500000 MUSDT",quantity="100.000000 MUSDT",suber=book.contract)
        arc.transfer(fromx=newuser,to=otcswap.contract,quantity="0.0700 BALC",memo='',suber=newuser).assetResponsePass()
        
        account = otcswap.getLastRowByIndex(otcswap.contract,'accounts','i64',newuser,newuser,1)
        balance = account['balance']
        sum = sum + 750
        assert balance == 50
        assert sum == account['sum']
        
        arc.transfer(fromx=newuser,to=otcswap.contract,quantity="-1.0000 BALC",memo='',suber=newuser).assetResponseFail()


        

    def test_setadmin(self): 
        otcswap.setconf(conf="otcconfx", suber=otcswap.contract).assetResponseFail()
        otcswap.setconf(conf="otcbook1", suber=otcswap.contract).assetResponseFail()
        otcswap.setconf(conf="metaconf1111", suber="user1").assetResponseFail()
        otcswap.setconf(conf="metaconf1111", suber=otcswap.contract).assetResponsePass()
        otcswap.setconf(conf="otcconf1", suber=otcswap.contract).assetResponsePass()

    
    def test_settleto_erro(self):
        newuser = amcli.newaccount("user1")
        otcswap.settleto(user="userxx",fee="0.500000 MUSDT",quantity="100.000000 MUSDT",suber=book.contract).assetResponseFail()
        otcswap.settleto(user="userxx",fee="0.000000 MUSDT",quantity="100.000000 MUSDT",suber=book.contract).assetResponseFail()
        otcswap.settleto(user="userxx",fee="0.500000 MUSDT",quantity="0.000000 MUSDT",suber=book.contract).assetResponseFail()
        otcswap.settleto(user="userxx",fee="0.500000 MUSDT",quantity="-100.000000 MUSDT",suber=book.contract).assetResponseFail()
        otcswap.settleto(user="userxx",fee="-0.500000 MUSDT",quantity="100.000000 MUSDT",suber=book.contract).assetResponseFail()
        otcswap.settleto(user="userxx",fee="0.50000 MUSDT",quantity="100.000000 MUSDT",suber=book.contract).assetResponseFail()
        otcswap.settleto(user="userxx",fee="0.500000 MUSDT",quantity="100.00000 MUSDT",suber=book.contract).assetResponseFail()
        otcswap.settleto(user="userxx",fee="0.500000 MUSDT",quantity="100.0000000 USDT",suber=book.contract).assetResponseFail()
        otcswap.settleto(user="userxx",fee="0.500000 USDT",quantity="100.0000000 MUSDT",suber=book.contract).assetResponseFail()
        otcswap.settleto(user=newuser,fee="0.500000 MUSDT",quantity="100.000000 MUSDT",suber="ad").assetResponseFail()

    
    def test_settleto(self): 
        newuser = amcli.newaccount("user1")
        balance = 0
        sum = 0
       
        otcswap.settleto(user=newuser,fee="0.500000 MUSDT",quantity="100.000000 MUSDT",suber=book.contract).assetResponsePass()
        
        account = otcswap.getLastRowByIndex(otcswap.contract,'accounts','i64',newuser,newuser,1)
        balance = 5000 * 0.15
        assert account['balance'] == balance
        assert account['sum'] == balance

        otcswap.settleto(user=newuser,fee="1.000000 MUSDT",quantity="200.000000 MUSDT",suber=book.contract).assetResponsePass()
        account = otcswap.getLastRowByIndex(otcswap.contract,'accounts','i64',newuser,newuser,1)
        balance = balance *3
        assert account['balance'] == balance
        assert account['sum'] == balance

        otcswap.settleto(user=newuser,fee="5.000000 MUSDT",quantity="1000.000000 MUSDT",suber=book.contract).assetResponsePass()
        account = otcswap.getLastRowByIndex(otcswap.contract,'accounts','i64',newuser,newuser,1)
        balance = balance + 50000 * 0.25
        assert account['balance'] == balance
        assert account['sum'] == balance

        otcswap.settleto(user=newuser,fee="5.000000 MUSDT",quantity="1000.000001 MUSDT",suber=book.contract).assetResponsePass()
        account = otcswap.getLastRowByIndex(otcswap.contract,'accounts','i64',newuser,newuser,1)
        balance = balance + 50000 * 0.25
        assert account['balance'] == balance
        assert account['sum'] == balance
        
        otcswap.settleto(user=newuser,fee="5.500000 MUSDT",quantity="1100.000000 MUSDT",suber=book.contract).assetResponsePass()
        account = otcswap.getLastRowByIndex(otcswap.contract,'accounts','i64',newuser,newuser,1)
        balance = balance + 55000 * 0.25
        assert account['balance'] == balance
        assert account['sum'] == balance
        
        otcswap.settleto(user=newuser,fee="10.000000 MUSDT",quantity="2000.000000 MUSDT",suber=book.contract).assetResponsePass()
        account = otcswap.getLastRowByIndex(otcswap.contract,'accounts','i64',newuser,newuser,1)
        balance = balance + 100000 * 0.35
        assert account['balance'] == balance
        assert account['sum'] == balance
        
        otcswap.settleto(user=newuser,fee="15.000000 MUSDT",quantity="3000.000000 MUSDT",suber=book.contract).assetResponsePass()
        account = otcswap.getLastRowByIndex(otcswap.contract,'accounts','i64',newuser,newuser,1)
        balance = balance + 150000 * 0.5
        assert account['balance'] == balance
        assert account['sum'] == balance
        
        otcswap.settleto(user=newuser,fee="30.000000 MUSDT",quantity="6000.000000 MUSDT",suber=book.contract).assetResponsePass()
        account = otcswap.getLastRowByIndex(otcswap.contract,'accounts','i64',newuser,newuser,1)
        balance = balance + 300000 * 0.5
        assert account['balance'] == balance
        assert account['sum'] == balance
        
        