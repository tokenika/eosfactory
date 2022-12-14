import csv
import logging
import os
from otc.otcbook.otcbook import otcbookv as o
from amax.cnydtoken.cnyd import CNYD
from xchain.mtoken.mtoken import Mtoken

mtoken = Mtoken()
cnyd = CNYD()
otcbookv = o()


def test_transfer1(): mtoken.transfer(fromx='merchantxpro', to=otcbookv.contract,
                                      quantity="100.000000 MUSDT", memo='deposit', suber='merchantxpro')


def test_transfer2(): cnyd.transfer(fromx='merchantx', to=otcbookv.contract,
                                    quantity="10000.0000 CNYD", memo='', suber='merchantx')


def test_transfer_merchant(): mtoken.transfer(fromx='p2.mart', to=otcbookv.contract,
                                              quantity="10.000000 MUSDT", memo='apply:测试x2:描述:xx@qq.com', suber='p2.mart')


def test_cancelarbit(): otcbookv.cancelarbit(
    account_type=1, account='user1', deal_id=1, session_msg='x', suber='user1')


def test_canceldeal(): otcbookv.canceldeal(account='user1', account_type=3, deal_id=1033,
                                           is_taker_black='false', suber='user1')

def test_addarbiter(): otcbookv.addarbiter(account='555544441111', email='x', suber='ad')


def test_delarbiter(): otcbookv.delarbiter(account='mk', suber='ad')

def test_closearbit(): otcbookv.closearbit(account='ck', deal_id=1009,
                                           arbit_result=0, session_msg='end:0', suber='ck')


def test_closedeal(): otcbookv.closedeal(account='555544441111', account_type=3, deal_id=2042, session_msg='确认收款,结束',
                                             suber='555544441111')


def test_closeorder(): otcbookv.closeorder(
    owner='merchantxpro', order_side='buy', order_id=2035, suber='merchantxpro')


def test_notification(): otcbookv.notification(
    account='user1', info=1, memo='x', suber='user1')


def test_opendeal(): otcbookv.opendeal(taker='555544441111', order_side='buy', order_id=2035, deal_quantity="10.000000 USDTTRC",
                                       order_sn=15125225, session_msg='x', suber='555544441111')




def test_openorder(): otcbookv.openorder(owner='merchantxpro', order_side='buy', pay_methods=["alipay", "wechat"],
                                         va_quantity="10.000000 USDTTRC", va_price="2.1000 CNY",
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

def test_pauseorder(): otcbookv.pauseorder(
    owner='merchantx', order_side='buy', order_id=75, suber='merchantx')


def test_processdeal2(): otcbookv.processdeal(account='merchantxpro', account_type=2, deal_id=2042, action=2, session_msg='接单',
                                             suber='merchantxpro')


def test_processdeal3(): otcbookv.processdeal(account='555544441111', account_type=3, deal_id=2042, action=3, session_msg='用户转币',
                                             suber='555544441111')


def test_processdeal4(): otcbookv.processdeal(account='merchantxpro', account_type=2, deal_id=2042, action=4, session_msg='商户转款',
                                             suber='merchantxpro')                                             

def test_processdeal(): otcbookv.processdeal(account='user1', account_type=1, deal_id=1, action=1, session_msg='x',
                                             suber='user1')

def test_resetdeal(): otcbookv.resetdeal(
    account='user1', deal_id=1, session_msg='x', suber='user1')


def test_resumeorder(): otcbookv.resumeorder(
    owner='user1', order_side='user1', order_id=1, suber='user1')


def test_setblacklist(): otcbookv.setblacklist(
    account='user1', duration_second=1, suber='user1')


def test_setconf(): otcbookv.setconf(
    conf_contract='otcconf1', suber=otcbookv.contract)


log = logging.getLogger(__name__)


def test_setmerchant():
    otcbookv.setmerchant(merchant='mk', status=9, merchant_name='测试商户user1',
                         merchant_detail='set_detail', email='setxxx@qq.com', memo='setmemo', reject_reason="set拒绝", by_force="true", suber='ad').assetResponsePass()


def test_remerchant():
    otcbookv.remerchant(merchant='555544441111', status=1, merchant_name='商家5555',
                        merchant_detail='detail', email='xxx@qq.com', memo='', reject_reason="re申请", suber='555544441111')


def test_stakechanged(): otcbookv.stakechanged(
    account='user1', quantity="0.10000000 AMAX", memo='x', suber='user1')


def test_startarbit(): otcbookv.startarbit(account='user1', account_type=3, deal_id=1009,suber='user1')


def test_enbmerchant(): otcbookv.enbmerchant(
    owner='merchantxpro', stats=14, suber='ad')


def test_withdraw(): otcbookv.withdraw(
    owner='merchantxpro', quantity="10.000000 MUSDT", suber='merchantxpro')


def test_merchant_Sctipt():
    with open('./pythonProject1/otcbookvcase/data.csv', encoding='utf-8-sig') as f:
        for row in csv.reader(f, skipinitialspace=True):
            account = row[1]
            name = row[3]
            email = row[5]
            print(account, name, email)
            # print(f"""$mcli push action meta.book setmerchant '["meta.balance","{account}","{name}","必须为本人账号实名转账\\n转账时请不要备注任何信息\\n请不要设置为延迟到账\\n黑钱绕道，发现必究报警","{email}",""]' -p meta.balance""")
            # print(f"""$mcli  push action meta.book enbmerchant '["{account}",11]'  -p meta.balance""")
            body = "amcli  -u http://exp1.nchain.me:8889 get account  "+account
            # body = f"amcli  -u http://exp1.nchain.me:8889  get table meta.book meta.book merchants -L {account} -U {account}"
            # print(body)
            res = os.popen(body).read()
            # print(res)
            if ("does not exist" not in res):
                print(account)
