
from redpackcase.redpack import redpack as r
from amax.cnydtoken.cnyd import CNYD
from amax.amaxtoken.amax import AMAX
from xchain.mtoken.mtoken import Mtoken

cnyd = CNYD()
amax = AMAX()
mtoken = Mtoken()
redpack = r()

class TestRedpack:

    def test_ontransfer(self):
        # cnyd.transfer(fromx='ad', to=redpack.contract, quantity="0.1000 CNYD", memo='xxx:3:0',
        #               suber='ad').assetResponsePass()
        #
        # id = redpack.getLastRow('redpack3', 'redpacks')['id']
        # redpack.claim(claimer='merchantx', pack_id=id, pwhash='xxx', name='m1merchantx', suber='ad').assetResponsePass()
        # redpack.claim(claimer='mk', pack_id=id, pwhash='xxx', name='m1mk', suber='ad').assetResponsePass()
        # redpack.claim(claimer='ck', pack_id=id, pwhash='xxx', name='m1ck', suber='ad').assetResponsePass()

        amax.transfer(fromx='ad', to=redpack.contract, quantity="0.00100000 AMAX", memo='xxx:1:0',
                      suber='ad').assetResponsePass()

        id = redpack.getLastRow('redpack3', 'redpacks')['id']
        redpack.claim(claimer='merchantx', pack_id=id, pwhash='xxx', name='m1merchantx', suber='ad').assetResponsePass()
        redpack.claim(claimer='mk', pack_id=id, pwhash='xxx', name='m1mk', suber='ad').assetResponsePass()
        redpack.claim(claimer='ck', pack_id=id, pwhash='xxx', name='m1ck', suber='ad').assetResponsePass()

    def test_setconf(self):
        redpack.setconf(admin='addd', hours=1, suber=redpack.contract).assetResponseFail()
        # redpack.setconf(admin='ad', hours=-1, suber=redpack.contract).assetResponseFail()
        redpack.setconf(admin='ad', hours=1, suber='ad').assetResponseFail()
        redpack.setconf(admin='mk', hours=1, suber=redpack.contract).assetResponsePass()
        redpack.setconf(admin='ad', hours=1, suber=redpack.contract).assetResponsePass()


    def test_addfee(self):
        redpack.delfee(coin='8,AMAX', suber=redpack.contract)
        redpack.addfee(fee="-1.00000000 AMAX", contract='amax.token', min=4, suber=redpack.contract).assetResponseFail()
        # redpack.addfee(fee="0.00000000 AMAX", contract='amax.token', min=-1, suber=redpack.contract).assetResponseFail()
        # redpack.addfee(fee="0.00000000 AMAX", contract='amax.token', min=9, suber=redpack.contract).assetResponseFail()
        redpack.addfee(fee="0.00000000 AMAX", contract='amax.token', min=4, suber=redpack.contract).assetResponsePass()
        redpack.addfee(fee="0.00000000 AMAX", contract='amax.token', min=5, suber=redpack.contract).assetResponsePass()
        redpack.addfee(fee="0.00000000 AMAX", contract='amax.token', min=4, suber='ad').assetResponseFail()

    def test_x(self):
        # redpack.delfee(coin='8,METH', suber=redpack.contract).assetResponsePass()
        # redpack.delfee(coin='8,MBTC', suber=redpack.contract).assetResponsePass()
        redpack.delfee(coin='4,CNYD', suber=redpack.contract).assetResponsePass()
        redpack.addfee(fee="0.00000000 METH", contract='amax.mtoken', min=5, suber=redpack.contract).assetResponsePass()
        redpack.addfee(fee="0.00000000 MBTC", contract='amax.mtoken', min=6, suber=redpack.contract).assetResponsePass()
        redpack.addfee(fee="0.0000 CNYD", contract='cnyd.token', min=2, suber=redpack.contract).assetResponsePass()


    def test_delfee(self):
        # redpack.delfee(coin='5,CNYD', suber=redpack.contract).assetResponseFail()
        redpack.delfee(coin='4,CNYDD', suber=redpack.contract).assetResponseFail()
        redpack.delfee(coin='4,CNYD', suber='user1').assetResponseFail()
        redpack.delfee(coin='4,CNYD', suber=redpack.contract).assetResponsePass()
        redpack.addfee(fee="0.0000 CNYD", contract='cnyd.token', min=2, suber=redpack.contract).assetResponsePass()



    def test_create(self):
        redpack.addfee(fee="0.1000 CNYD", contract='cnyd.token', min=2, suber=redpack.contract).assetResponsePass()
        cnyd.transfer(fromx='user1', to=redpack.contract, quantity="10.0000 CNYD", memo='xxx:3:2',
                                     suber='user1').assetResponseFail()
        cnyd.transfer(fromx='user1', to=redpack.contract, quantity="1.0999 CNYD", memo='xxx:10:0',
                      suber='user1').assetResponseFail()
        cnyd.transfer(fromx='user1', to=redpack.contract, quantity="1.1000 CNYD", memo='xxx:10:0',
                      suber='user1').assetResponsePass()
        cnyd.transfer(fromx='user1', to=redpack.contract, quantity="10.0000 CNYD", memo='xxx:10:0',
                  suber='user1').assetResponsePass()

    def test_claim1(self):
        cnyd.transfer(fromx='user1', to=redpack.contract, quantity="0.3300 CNYD", memo='xxx:3:0',
                      suber='user1').assetResponsePass()
        id = redpack.getLastRow('redpack3','redpacks')['id']
        # 用户不存在应失败
        redpack.claim(claimer='mxk', pack_id=id, pwhash='xxx', name='m1mk', suber='ad').assetResponseFail()
        redpack.claim(claimer='merchantx', pack_id=id, pwhash='xxx', name='m1merchantx', suber='ad').assetResponsePass()
        redpack.claim(claimer='mk', pack_id=id, pwhash='xxx', name='m1mk', suber='ad').assetResponsePass()
        # 重复领取失败
        redpack.claim(claimer='mk', pack_id=id, pwhash='xxx', name='m1mk', suber='ad').assetResponseFail()
        redpack.claim(claimer='ck', pack_id=id, pwhash='xxx', name='m1ck', suber='ad').assetResponsePass()
        # 已领取完应失败
        redpack.claim(claimer='fee', pack_id=id, pwhash='xxx', name='m1mk', suber='ad').assetResponseFail()

        cnyd.transfer(fromx='user1', to=redpack.contract, quantity="0.3300 CNYD", memo='xxx:3:0',
                      suber='user1').assetResponsePass()
        id = redpack.getLastRow('redpack3', 'redpacks')['id']
        redpack.setconf(admin='ad', hours=0, suber=redpack.contract).assetResponsePass()

        redpack.cancel(pack_id=id, suber='ad').assetResponsePass()
        # 已取消应失败
        redpack.claim(claimer='fee', pack_id=id, pwhash='xxx', name='m1mk', suber='ad').assetResponseFail()



    def test_claim2(self):
        cnyd.transfer(fromx='user1', to=redpack.contract, quantity="1.3300 CNYD", memo='xxx:3:1',
                      suber='user1').assetResponsePass()
        id = redpack.getLastRow('redpack3', 'redpacks')['id']
        redpack.claim(claimer='merchantx', pack_id=id, pwhash='xxx', name='m1merchantx', suber='ad').assetResponsePass()
        redpack.claim(claimer='mk', pack_id=id, pwhash='xxx', name='m1mk', suber='ad').assetResponsePass()
        redpack.claim(claimer='ck', pack_id=id, pwhash='xxx', name='m1ck', suber='ad').assetResponsePass()

    def test_cancel(self):
        # cnyd.transfer(fromx='user1', to=redpack.contract, quantity="1.3300 CNYD", memo='xxx:3:0',
        #               suber='user1').assetResponsePass()
        # id = redpack.getLastRow('redpack3', 'redpacks')['id']
        # redpack.setconf(admin='ad', hours=0, suber=redpack.contract).assetResponsePass()
        # # 全额退回
        # redpack.cancel(pack_id=id, suber='ad').assetResponsePass()

        #  部分退回
        cnyd.transfer(fromx='user1', to=redpack.contract, quantity="1.3300 CNYD", memo='xxx:3:0',
                      suber='user1').assetResponsePass()
        id = redpack.getLastRow('redpack3', 'redpacks')['id']
        redpack.setconf(admin='ad', hours=0, suber=redpack.contract).assetResponsePass()
        redpack.claim(claimer='ck', pack_id=id, pwhash='xxx', name='m1ck', suber='ad').assetResponsePass()
        redpack.cancel(pack_id=id, suber='ad').assetResponsePass()
        # 取消状态不可再取消
        redpack.cancel(pack_id=id, suber='ad').assetResponseFail()

        cnyd.transfer(fromx='user1', to=redpack.contract, quantity="1.3300 CNYD", memo='xxx:3:0',
                      suber='user1').assetResponsePass()
        id = redpack.getLastRow('redpack3', 'redpacks')['id']
        redpack.cancel(pack_id=id + 1, suber='ad').assetResponseFail()
        redpack.cancel(pack_id=id, suber='user1').assetResponseFail()

        redpack.setconf(admin='ad', hours=1, suber=redpack.contract).assetResponsePass()
        # 未到过期时间，不可取消
        redpack.cancel(pack_id=id, suber='ad').assetResponseFail()
        redpack.setconf(admin='ad', hours=0, suber=redpack.contract).assetResponsePass()
