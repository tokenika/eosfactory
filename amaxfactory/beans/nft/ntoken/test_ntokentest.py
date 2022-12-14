from time import sleep
from nft.ntoken.ntoken import ntoken as n

ntoken = n()


class TestNtoken:
    def test_1(self):
        ntoken.create(issuer='user1111', maximum_supply=10, symbol=[8888, 0], token_uri='8888', ipowner='user1',
                      suber='user1').assetResponseFail()
        ntoken.create(issuer='ad', maximum_supply=10, symbol=[8888, 0], token_uri='8888', ipowner='user1',
                      suber='user1').assetResponseFail()
        ntoken.create(issuer='user1', maximum_supply=0, symbol=[8888, 0], token_uri='8888', ipowner='user1',
                      suber='user1').assetResponseFail()
        ntoken.create(issuer='user1', maximum_supply=-10, symbol=[8888,0], token_uri='8888', ipowner='user1',
                      suber='user1').assetResponseFail()
        ntoken.create(issuer='user1', maximum_supply=10, symbol=[7, 0], token_uri='8888', ipowner='user1',
                      suber='user1').assetResponseFail()
        ntoken.create(issuer='user1', maximum_supply=10, symbol=[8888,0], token_uri='xxx3', ipowner='user1',
                      suber='user1').assetResponseFail()

        # ntoken.create(issuer='user1', maximum_supply=10, symbol=[8886, 0], token_uri='8886', ipowner='user1',
        #               suber='user1').assetResponsePass()
        ntoken.create(issuer='user1', maximum_supply=10, symbol=[8885, 7], token_uri='8885', ipowner='user1',
                      suber='user1').assetResponsePass()
        ntoken.create(issuer='user1', maximum_supply=10, symbol=[8891, 0], token_uri='8891', ipowner='user11111',
                      suber='user1').assetResponseFail()


    def test_2(self):
        ntoken.create(issuer='user1', maximum_supply=100, symbol=[188882, 7], token_uri='188882', ipowner='user1',
                      suber='user1').assetResponsePass()
        ntoken.issue(to='user1xxxx', quantity=[10, [18888, 7]], memo='x', suber='user1').assetResponseFail()
        ntoken.issue(to='ad', quantity=[10, [18888, 7]], memo='x', suber='user1').assetResponseFail()
        ntoken.issue(to='user1', quantity=[0, [18888, 7]], memo='x', suber='user1').assetResponseFail()
        ntoken.issue(to='user1', quantity=[-10, [18888, 7]], memo='x', suber='user1').assetResponseFail()
        ntoken.issue(to='user1', quantity=[101, [18888, 7]], memo='x', suber='user1').assetResponseFail()
        ntoken.issue(to='user1', quantity=[10, [18888, 7]], memo='x', suber='ad').assetResponseFail()
        ntoken.issue(to='ad', quantity=[10, [18888, 7]], memo='x', suber='ad').assetResponseFail()
        ntoken.issue(to='user1', quantity=[10, [188882, 7]], memo='x', suber='user1').assetResponsePass()
        ntoken.issue(to='user1', quantity=[91, [188882, 7]], memo='x', suber='user1').assetResponseFail()
        ntoken.issue(to='user1', quantity=[90, [188882, 7]], memo='x', suber='user1').assetResponsePass()


    def test_3(self):
        # ntoken.setnotary(notary='user1xx', add='true', suber=ntoken.contract).assetResponseFail()
        ntoken.setnotary(notary='user1', add='true', suber=ntoken.contract).assetResponsePass()
        ntoken.setnotary(notary='user1', add='false', suber=ntoken.contract).assetResponsePass()
        ntoken.setnotary(notary='user1', add='true', suber='user1').assetResponseFail()

    def test_4(self):
        ntoken.setnotary(notary='user1', add='true', suber=ntoken.contract).assetResponsePass()
        ntoken.notarize(notary='user11111', token_id=18888, suber='user1').assetResponseFail()
        ntoken.notarize(notary='user1', token_id=18888, suber='ad').assetResponseFail()
        ntoken.notarize(notary='ad', token_id=18888, suber='user1').assetResponseFail()
        ntoken.notarize(notary='user1', token_id=188828, suber='user1').assetResponseFail()
        ntoken.notarize(notary='ad', token_id=18888, suber='ad').assetResponseFail()
        ntoken.notarize(notary='user1', token_id=18888, suber='user1').assetResponsePass()

        ntoken.setnotary(notary='ck', add='true', suber=ntoken.contract).assetResponsePass()
        ntoken.notarize(notary='ck', token_id=18888, suber='ck').assetResponsePass()


    def test_5(self):
        # ntoken.create(issuer='user1', maximum_supply=100, symbol=[18889, 7], token_uri='18889', ipowner='user1',
        #               suber='user1').assetResponsePass()
        # ntoken.issue(to='user1', quantity=[10, [18889, 7]], memo='x', suber='user1').assetResponsePass()

        ntoken.retire(quantity=[0, [18889, 7]], memo='x', suber='user1').assetResponseFail()
        ntoken.retire(quantity=[-1, [18889, 7]], memo='x', suber='user1').assetResponseFail()
        ntoken.retire(quantity=[11, [18889, 7]], memo='x', suber='user1').assetResponseFail()
        ntoken.retire(quantity=[1, [18889]], memo='x', suber='user1').assetResponseFail()
        ntoken.retire(quantity=[1, [18889, 7]], memo='x', suber='user1').assetResponsePass()

        ntoken.transfer(fromx='user1', to='mk', assets=[[1, [18889, 7]]], memo='1', suber='user1').assetResponsePass()
        ntoken.retire(quantity=[1, [18889, 7]], memo='x', suber='mk').assetResponseFail()

    def test_6(self):
        ntoken.transfer(fromx='user1', to='mk', assets=[[10, [18888, 7]]], memo='1', suber='user1').assetResponsePass()

        ntoken.transfer(fromx='mk', to='user1', assets=[[1, [18888, 7]]], memo='1', suber='user1').assetResponseFail()
        ntoken.transfer(fromx='user111', to='mk', assets=[[1, [18888, 7]]], memo='1', suber='user1').assetResponseFail()
        ntoken.transfer(fromx='user1', to='mk111', assets=[[1, [18888, 7]]], memo='1', suber='user1').assetResponseFail()
        ntoken.transfer(fromx='user1', to='mk', assets=[[101, [18888, 7]]], memo='1', suber='user1').assetResponseFail()
        ntoken.transfer(fromx='user1', to='mk', assets=[[0, [18888, 7]]], memo='1', suber='user1').assetResponseFail()
        ntoken.transfer(fromx='user1', to='mk', assets=[[-1, [18888, 7]]], memo='1', suber='user1').assetResponseFail()
        ntoken.transfer(fromx='user1', to='mk', assets=[[1, [18888]]], memo='1', suber='user1').assetResponseFail()
        ntoken.transfer(fromx='user1', to='mk', assets=[[1, [18888111, 7]]], memo='1', suber='user1').assetResponseFail()
        ntoken.transfer(fromx='user1', to='mk', assets=[[10, [18888, 7]], [1, [18889, 7]]], memo='1', suber='user1').assetResponsePass()

    def test_7(self):
        ntoken.create(issuer='ad', maximum_supply=1000000, symbol=[1,0], token_uri=f'xx2xx{ntoken.getCode()}', ipowner='ad',
                                 suber='ad')
        ntoken.issue(to='ad', quantity=[1000000,[1,0]], memo='x', suber='ad')
