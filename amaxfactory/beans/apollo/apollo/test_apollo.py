import random
from re import sub
from apollo.apollo.apollo import Apollo
from nft.ntoken.ntoken import ntoken as n
from amax.cnydtoken.cnyd import CNYD
from xchain.mtoken.mtoken import Mtoken
from amax.amaxtoken.amax import AMAX
amax = AMAX()

mtoken = Mtoken()
cnyd = CNYD()
ntoken = n()
ntoken1 = n()
apollo = Apollo()


class TestMart:

    def test_sell(self):
        ntoken1.contract = 'ntoken1'
        ntoken.transfer(fromx='user1', to=apollo.contract, assets=[
                        [2, [1, 0]]], memo='', suber='user1').assetResponseFail()
        ntoken.transfer(fromx='user1', to=apollo.contract, assets=[
                        [2, [1, 0]]], memo='xx', suber='user1').assetResponseFail()

        ntoken.transfer(fromx='user1', to=apollo.contract, assets=[[1, [1, 0]], [2, [1, 0]]], memo='10',
                        suber='user1').assetResponseFail()
        ntoken.transfer(fromx='user1', to=apollo.contract, assets=[[2, [1, 0]]], memo='-1',
                        suber='user1').assetResponseFail()
        # ntoken.transfer(fromx='user1', to=mart.contract, assets=[[2, [200000, 7]]], memo='1/100000000',
        #                 suber='user1').assetResponseFail()
        last_id = apollo.getLastRow(apollo.contract,'global')['last_sell_order_idx']

        ntoken1.transfer(fromx='user1', to=apollo.contract, assets=[[1, [2222, 0]]], memo='1',
            suber='user1').assetResponsePass()
        ntoken1.transfer(fromx='user1', to=apollo.contract, assets=[[1, [2222, 0]]], memo='10',
            suber='user1').assetResponsePass()
        last_id2 = apollo.getLastRow(apollo.contract,'global')['last_sell_order_idx']

        assert last_id == last_id2

    def test_setorderfee(self):
        last_id = apollo.getLastRow(apollo.contract,'global')['last_sell_order_idx']
        apollo.setorderfee(order_id=last_id,start_at='2022-08-20T011:20:00.000',end_at='2022-08-29T08:00:00.000',fee='0.100000 MUSDT',suber=apollo.contract).assetResponsePass()
        apollo.setorderfee(order_id=last_id,start_at='2022-08-20T011:20:00.000',end_at='2022-08-29T08:00:00.000',fee='0.000000 MUSDT',suber=apollo.contract).assetResponsePass()
        apollo.setorderfee(order_id=last_id,start_at='2022-08-20T011:20:00.000',end_at='2022-08-29T08:00:00.000',fee='-1.000000 MUSDT',suber=apollo.contract).assetResponseFail()
        apollo.setorderfee(order_id=last_id,start_at='2022-08-20T011:20:00.000',end_at='2022-08-29T08:00:00.000',fee='-1.000000 MUSDT',suber='ad').assetResponseFail()


    def test_buy(self):
        # ntoken.transfer(fromx='ad', to=apollo.contract, assets=[[10, [1, 0]]], memo='2000000',
                        # suber='ad').assetResponsePass()
        # apollo.setorderfee(order_id=last_id,start_at='2022-08-01T10:34:00.000',end_at='2022-08-29T08:00:00.000',fee='0.100000 MUSDT',suber=apollo.contract).assetResponsePass()

        id = apollo.getLastRow(apollo.contract,'global')['last_sell_order_idx']
        mtoken.transfer(fromx='merchantx', to=apollo.contract, quantity="2.100000 MUSDT",
                        memo=f'200000:{id + 1}:10', suber='merchantx').assetResponseFail()
        mtoken.transfer(fromx='merchantx', to=apollo.contract, quantity="2.100000 MUSDT",
                        memo=f'200000:{id}:-10', suber='merchantx').assetResponseFail()
        mtoken.transfer(fromx='merchantx', to=apollo.contract, quantity="2.100000 MUSDT", memo=f'20110:{id}:10',
                        suber='merchantx').assetResponseFail()
        # mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="20.000000 MUSDT", memo=f'200000:{id}:10/1/1',
        #                 suber='merchantx').assetResponseFail()
        # mtoken.transfer(fromx='merchantx', to=mart.contract, quantity="20.000000 MUSDT", memo=f'200000:{id}:10/x',
        #             suber='merchantx').assetResponseFail()
        mtoken.transfer(fromx='merchantx', to=apollo.contract, quantity="2.100000 METH", memo=f'1:{id}:1',
                        suber='merchantx').assetResponseFail()
        mtoken.transfer(fromx='merchantx', to=apollo.contract, quantity="210.000000 MUSDT", memo=f'1:{id}:100',
                        suber='merchantx').assetResponseFail()
        mtoken.transfer(fromx='merchantx', to=apollo.contract, quantity="2.200000 MUSDT", memo=f'1:{id}:1',
                        suber='merchantx').assetResponseFail()
        mtoken.transfer(fromx='merchantx', to=apollo.contract, quantity="2.000000 MUSDT", memo=f'1:{id}:1',
                        suber='merchantx').assetResponseFail()
        amax.transfer(fromx='user1', to=apollo.contract, quantity="1.000000 MUSDT", memo=f'1:{id}:1',
                      suber='user1').assetResponsePass()
        assert apollo.getLastRow('200000', 'sellorders')['frozen'] == 99

    def test_buy2(self):
        # buy_count 向下取整
        # price >sell_price 数量小于卖单数量 以sell_price*buy_count成交，多余的钱退回
        ntoken.transfer(fromx='user1', to=apollo.contract, assets=[[2, [200000, 7]]], memo='10000000',
                        suber='user1').assetResponsePass()
        id = apollo.getLastRow('200000', 'sellorders')['id']
        mtoken.transfer(fromx='merchantx', to=apollo.contract, quantity="19.900000 MUSDT",
                        memo=f'200000:{id}:11000000', suber='merchantx').assetResponsePass()

    def test_buy3(self):
        # price >sell_price 数量等于卖单数量 以sell_price*count成交，多余的钱退回
        ntoken.transfer(fromx='user1', to=apollo.contract, assets=[[2, [200000, 7]]], memo='10000000',
                        suber='user1').assetResponsePass()
        id = apollo.getLastRow('200000', 'sellorders')['id']
        mtoken.transfer(fromx='merchantx', to=apollo.contract, quantity="23.000000 MUSDT",
                        memo=f'200000:{id}:11000000', suber='merchantx').assetResponsePass()

    def test_buy4(self):
        # price >sell_price 数量大于单数量 以sell_price*sell_count成交，多余的钱退回
        ntoken.transfer(fromx='user1', to=apollo.contract, assets=[[2, [200000, 7]]], memo='10000000',
                        suber='user1').assetResponsePass()
        id = apollo.getLastRow('200000', 'sellorders')['id']
        mtoken.transfer(fromx='merchantx', to=apollo.contract, quantity="33.000000 MUSDT",
                        memo=f'200000:{id}:11000000', suber='merchantx').assetResponsePass()

    def test_buy5(self):
        # buy_count 向下取整
        # price =sell_price 数量小于卖单数量 以price*buy_count 成交
        ntoken.transfer(fromx='user1', to=apollo.contract, assets=[[2, [200000, 7]]], memo='10000000',
                        suber='user1').assetResponsePass()
        id = apollo.getLastRow('200000', 'sellorders')['id']
        mtoken.transfer(fromx='merchantx', to=apollo.contract, quantity="10.000000 MUSDT", memo=f'200000:{id}:10000000',
                        suber='merchantx').assetResponsePass()

    def test_buy6(self):
        # price =sell_price 数量等于卖单数量 以price*count 成交
        ntoken.transfer(fromx='user1', to=apollo.contract, assets=[[2, [200000, 7]]], memo='10000000',
                        suber='user1').assetResponsePass()
        id = apollo.getLastRow('200000', 'sellorders')['id']
        mtoken.transfer(fromx='merchantx', to=apollo.contract, quantity="20.000000 MUSDT", memo=f'200000:{id}:10000000',
                        suber='merchantx').assetResponsePass()

    def test_buy7(self):
        # price =sell_price 数量大于单数量 以price*sell_count 成交
        ntoken.transfer(fromx='user1', to=apollo.contract, assets=[[2, [200000, 7]]], memo='10000000',
                        suber='user1').assetResponsePass()
        id = apollo.getLastRow('200000', 'sellorders')['id']
        mtoken.transfer(fromx='merchantx', to=apollo.contract, quantity="30.000000 MUSDT", memo=f'200000:{id}:10000000',
                        suber='merchantx').assetResponsePass()

    def test_buy8(self):
        # price =sell_price 数量大于单数量 以price*sell_count 成交
        ntoken.transfer(fromx='user1', to=apollo.contract, assets=[[2, [200000, 7]]], memo='10000000',
                        suber='user1').assetResponsePass()
        id = apollo.getLastRow('200000', 'sellorders')['id']
        mtoken.transfer(fromx='merchantx', to=apollo.contract, quantity="5.000000 MUSDT", memo=f'200000:{id}:5000000',
                        suber='merchantx').assetResponsePass()
        mtoken.transfer(fromx='merchantx', to=apollo.contract, quantity="10.000000 MUSDT", memo=f'200000:{id}:5000000',
                        suber='merchantx').assetResponsePass()
        mtoken.transfer(fromx='merchantx', to=apollo.contract, quantity="15.000000 MUSDT", memo=f'200000:{id}:5000000',
                        suber='merchantx').assetResponsePass()

    def test_buy9(self):
        # 转账金额小于价格
        ntoken.transfer(fromx='user1', to=apollo.contract, assets=[[2, [200000, 7]]], memo='1999',
                        suber='user1').assetResponsePass()
        id = apollo.getLastRow('200000', 'sellorders')['id']
        mtoken.transfer(fromx='merchantx', to=apollo.contract, quantity="0.001999 MUSDT", memo=f'200000:{id}:1999',
                        suber='merchantx').assetResponsePass()

    def test_buy10(self):
        # 小数测试
        price = random.randint(100, 99999999)

        bid = apollo.getLastRow(apollo.contract, 'buyerbids')['id']

        ntoken.transfer(fromx='user1', to=apollo.contract, assets=[[2, [200000, 7]]], memo=f'{price}',
                        suber='user1').assetResponsePass()
        id = apollo.getLastRow('200000', 'sellorders')['id']
        mtoken.transfer(fromx='merchantx', to=apollo.contract, quantity=f"{price/1000000} MUSDT", memo=f'200000:{id}:{price}',
                        suber='merchantx').assetResponsePass()
        bid2 = apollo.getLastRow(apollo.contract, 'buyerbids')['id']
        assert bid == bid2

    def test_buy11(self):
        # 大额测试
        bid = apollo.getLastRow(apollo.contract, 'buyerbids')['id']

        ntoken.transfer(fromx='user1', to=apollo.contract, assets=[[2, [200000, 7]]], memo='1000000000000',
                        suber='user1').assetResponsePass()
        id = apollo.getLastRow('200000', 'sellorders')['id']
        mtoken.transfer(fromx='ad', to=apollo.contract, quantity="1000000.000000 MUSDT", memo=f'200000:{id}:1000000000000',
                        suber='ad').assetResponsePass()
        bid2 = apollo.getLastRow(apollo.contract, 'buyerbids')['id']
        assert bid == bid2

    def test_cancelorder(self):
        ntoken.transfer(fromx='ad', to=apollo.contract, assets=[[10, [1, 0]]], memo='2000000',
                        suber='ad').assetResponsePass()
        last_id = apollo.getLastRow(apollo.contract,'global')['last_sell_order_idx']

        apollo.cancelorder('user1',1,last_id,suber='user1').assetResponseFail()
        # apollo.cancelorder('ad',11,last_id,suber='ad').assetResponseFail()
        apollo.cancelorder('ad',1,last_id+1,suber='ad').assetResponseFail()
        apollo.cancelorder('ad',11,last_id,suber='user1').assetResponseFail()
        apollo.cancelorder('ad',1,last_id,suber='ad').assetResponsePass()
        apollo.cancelorder('ad',1,last_id,suber='ad').assetResponseFail()
        


    def test_getsellorders(self):
        print(apollo.getLastRow('200000', 'sellorders'))

    def test_getbuyerbids(self):
        print(apollo.getLastRow(apollo.contract, 'buyerbids'))
