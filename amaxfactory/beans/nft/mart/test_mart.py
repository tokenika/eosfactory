import random

from nft.mart.mart import mart as m
from nft.ntoken.ntoken import ntoken as n
from amax.cnydtoken.cnyd import CNYD
from xchain.mtoken.mtoken import Mtoken
from amax.amaxtoken.amax import AMAX
amax = AMAX()

mtoken = Mtoken()
cnyd = CNYD()
ntoken = n()
ntoken1 = n()
mart = m()


class TestMart:

    def test_sell(self):
        ntoken1.contract = 'ntoken1'
        ntoken.transfer(fromx='user1', to=mart.contract, assets=[
                        [2, [200000, 7]]], memo='', suber='user1').assetResponseFail()
        ntoken.transfer(fromx='user1', to=mart.contract, assets=[
                        [2, [200000, 7]]], memo='xx', suber='user1').assetResponseFail()

        ntoken.transfer(fromx='user1', to=mart.contract, assets=[[2, [200000, 7]], [2, [200000, 7]]], memo='10',
                        suber='user1').assetResponseFail()
        ntoken.transfer(fromx='user1', to=mart.contract, assets=[[2, [200000, 7]]], memo='-1',
                        suber='user1').assetResponseFail()
        # ntoken.transfer(fromx='user1', to=mart.contract, assets=[[2, [200000, 7]]], memo='1/100000000',
        #                 suber='user1').assetResponseFail()
        ntoken1.transfer(fromx='user1', to=mart.contract, assets=[[1, [2222, 0]]], memo='1',
                         suber='user1').assetResponsePass()
        ntoken1.transfer(fromx='user1', to=mart.contract, assets=[[1, [2222, 0]]], memo='10',
                         suber='user1').assetResponsePass()
        assert mart.getLastRow('2222', 'sellorders')['id'] == 0

    def test_buy(self):
        ntoken.transfer(fromx='user1', to=mart.contract, assets=[[2, [200000, 7]]], memo='1',
                        suber='user1').assetResponsePass()
        id = mart.getLastRow('200000', 'sellorders')['id']
        mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="20.000000 MUSDT",
                        memo=f'200000:{id + 1}:10', suber='merchantx').assetResponseFail()
        mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="20.000000 MUSDT",
                        memo=f'200000:{id}:-10', suber='merchantx').assetResponseFail()
        mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="20.000000 MUSDT", memo=f'20110:{id}:10',
                        suber='merchantx').assetResponseFail()
        # mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="20.000000 MUSDT", memo=f'200000:{id}:10/1/1',
        #                 suber='merchantx').assetResponseFail()
        # mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="20.000000 MUSDT", memo=f'200000:{id}:10/x',
        #             suber='merchantx').assetResponseFail()
        mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="1.000000 METH", memo=f'200000:{id}:1',
                        suber='merchantx').assetResponseFail()
        amax.transfer(fromx='user1', to=mart.contract, quantity="1.000000 MUSDT", memo=f'200000:{id}:1',
                      suber='user1').assetResponsePass()
        assert mart.getLastRow('200000', 'sellorders')['frozen'] == 2

    def test_buy2(self):
        # buy_count 向下取整
        # price >sell_price 数量小于卖单数量 以sell_price*buy_count成交，多余的钱退回
        ntoken.transfer(fromx='user1', to=mart.contract, assets=[[2, [200000, 7]]], memo='10000000',
                        suber='user1').assetResponsePass()
        id = mart.getLastRow('200000', 'sellorders')['id']
        mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="19.900000 MUSDT",
                        memo=f'200000:{id}:11000000', suber='merchantx').assetResponsePass()

    def test_buy3(self):
        # price >sell_price 数量等于卖单数量 以sell_price*count成交，多余的钱退回
        ntoken.transfer(fromx='user1', to=mart.contract, assets=[[2, [200000, 7]]], memo='10000000',
                        suber='user1').assetResponsePass()
        id = mart.getLastRow('200000', 'sellorders')['id']
        mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="23.000000 MUSDT",
                        memo=f'200000:{id}:11000000', suber='merchantx').assetResponsePass()

    def test_buy4(self):
        # price >sell_price 数量大于单数量 以sell_price*sell_count成交，多余的钱退回
        ntoken.transfer(fromx='user1', to=mart.contract, assets=[[2, [200000, 7]]], memo='10000000',
                        suber='user1').assetResponsePass()
        id = mart.getLastRow('200000', 'sellorders')['id']
        mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="33.000000 MUSDT",
                        memo=f'200000:{id}:11000000', suber='merchantx').assetResponsePass()

    def test_buy5(self):
        # buy_count 向下取整
        # price =sell_price 数量小于卖单数量 以price*buy_count 成交
        ntoken.transfer(fromx='user1', to=mart.contract, assets=[[2, [200000, 7]]], memo='10000000',
                        suber='user1').assetResponsePass()
        id = mart.getLastRow('200000', 'sellorders')['id']
        mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="10.000000 MUSDT", memo=f'200000:{id}:10000000',
                        suber='merchantx').assetResponsePass()

    def test_buy6(self):
        # price =sell_price 数量等于卖单数量 以price*count 成交
        ntoken.transfer(fromx='user1', to=mart.contract, assets=[[2, [200000, 7]]], memo='10000000',
                        suber='user1').assetResponsePass()
        id = mart.getLastRow('200000', 'sellorders')['id']
        mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="10.000000 MUSDT", memo=f'200000:{id}:10000000',
                        suber='merchantx').assetResponsePass()

    def test_buy7(self):
        # price =sell_price 数量大于单数量 以price*sell_count 成交
        ntoken.transfer(fromx='user1', to=mart.contract, assets=[[2, [200000, 7]]], memo='10000000',
                        suber='user1').assetResponsePass()
        id = mart.getLastRow('200000', 'sellorders')['id']
        mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="30.000000 MUSDT", memo=f'200000:{id}:10000000',
                        suber='merchantx').assetResponsePass()

    def test_buy8(self):
        # price =sell_price 数量大于单数量 以price*sell_count 成交
        ntoken.transfer(fromx='user1', to=mart.contract, assets=[[2, [200000, 7]]], memo='10000000',
                        suber='user1').assetResponsePass()
        id = mart.getLastRow('200000', 'sellorders')['id']
        mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="5.000000 MUSDT", memo=f'200000:{id}:5000000',
                        suber='merchantx').assetResponsePass()
        mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="10.000000 MUSDT", memo=f'200000:{id}:5000000',
                        suber='merchantx').assetResponsePass()
        mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="15.000000 MUSDT", memo=f'200000:{id}:5000000',
                        suber='merchantx').assetResponsePass()

    def test_buy9(self):
        # 转账金额小于价格
        ntoken.transfer(fromx='user1', to=mart.contract, assets=[[2, [200000, 7]]], memo='1999',
                        suber='user1').assetResponsePass()
        id = mart.getLastRow('200000', 'sellorders')['id']
        mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="0.001999 MUSDT", memo=f'200000:{id}:1999',
                        suber='merchantx').assetResponsePass()

    def test_buy10(self):
        # 小数测试
        price = random.randint(100, 99999999)

        bid = mart.getLastRow(mart.contract, 'buyerbids')['id']

        ntoken.transfer(fromx='user1', to=mart.contract, assets=[[2, [200000, 7]]], memo=f'{price}',
                        suber='user1').assetResponsePass()
        id = mart.getLastRow('200000', 'sellorders')['id']
        mtoken.transfer(fromx='merchantx', to=mart.contract, quantity=f"{price/1000000} MUSDT", memo=f'200000:{id}:{price}',
                        suber='merchantx').assetResponsePass()
        bid2 = mart.getLastRow(mart.contract, 'buyerbids')['id']
        assert bid == bid2

    def test_buy11(self):
        # 大额测试
        bid = mart.getLastRow(mart.contract, 'buyerbids')['id']

        ntoken.transfer(fromx='user1', to=mart.contract, assets=[[2, [200000, 7]]], memo='1000000000000',
                        suber='user1').assetResponsePass()
        id = mart.getLastRow('200000', 'sellorders')['id']
        mtoken.transfer(fromx='ad', to=mart.contract, quantity="1000000.000000 MUSDT", memo=f'200000:{id}:1000000000000',
                        suber='ad').assetResponsePass()
        bid2 = mart.getLastRow(mart.contract, 'buyerbids')['id']
        assert bid == bid2

    def test_takebuyorder0(self):
        ntoken.transfer(fromx='user1', to=mart.contract, assets=[
                        [2, [200000, 7]]], memo='10000000', suber='user1').assetResponsePass()
        id = mart.getLastRow('200000', 'sellorders')['id']

        mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="18.000000 MUSDT",
                        memo=f'200000:{id}:9000000', suber='merchantx').assetResponsePass()

        bid = mart.getLastRow(mart.contract, 'buyerbids')['id']
        mart.takebuybid(issuer='ad', token_id=200000,
                        buy_order_id=bid, suber='ad').assetResponseFail()
        mart.takebuybid(issuer='user1', token_id=200000,
                        buy_order_id=bid, suber='ad').assetResponseFail()
        mart.takebuybid(issuer='user1', token_id=200000,
                        buy_order_id=bid+1, suber='user1').assetResponseFail()
        mart.takebuybid(issuer='user1', token_id=2000001,
                        buy_order_id=bid, suber='user1').assetResponseFail()

    def test_takebuyorder1(self):
        # sell_count>buy_count
        ntoken.transfer(fromx='user1', to=mart.contract, assets=[
                        [3, [200000, 7]]], memo='10000000', suber='user1').assetResponsePass()
        id = mart.getLastRow('200000', 'sellorders')['id']

        mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="9.000000 MUSDT",
                        memo=f'200000:{id}:9000000', suber='merchantx').assetResponsePass()

        bid = mart.getLastRow(mart.contract, 'buyerbids')['id']
        mart.takebuybid(issuer='user1', token_id=200000,
                        buy_order_id=bid, suber='user1').assetResponsePass()

    def test_takebuyorder2(self):
        # sell_count=buy_count
        ntoken.transfer(fromx='user1', to=mart.contract, assets=[
                        [2, [200000, 7]]], memo='10000000', suber='user1').assetResponsePass()
        id = mart.getLastRow('200000', 'sellorders')['id']

        mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="18.000000 MUSDT",
                        memo=f'200000:{id}:9000000', suber='merchantx').assetResponsePass()

        bid = mart.getLastRow(mart.contract, 'buyerbids')['id']
        mart.takebuybid(issuer='user1', token_id=200000,
                        buy_order_id=bid, suber='user1').assetResponsePass()

    def test_takebuyorder3(self):
        # sell_count<buy_count
        ntoken.transfer(fromx='user1', to=mart.contract, assets=[[1, [200000, 7]]], memo='10000000',
                        suber='user1').assetResponsePass()
        id = mart.getLastRow('200000', 'sellorders')['id']

        mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="18.000000 MUSDT", memo=f'200000:{id}:9000000',
                        suber='merchantx').assetResponsePass()

        bid = mart.getLastRow(mart.contract, 'buyerbids')['id']
        mart.takebuybid(issuer='user1', token_id=200000,
                        buy_order_id=bid, suber='user1').assetResponsePass()

    def test_takebuyorder4(self):
        # 大额测试
        ntoken.transfer(fromx='user1', to=mart.contract, assets=[[2, [200000, 7]]], memo='1000000000001',
                        suber='user1').assetResponsePass()
        id = mart.getLastRow('200000', 'sellorders')['id']

        mtoken.transfer(fromx='ad', to=mart.contract, quantity="1000000.000000 MUSDT",
                        memo=f'200000:{id}:1000000000000', suber='ad').assetResponsePass()

        bid = mart.getLastRow(mart.contract, 'buyerbids')['id']
        mart.takebuybid(issuer='user1', token_id=200000,
                        buy_order_id=bid, suber='user1').assetResponsePass()

    def test_cancelorder(self):
        ntoken.transfer(fromx='user1', to=mart.contract, assets=[[2, [200000, 7]]], memo='10000000',
                        suber='user1').assetResponsePass()
        id = mart.getLastRow('200000', 'sellorders')['id']
        mart.cancelorder(maker='ad', token_id=200000, order_id=id,  suber='ad')
        mart.cancelorder(maker='user1', token_id=200000,
                         order_id=id,  suber='ad').assetResponseFail()
        mart.cancelorder(maker='user1', token_id=200000,
                         order_id=id+1, suber='user1').assetResponseFail()
        mart.cancelorder(maker='user1', token_id=200001,
                         order_id=id, suber='user1').assetResponseFail()

        mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="10.000000 MUSDT", memo=f'200000:{id}:10000000',
                        suber='merchantx').assetResponsePass()
        mart.cancelorder(maker='user1', token_id=200000,
                         order_id=id,  suber='user1').assetResponsePass()

        ntoken.transfer(fromx='user1', to=mart.contract, assets=[[2, [200000, 7]]], memo='10',
                        suber='user1').assetResponsePass()
        id += 1
        mart.cancelorder(maker='user1', token_id=200000,
                         order_id=id, suber='user1').assetResponsePass()

    def test_cancelbid(self):
        ntoken.transfer(fromx='user1', to=mart.contract, assets=[[2, [200000, 7]]], memo='10000000',
                        suber='user1').assetResponsePass()
        id = mart.getLastRow('200000', 'sellorders')['id']
        mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="18.000000 MUSDT", memo=f'200000:{id}:9000000',
                        suber='merchantx').assetResponsePass()
        bid = mart.getLastRow(mart.contract, 'buyerbids')['id']
        mart.cancelbid(buyer='ad', bid_id=bid, suber='ad').assetResponseFail()
        mart.cancelbid(buyer='merchantx', bid_id=bid,
                       suber='ad').assetResponseFail()
        mart.cancelbid(buyer='merchantx', bid_id=bid+1,
                       suber='merchantx').assetResponseFail()
        mart.cancelbid(buyer='merchantx', bid_id=bid,
                       suber='merchantx').assetResponsePass()

    # def test_init(self): mart.init(suber=mart.contract)

    def test_getsellorders(self):
        print(mart.getLastRow('200000', 'sellorders'))

    def test_getbuyerbids(self):
        print(mart.getLastRow(mart.contract, 'buyerbids'))
