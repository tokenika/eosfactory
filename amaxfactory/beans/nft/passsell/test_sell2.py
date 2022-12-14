# from passlockcase.passlock import PASSLOCK
import time
from nft.passsell.passsell import PASSSELL
from nft.ntoken.ntoken import ntoken as n
from xchain.mtoken.mtoken import Mtoken
from kverso.vntoken.vntoken import VNTOKEN
vntoken = VNTOKEN()
mtoken = Mtoken()
ntoken = n()
passsell = PASSSELL()

# passlock = PASSLOCK()å


# 新增pass
def test_addpass():
    # owner不存在
    passsell.addpass(owner='user11111111', title='pass one', nft_symbol=[1005, 0], gift_symbol=[2002, 0],
                     price="99.000000 MUSDT", started_at="2022-10-26T02:50:00.000", ended_at="2022-11-26T06:00:00.000", buy_lock_plan_id=12, token_split_plan_id=30, suber='ad').assetResponseFail()
    # nft错误
    passsell.addpass(owner='user1', title='pass one', nft_symbol=[1005, 0], gift_symbol=[2002, 0],
                     price="99.000000 MUSDT", started_at="2022-10-26T02:50:00.000", ended_at="2022-11-26T06:00:00.000", buy_lock_plan_id=12, token_split_plan_id=30, suber='ad').assetResponseFail()
    # gift错误
    passsell.addpass(owner='user1', title='pass one', nft_symbol=[1002, 0], gift_symbol=[20020, 0],
                     price="99.000000 MUSDT", started_at="2022-10-26T02:50:00.000", ended_at="2022-11-26T06:00:00.000", buy_lock_plan_id=12, token_split_plan_id=30, suber='ad').assetResponseFail()
    # price小于0
    passsell.addpass(owner='user1', title='pass one', nft_symbol=[1002, 0], gift_symbol=[2002, 0],
                     price="-1.000000 MUSDT", started_at="2022-10-26T02:50:00.000", ended_at="2022-11-26T06:00:00.000", buy_lock_plan_id=12, token_split_plan_id=30, suber='ad').assetResponseFail()
    # price等于0
    passsell.addpass(owner='user1', title='pass one', nft_symbol=[1002, 0], gift_symbol=[2002, 0],
                     price="0.000000 MUSDT", started_at="2022-10-26T02:50:00.000", ended_at="2022-11-26T06:00:00.000", buy_lock_plan_id=12, token_split_plan_id=30, suber='ad').assetResponseFail()
    # starttime>endtime
    passsell.addpass(owner='user1', title='pass one', nft_symbol=[1002, 0], gift_symbol=[2002, 0],
                     price="5.000000 MUSDT", started_at="2022-12-26T02:50:00.000", ended_at="2022-11-26T06:00:00.000", buy_lock_plan_id=12, token_split_plan_id=30, suber='ad').assetResponseFail()

    # start time<current time    目前该case未实现
    # passsell.addpass(owner='user1', title='pass one', nft_symbol=[1002, 0], gift_symbol=[2002, 0],
    #                  price="5.000000 MUSDT", started_at="2022-8-26T02:50:00.000", ended_at="2022-11-26T06:00:00.000", buy_lock_plan_id=12, token_split_plan_id=30, suber='ad').assetResponseFail()

    # lock_plan_id不存在
    passsell.addpass(owner='user1', title='pass one', nft_symbol=[1002, 0], gift_symbol=[2002, 0],
                     price="5.000000 MUSDT", started_at="2022-8-26T02:50:00.000", ended_at="2022-11-26T06:00:00.000", buy_lock_plan_id=500055, token_split_plan_id=30, suber='ad').assetResponseFail()
    # split_plan_id不存在
    passsell.addpass(owner='user1', title='pass one', nft_symbol=[1002, 0], gift_symbol=[2002, 0],
                     price="5.000000 MUSDT", started_at="2022-8-26T02:50:00.000", ended_at="2022-11-26T06:00:00.000", buy_lock_plan_id=12, token_split_plan_id=305555, suber='ad').assetResponseFail()

    # 提交用户无权限
    passsell.addpass(owner='user1', title='pass one', nft_symbol=[1002, 0], gift_symbol=[2002, 0],
                     price="5.000000 MUSDT", started_at="2022-8-26T02:50:00.000", ended_at="2022-11-26T06:00:00.000", buy_lock_plan_id=12, token_split_plan_id=30, suber='ad102').assetResponseFail()
   
    # 参数正确, 操作人为admin
    passsell.addpass(owner='user1', title='pass one', nft_symbol=[1002, 0], gift_symbol=[2002, 0],
                     price="5.000000 MUSDT", started_at="2022-8-26T02:50:00.000", ended_at="2022-11-26T06:00:00.000", buy_lock_plan_id=12, token_split_plan_id=30, suber='ad').assetResponsePass()
    # 参数正确, 操作人为self, 合约 pa.mart
    passsell.addpass(owner='user1', title='pass one', nft_symbol=[1002, 0], gift_symbol=[2002, 0],
                     price="5.000000 MUSDT", started_at="2022-8-26T02:50:00.000", ended_at="2022-11-26T06:00:00.000", buy_lock_plan_id=12, token_split_plan_id=30, suber=passsell.contract).assetResponsePass()

