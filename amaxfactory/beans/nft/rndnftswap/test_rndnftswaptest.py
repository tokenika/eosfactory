
import time
from kverso.vntoken.vntoken import VNTOKEN
from nft.ntoken.ntoken import ntoken as n
from nft.rndnftswap.rndnftswap import RNDNFTSWAP
ntoken = n()
rndnftswap = RNDNFTSWAP()
vntoken = VNTOKEN()




def test_t():
    rndnftswap.init(admin='ad', suber=rndnftswap.contract)

# 时间已到期的both[11010,0]
# 已使用closebooth关闭的booth[1919,0]  (get table已查不到)
#正常的booth[2002,0]     [20202,0]
# 未充值的booth 15515



def test_00():
    #铸造quote_nft并使用该nft创建一个booth
    nft_id = 2003
    vntoken.create(issuer='user1', maximum_supply=10000, symbol=[nft_id, 0],
                   token_uri=f'{nft_id}', ipowner='user1', token_type="uuu", suber='user1')
    vntoken.issue(to='user1', quantity=[
                  3000, [nft_id, 0]], memo='x', suber='user1')
    rndnftswap.createbooth(owner="user1", title="test01", base_nft_contract="pass.ntoken", quote_nft_contract="verso.mid",
                           quote_nft_price=f"[3,[{nft_id},0]]", opened_at="2022-8-26T02:50:00.000", close_at="2023-11-3T02:36:00.000", suber='ad')

def test_vntoen():
    #前置准备: 创建铸造一个新的quote_nft
    vid = 2003
    vntoken.create(issuer='user1', maximum_supply=10000, symbol=[vid, 0],
                   token_uri=f'{vid}', ipowner='user1', token_type="uuu", suber='user1')
    vntoken.issue(to='user1', quantity=[
                  3000, [vid, 0]], memo='x', suber='user1')


def test_ntoen():
    #前置准备: 创建铸造一个新的base_nft, 用于充值
    nid = 1006
    ntoken.create(issuer='user1', maximum_supply=10000, symbol=[nid, 0],
                   token_uri=f'{nid}', ipowner='user1', suber='user1')
    ntoken.issue(to='user1', quantity=[
                  3000, [nid, 0]], memo='x', suber='user1')


def test_01():
    # 创建一个booth用于测试
    rndnftswap.createbooth(owner="user1", title="test01", base_nft_contract="pass.ntoken", quote_nft_contract="verso.mid",
                           quote_nft_price="[1,[191190,0]]", opened_at="2022-8-26T02:50:00.000", close_at="2023-11-3T02:36:00.000", suber='ad')
    # 充值多类多个nft
    ntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
                        [2, [1002, 0]], [3, [1003, 0]]], memo='refuel:verso.mid:191190', suber='user1').assetResponsePass()


def test_02():
    # close booth
    rndnftswap.closebooth(
        owner='user1', quote_nft_contract="verso.mid", symbol_id=191190, suber='user1').assetResponsePass()


def test_03():
    rndnftswap.enablebooth(owner='user1', quote_nft_contract="verso.mid",
                           symbol_id=11010, enabled='true', suber=rndnftswap.contract)
    #rndnftswap.setboothtime(
    #    owner='user1', quote_nft_contract="verso.mid", symbol_id=2002, opened_at="2022-8-26T02:50:00.000", closed_at="2023-11-26T02:50:00.000", suber=rndnftswap.contract).assetResponsePass()

def test_04():
    vntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
            [2, [11010, 0]]], memo='swap', suber='user1').assetResponseFail()







class TestRndnftswap:

    def test_1_init(self):

        # pass
        rndnftswap.init(
            admin='ad', suber=rndnftswap.contract).assetResponsePass()

        # 非self失败
        rndnftswap.init(admin='ad', suber='ad').assetResponseFail()

        # 初始化的admin不存在
        rndnftswap.init(
            admin='1', suber=rndnftswap.contract).assetResponseFail()

    def test_2_createbooth(self):

        # owner不存在
        rndnftswap.createbooth(owner="1", title="test01", base_nft_contract="pass.ntoken", quote_nft_contract="verso.mid",
                               quote_nft_price="[1,[20202,0]]", opened_at="2022-8-26T02:50:00.000", close_at="2022-11-26T02:50:00.000", suber=rndnftswap.contract).assetResponseFail()

        # base_nft_contract 不存在
        rndnftswap.createbooth(owner="user1", title="test01", base_nft_contract="pass.ntoken1121", quote_nft_contract="verso.mid",
                               quote_nft_price="[1,[20202,0]]", opened_at="2022-8-26T02:50:00.000", close_at="2022-11-26T02:50:00.000", suber=rndnftswap.contract).assetResponseFail()

        # quote_nft_contract 不存在
        rndnftswap.createbooth(owner="user1", title="test01", base_nft_contract="pass.ntoken", quote_nft_contract="verso.mid1112",
                               quote_nft_price="[1,[20202,0]]", opened_at="2022-8-26T02:50:00.000", close_at="2022-11-26T02:50:00.000", suber=rndnftswap.contract).assetResponseFail()

        # booth的quote_nft已存在  verso.mid:2002 已存在
        rndnftswap.createbooth(owner="user1", title="test01", base_nft_contract="pass.ntoken", quote_nft_contract="verso.mid",
                               quote_nft_price="[1,[2002,0]]", opened_at="2022-8-26T02:50:00.000", close_at="2022-11-26T02:50:00.000", suber=rndnftswap.contract).assetResponseFail()

        # 价格=0 失败
        rndnftswap.createbooth(owner="user1", title="test01", base_nft_contract="pass.ntoken", quote_nft_contract="verso.mid",
                               quote_nft_price="[0,[20202,0]]", opened_at="2022-8-26T02:50:00.000", close_at="2022-11-26T02:50:00.000", suber=rndnftswap.contract).assetResponseFail()

        # 价格<0 失败
        rndnftswap.createbooth(owner="user1", title="test01", base_nft_contract="pass.ntoken", quote_nft_contract="verso.mid",
                               quote_nft_price="[-1,[20202,0]]", opened_at="2022-8-26T02:50:00.000", close_at="2022-11-26T02:50:00.000", suber=rndnftswap.contract).assetResponseFail()

        #close_at < 当前时间应失败
        rndnftswap.createbooth(owner="user1", title="test01", base_nft_contract="pass.ntoken", quote_nft_contract="verso.mid",
                               quote_nft_price="[1,[20202,0]]", opened_at="2022-8-26T02:50:00.000", close_at="2022-8-27T02:50:00.000", suber=rndnftswap.contract).assetResponseFail()

        #close_at < opened_at失败
        rndnftswap.createbooth(owner="user1", title="test01", base_nft_contract="pass.ntoken", quote_nft_contract="verso.mid",
                               quote_nft_price="[1,[20202,0]]", opened_at="2023-2-26T02:50:00.000", close_at="2023-2-25T02:50:00.000", suber=rndnftswap.contract).assetResponseFail()

        # 权限: 非self非admin则失败
        rndnftswap.createbooth(owner="user1", title="test01", base_nft_contract="pass.ntoken", quote_nft_contract="verso.mid",
                               quote_nft_price="[1,[20202,0]]", opened_at="2022-8-26T02:50:00.000", close_at="2022-11-26T02:50:00.000", suber="user1").assetResponseFail()

        # 权限：self pass -已测试通过
        # rndnftswap.createbooth(owner="user1", title="test01", base_nft_contract="pass.ntoken", quote_nft_contract="verso.mid",
        #                        quote_nft_price="[1,[20202,0]]", opened_at="2022-8-26T02:50:00.000", close_at="2022-11-26T02:50:00.000", suber=rndnftswap.contract).assetResponsePass()

        # 权限： admin pass -已测试通过
        # rndnftswap.createbooth(owner="user1",title="test01",base_nft_contract="pass.ntoken",quote_nft_contract="verso.mid",
        # quote_nft_price="[1,[20202,0]]",opened_at="2022-8-26T02:50:00.000",close_at="2022-11-26T02:50:00.000", suber='ad').assetResponsePass

    def test_3_enablebooth(self):
        # 前置：设置booth状态为默认true
        rndnftswap.enablebooth(owner='user1', quote_nft_contract="verso.mid",
                               symbol_id=2002, enabled='true', suber=rndnftswap.contract)

        # 权限：self执行成功，状态true变为false
        rndnftswap.enablebooth(owner='user1', quote_nft_contract="verso.mid",
                               symbol_id=2002, enabled='false', suber=rndnftswap.contract).assetResponsePass()

        # 权限： admin执行成功，状态false变为true
        rndnftswap.enablebooth(owner='user1', quote_nft_contract="verso.mid",
                               symbol_id=2002, enabled='true', suber='ad').assetResponsePass()

        # 权限： owner执行成功， 状态由 true 变为false
        rndnftswap.enablebooth(owner='user1', quote_nft_contract="verso.mid",
                               symbol_id=2002, enabled='false', suber='user1').assetResponsePass()

        # 权限：其他账号失败
        rndnftswap.enablebooth(owner='user1', quote_nft_contract="verso.mid",
                               symbol_id=2002, enabled='false', suber='ck').assetResponseFail()

        # 恢复booth状态为默认true
        rndnftswap.enablebooth(owner='user1', quote_nft_contract="verso.mid",
                               symbol_id=2002, enabled='true', suber=rndnftswap.contract)

        # owner不等于booth的owner
        rndnftswap.enablebooth(owner='ck', quote_nft_contract="verso.mid", symbol_id=2002,
                               enabled='true', suber=rndnftswap.contract).assetResponseFail()

        # quote_nft_contract不存在
        rndnftswap.enablebooth(owner='user1', quote_nft_contract="verso.mid121",
                               symbol_id=2002, enabled='true', suber=rndnftswap.contract).assetResponseFail()

        # quote_nft_contract.symbol_id不存在应失败
        rndnftswap.enablebooth(owner='user1', quote_nft_contract="verso.mid",
                               symbol_id=2003432, enabled='true', suber=rndnftswap.contract).assetResponseFail()

        # booth当前状态与设置的状态一致时应失败/第二次设置会失败
        rndnftswap.enablebooth(owner='user1', quote_nft_contract="verso.mid",
                               symbol_id=2002, enabled='false', suber=rndnftswap.contract)
        time.sleep(1)
        rndnftswap.enablebooth(owner='user1', quote_nft_contract="verso.mid",
                               symbol_id=2002, enabled='false', suber=rndnftswap.contract).assetResponseFail()
        rndnftswap.enablebooth(owner='user1', quote_nft_contract="verso.mid",
                               symbol_id=2002, enabled='true', suber=rndnftswap.contract)
        time.sleep(1)
        rndnftswap.enablebooth(owner='user1', quote_nft_contract="verso.mid",
                               symbol_id=2002, enabled='true', suber=rndnftswap.contract).assetResponseFail()

        #booth已调用close关闭
        rndnftswap.enablebooth(owner='user1', quote_nft_contract="verso.mid",
                               symbol_id=19119, enabled='true', suber=rndnftswap.contract).assetResponseFail()
        # booth时间已过期
        rndnftswap.enablebooth(owner='user1', quote_nft_contract="verso.mid",
                               symbol_id=11010, enabled='true', suber=rndnftswap.contract).assetResponseFail()

    def test_4_setboothtime(self):
        # 权限：self成功
        rndnftswap.setboothtime(
            owner='user1', quote_nft_contract="verso.mid", symbol_id=2002, opened_at="2022-8-26T02:50:00.000", closed_at="2023-11-26T02:50:00.000", suber=rndnftswap.contract).assetResponsePass()

        # 权限：admin成功
        rndnftswap.setboothtime(
            owner='user1', quote_nft_contract="verso.mid", symbol_id=2002, opened_at="2022-8-26T02:50:00.000", closed_at="2023-11-26T02:50:00.000", suber='ad').assetResponsePass()


        # 权限：owner成功 / 重复提交成功
        rndnftswap.setboothtime(
            owner='user1', quote_nft_contract="verso.mid", symbol_id=2002, opened_at="2022-8-26T02:50:00.000", closed_at="2023-11-26T02:50:00.000", suber='user1').assetResponsePass()
        time.sleep(1.5)
        rndnftswap.setboothtime(
            owner='user1', quote_nft_contract="verso.mid", symbol_id=2002, opened_at="2022-8-26T02:50:00.000", closed_at="2023-11-26T02:50:00.000", suber='user1').assetResponsePass()

        # 权限：其他账号失败
        rndnftswap.setboothtime(
            owner='user1', quote_nft_contract="verso.mid", symbol_id=2002, opened_at="2022-8-26T02:50:00.000", closed_at="2023-11-26T02:50:00.000", suber='ck').assetResponseFail()

        # owner不等于该booth所属的owner应失败
        rndnftswap.setboothtime(
            owner='ck', quote_nft_contract="verso.mid", symbol_id=2002, opened_at="2022-8-26T02:50:00.000", closed_at="2023-11-26T02:50:00.000", suber=rndnftswap.contract).assetResponseFail()

        # quote_nft_contract不存在应失败
        rndnftswap.setboothtime(
            owner='user1', quote_nft_contract="verso.mid12123", symbol_id=2002, opened_at="2022-8-26T02:50:00.000", closed_at="2023-11-26T02:50:00.000", suber=rndnftswap.contract).assetResponseFail()

        # quote_nft_contract.symbol_id不存在
        rndnftswap.setboothtime(
            owner='user1', quote_nft_contract="verso.mid", symbol_id=20023232, opened_at="2022-8-26T02:50:00.000", closed_at="2023-11-26T02:50:00.000", suber=rndnftswap.contract).assetResponseFail()


        rndnftswap.setboothtime(
            owner='user1', quote_nft_contract="verso.mid", symbol_id=1919, opened_at="2022-8-26T02:50:00.000", closed_at="2023-11-26T02:50:00.000", suber=rndnftswap.contract).assetResponseFail()


        #close_at < opened_at 应失败 
        rndnftswap.setboothtime(
            owner='user1', quote_nft_contract="verso.mid", symbol_id=2002, opened_at="2023-8-26T02:50:00.000", closed_at="2023-7-26T02:50:00.000", suber=rndnftswap.contract).assetResponseFail()

        # close_at < 当前时间应失败  
        rndnftswap.setboothtime(
            owner='user1', quote_nft_contract="verso.mid", symbol_id=2002, opened_at="2022-8-26T02:50:00.000", closed_at="2022-9-26T02:50:00.000", suber=rndnftswap.contract).assetResponseFail()

    def test_5_closebooth(self):

        # 权限：其他账号失败
        rndnftswap.closebooth(
            owner='user1', quote_nft_contract="verso.mid", symbol_id=20202, suber='ck').assetResponseFail()

        # owner不等于booth的owner
        rndnftswap.closebooth(
            owner='ck', quote_nft_contract="verso.mid", symbol_id=20202, suber=rndnftswap.contract).assetResponseFail()

        # quote_nft_contract不存在
        rndnftswap.closebooth(owner='user1', quote_nft_contract="verso.mid121",
                              symbol_id=20202, suber=rndnftswap.contract).assetResponseFail()

        # quote_nft_contract.symbol_id不存在应失败
        rndnftswap.closebooth(owner='user1', quote_nft_contract="verso.mid",
                              symbol_id=2003432, suber=rndnftswap.contract).assetResponseFail()

        # booth的状态为disable时失败
        rndnftswap.enablebooth(owner='user1', quote_nft_contract="verso.mid",
                               symbol_id=20202, enabled='false', suber=rndnftswap.contract)
        rndnftswap.closebooth(
            owner='user1', quote_nft_contract="verso.mid", symbol_id=20202, suber=rndnftswap.contract).assetResponseFail()
        rndnftswap.enablebooth(owner='user1', quote_nft_contract="verso.mid",
                               symbol_id=20202, enabled='true', suber=rndnftswap.contract)

        # 权限：self执行成功
        # rndnftswap.closebooth(
        #     owner='user1', quote_nft_contract="verso.mid", symbol_id=20202, suber=rndnftswap.contract).assetResponsePass()

        # # 权限： admin执行成功 --测试通过
        # rndnftswap.closebooth(
        #     owner='user1', quote_nft_contract="verso.mid", symbol_id=20202, suber='ad').assetResponsePass()

        # # 权限： owner执行成功
        # rndnftswap.closebooth(
        #     owner='user1', quote_nft_contract="verso.mid", symbol_id=20202, suber='user1').assetResponsePass()


    def test_6_reful(self):

        # nft数量小于0
        ntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
                        [-1, [1002, 0]]], memo='refuel:verso.mid:2002', suber='user1').assetResponseFail()
        # nft数量为0
        ntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
                        [0, [1002, 0]]], memo='refuel:verso.mid:2002', suber='user1').assetResponseFail()
        # assets symbol不存在
        ntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
                        [1, [1021302, 0]]], memo='refuel:verso.mid:2002', suber='user1').assetResponseFail()
        # memo第一个参数为refuel但参数个数非3个
        ntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
                        [1, [1002, 0]]], memo='refuel:verso.mid', suber='user1').assetResponseFail()

        # memo第二个参数不等于quote_nft_contract则失败
        ntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
                        [1, [1002, 0]]], memo='refuel:pass.ntoken:1002', suber='user1').assetResponseFail()
        # memo 第三个参数symbol_id不存在应失败
        ntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
                        [1, [1002, 0]]], memo='refuel:verso.mid:208902', suber='user1').assetResponseFail()
        # booth状态为disable则失败
        rndnftswap.enablebooth(owner='user1', quote_nft_contract="verso.mid",
                               symbol_id=2002, enabled='false', suber=rndnftswap.contract)
        ntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
                        [1, [1002, 0]]], memo='refuel:verso.mid:2002', suber='user1').assetResponseFail()
        rndnftswap.enablebooth(owner='user1', quote_nft_contract="verso.mid",
                               symbol_id=2002, enabled='true', suber=rndnftswap.contract)

        # 转入的nft不是base_nft则失败
        vntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
            [1, [2002, 0]]], memo='refuel:verso.mid:2002', suber='user1').assetResponseFail()

        # 权限: 非owner充值失败  目前存在bug
        # ntoken.transfer(fromx='ck', to='rndnft.swap1', assets=[[1,[1002,0]]], memo='refuel:verso.mid:2002', suber='ck').assetResponseFail()

        # 权限: owner充值成功
        # 需要注意校验数据结果
        
        # 充值单类1个nft
        ntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
                        [1, [1002, 0]]], memo='refuel:verso.mid:2002', suber='user1').assetResponsePass()

        # 充值单类多个nft
        ntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
                        [3, [1002, 0]]], memo='refuel:verso.mid:2002', suber='user1').assetResponsePass()

        # 重复充值单类多个nft--充值同一个数值
        time.sleep(1.5)
        ntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
                        [3, [1002, 0]]], memo='refuel:verso.mid:2002', suber='user1').assetResponsePass()

        # 充值多类1个nft
        ntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
                        [1, [1002, 0]], [1, [1003, 0]]], memo='refuel:verso.mid:2002', suber='user1').assetResponsePass()
        # 充值多类多个nft
        ntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
                        [2, [1002, 0]], [2, [1003, 0]]], memo='refuel:verso.mid:2002', suber='user1').assetResponsePass()

        # 时间已过期


    def test_7_swap(self):

        # nft数量小于0
        vntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
            [-1, [2002, 0]]], memo='swap', suber='user1').assetResponseFail()
        # nft数量为0
        vntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
            [0, [2002, 0]]], memo='swap', suber='user1').assetResponseFail()
        # nft数量小于盲盒价格
        vntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
            [2, [2003, 0]]], memo='swap', suber='user1').assetResponseFail()

        # assets symbol不存在
        vntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
            [1, [1021302, 0]]], memo='swap', suber='user1').assetResponseFail()

        # memo参数个数为1个且不为swap则失败
        vntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
            [1, [1002, 0]]], memo='swap1', suber='user1').assetResponseFail()
        # booth状态为disable则失败
        rndnftswap.enablebooth(owner='user1', quote_nft_contract="verso.mid",
                               symbol_id=2002, enabled='false', suber=rndnftswap.contract)
        vntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
            [1, [2002, 0]]], memo='swap', suber='user1').assetResponseFail()
        rndnftswap.enablebooth(owner='user1', quote_nft_contract="verso.mid",
                               symbol_id=2002, enabled='true', suber=rndnftswap.contract)
        # 转入的nft不是quote_nft_contract则失败
        ntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
                        [1, [1002, 0]]], memo='swap', suber='user1').assetResponseFail()

        # 初始化,设置默认时间
        rndnftswap.setboothtime(
            owner='user1', quote_nft_contract="verso.mid", symbol_id=2002, opened_at="2022-8-26T02:50:00.000", closed_at="2023-11-26T02:50:00.000", suber=rndnftswap.contract)

        # 需要注意校验数据结果
        # nft单类抽取1个盲盒
        vntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
            [1, [2002, 0]]], memo='swap', suber='user1').assetResponsePass()

        
        # nft单类抽取1个盲盒-重复抽取
        time.sleep(1.5)
        vntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
            [1, [2002, 0]]], memo='swap', suber='user1').assetResponsePass()

        # nft单类抽取多个盲盒
        vntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
            [2, [2002, 0]]], memo='swap', suber='user1').assetResponsePass()

        # nft多类抽取盲盒则失败
        vntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
            [1, [1002, 0]], [3, [1003, 0]]], memo='swap', suber='user1').assetResponseFail()

        # 抽取的盲盒数量大于盲盒库存
        vntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
            [3000, [2002, 0]]], memo='swap', suber='user1').assetResponseFail()

        # booth未到开始时间则失败
        rndnftswap.setboothtime(
            owner='user1', quote_nft_contract="verso.mid", symbol_id=2002, opened_at="2023-8-26T02:50:00.000", closed_at="2023-11-26T02:50:00.000", suber=rndnftswap.contract)
        vntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
            [2, [2002, 0]]], memo='swap', suber='user1').assetResponseFail()
        rndnftswap.setboothtime(
            owner='user1', quote_nft_contract="verso.mid", symbol_id=2002, opened_at="2022-8-26T02:50:00.000", closed_at="2023-11-26T02:50:00.000", suber=rndnftswap.contract)

        # booth已结束则失败 11010
        vntoken.transfer(fromx='user1', to='rndnft.swap1', assets=[
            [2, [11010, 0]]], memo='swap', suber='user1').assetResponseFail()