# 转入nft
def test_nft_transfer():
    
    # 成功转入 
    ntoken.transfer(fromx='user1', to='pa.mart', assets=[[1,[1002,0]]], memo='refuel:4', suber='user1').assetResponsePass()

    # 转入数量为0
    ntoken.transfer(fromx='user1', to='pa.mart', assets=[[0,[1002,0]]], memo='refuel:4', suber='user1').assetResponseFail()

    # nft不存在 
    ntoken.transfer(fromx='user1', to='pa.mart', assets=[[1,[151454545,0]]], memo='refuel:4', suber='user1').assetResponseFail()

    # 非owner转入失败 
    ntoken.transfer(fromx='ad', to='pa.mart', assets=[[1,[1002,0]]], memo='refuel:4', suber='ad').assetResponseFail()

    #校验转入的nft数据
    pass_id = passsell.getLastRow(passsell.contract, "passes")['id']
    nft_total_0 = passsell.getLastRow(passsell.contract, "passes")['nft_total']['amount']
    ntoken.transfer(fromx='user1', to='pa.mart', assets=[[1,[1002,0]]], memo=f'refuel:{pass_id}', suber='user1').assetResponsePass()
    nft_total_1 = passsell.getLastRow(passsell.contract, "passes")['nft_total']['amount']  
    assert nft_total_1 - nft_total_0 == 1


# 转入gift
def test_gift_transfer():
    # 成功转入 
    vntoken.transfer(fromx='user1', to='pa.mart', assets=[[1,[2002,0]]], memo='refuel:4', suber='user1').assetResponsePass()
    # gift不存在 
    vntoken.transfer(fromx='user1', to='pa.mart', assets=[[1,[151454545,0]]], memo='refuel:4', suber='user1').assetResponseFail()
    # 非owner转入失败 
    vntoken.transfer(fromx='ad', to='pa.mart', assets=[[1,[2002,0]]], memo='refuel:4', suber='ad').assetResponseFail()


# 购买pass
def test_buypass():
    # 购买成功
    mtoken.transfer(fromx='ad', to=passsell.contract, quantity="5.000000  MUSDT",
                    memo=f'buy:4:1', suber='ad').assetResponsePass()

    # 购买价格不对
    mtoken.transfer(fromx='ad', to=passsell.contract, quantity="5.000000  MUSDT",
                    memo=f'buy:4:2', suber='ad').assetResponseFail()

    # 币种错误
    mtoken.transfer(fromx='ad', to=passsell.contract, quantity="5.000000  AMAX",
                    memo=f'buy:4:1', suber='ad').assetResponseFail()

    # memo第一个参数错误
    mtoken.transfer(fromx='ad', to=passsell.contract, quantity="5.000000  MUSDT",
                    memo=f'buy2:4:1', suber='ad').assetResponseFail()

    # memo第二个参数 passid不存在
    mtoken.transfer(fromx='ad', to=passsell.contract, quantity="5.000000  MUSDT",
                    memo=f'buy:5656565:1', suber='ad').assetResponseFail()

    # memo第三个参数 数量为0
    mtoken.transfer(fromx='ad', to=passsell.contract, quantity="5.000000  MUSDT",
                    memo=f'buy:4:0', suber='ad').assetResponseFail()

    # pass已关闭,失败
    mtoken.transfer(fromx='ad', to=passsell.contract, quantity="5.000000  MUSDT",
                    memo=f'buy:3:1', suber='ad').assetResponseFail()

    # pass已结束,失败
    mtoken.transfer(fromx='ad', to=passsell.contract, quantity="5.000000  MUSDT",
                    memo=f'buy:13:1', suber='ad').assetResponseFail()

    
    #pass未开始,失败
    # end_pass_id = passsell.addpass(owner='user1', title='pass one', nft_symbol=[1002, 0], gift_symbol=[2002, 0],
    #                                price="5.000000 MUSDT", started_at="2022-8-26T02:50:00.000", ended_at="2023-11-24T06:00:00.000", buy_lock_plan_id=12, 
    #                                token_split_plan_id=30, suber='ad').getLastRow(passsell.contract, "passes")['id']
    mtoken.transfer(fromx='ad', to=passsell.contract, quantity="5.000000  MUSDT",
                    memo=f'buy:14:1', suber='ad').assetResponseFail()

    # pass未转入nft/gift
    mtoken.transfer(fromx='ad', to=passsell.contract, quantity="5.000000  MUSDT",
                    memo=f'buy:16:1', suber='ad').assetResponseFail()


def test_demo(): 
    mtoken.transfer(fromx='ad', to=passsell.contract, quantity="5.000000  MUSDT",
                    memo=f'buy:16:1', suber='ad').assetResponseFail()
    # 参数正确, 操作人为admin
    passsell.addpass(owner='user1', title='pass one', nft_symbol=[1002, 0], gift_symbol=[2002, 0],
                     price="5.000000 MUSDT", started_at="2022-8-26T02:50:00.000", ended_at="2022-11-26T06:00:00.000", buy_lock_plan_id=12, token_split_plan_id=30, suber='ad').assetResponsePass()

    # 参数正确, 操作人为self, 合约自己
    passsell.addpass(owner='user1', title='pass one', nft_symbol=[1002, 0], gift_symbol=[2002, 0],
                     price="5.000000 MUSDT", started_at="2022-8-26T02:50:00.000", ended_at="2022-11-26T06:00:00.000", buy_lock_plan_id=12, token_split_plan_id=30, suber=passsell.contract).assetResponsePass()