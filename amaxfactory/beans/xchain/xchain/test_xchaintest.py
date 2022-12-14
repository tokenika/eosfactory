from amax.amaxtoken.amax import AMAX
from xchain.xchain.xchain import xchain as x
from xchain.mtoken.mtoken import Mtoken

mtoken = Mtoken()
xchain = x()
amax = AMAX()


class TestXchain:
    def test_1(self):
        # amax.create(issuer='amax', maximum_supply="100000000.00000000 AMUSDT", suber='amax.token')
        # amax.issue(to='amax', quantity="10000000.00000000 AMUSDT", memo='x', suber='amax')
        # amax.transfer(fromx='amax', to=xchain.contract, quantity="10000.00000000 AMUSDT", memo='x', suber='amax')
        xchain.addcoin(account='ad', coin='6,MBNB', suber='ad')
        xchain.addchaincoin(account='ad', chain='bsc', coin='6,MBNB',
                                                     fee="0.000100 MBNB", suber='ad')

    def test_2(self):
        # mtoken.create(issuer='ad', maximum_supply="1000000000.00000000 METH", suber=mtoken.contract)
        # mtoken.create(issuer='ad', maximum_supply="1000000000.00000000 MBTC", suber=mtoken.contract)
        # mtoken.create(issuer='ad', maximum_supply="1000000000.000000 MUSDT", suber=mtoken.contract)
        # mtoken.create(issuer='ad', maximum_supply="1000000000.000000 MBNB", suber=mtoken.contract)
        # mtoken.create(issuer='ad', maximum_supply="1000000000.0000 METAS", suber=mtoken.contract)

        # mtoken.issue(to='ad', quantity="100000000.00000000 METH", memo='x', suber='ad')
        # mtoken.issue(to='ad', quantity="100000000.00000000 MBTC", memo='x', suber='ad')
        # mtoken.issue(to='ad', quantity="100000000.00000000 Mtron", memo='x', suber='ad')
        # mtoken.issue(to='ad', quantity="100000000.000000 MUSDT", memo='x', suber='ad')
        # mtoken.issue(to='ad', quantity="100000000.000000 MBNB", memo='x', suber='ad')
        # mtoken.issue(to='ad', quantity="100000000.0000 METAS", memo='x', suber='ad')

        # xchain.init(admin='ad', maker='mk', checker='ck', fee_collector='fee', suber=xchain.contract)
        mtoken.transfer(fromx='ad', to=xchain.contract, quantity="10000.00000000 METH", memo='refuel', suber='ad')
        mtoken.transfer(fromx='ad', to=xchain.contract, quantity="10000.00000000 MBTC", memo='refuel', suber='ad')
        mtoken.transfer(fromx='ad', to=xchain.contract, quantity="10000.000000 MUSDT", memo='refuel', suber='ad')

        mtoken.transfer(fromx='ad', to=xchain.contract, quantity="100000.000000 MBNB", memo='refuel', suber='ad')
        
        # xchain.addchain(account='ad', chain='eth', base_chain='eth', common_xin_account='', suber='ad')
        # xchain.addchain(account='ad', chain='btc', base_chain='btc', common_xin_account='', suber='ad')
        # xchain.addchain(account='ad', chain='bsc', base_chain='eth', common_xin_account='', suber='ad')
        # xchain.addchain(account='ad', chain='tron', base_chain='tron', common_xin_account='', suber='ad')

        
        # xchain.addcoin(account='ad', coin='6,MUSDT', suber='ad')
        # xchain.addchaincoin(account='ad', chain='eth', coin='6,MUSDT',
        #                                              fee="5.000000 MUSDT", suber='ad')
        # xchain.addchaincoin(account='ad', chain='bsc', coin='6,MUSDT',
        #                                              fee="4.000000 MUSDT", suber='ad')
        # xchain.addchaincoin(account='ad', chain='tron', coin='6,MUSDT',
        #                                              fee="2.000000 MUSDT", suber='ad')
        # #
        # xchain.addcoin(account='ad', coin='8,METH', suber='ad')
        # xchain.addchaincoin(account='ad', chain='eth', coin='8,METH',
        #                     fee="0.00200000 METH", suber='ad')
        # xchain.delchaincoin(account='ad', chain='eth', coin='8,METH', suber='ad')

        # xchain.addcoin(account='ad', coin='6,MBNB', suber='ad')

        # xchain.addchaincoin(account='ad', chain='bsc', coin='6,MBNB',
        #                     fee="0.001000 MBNB", suber='ad')
        
        # xchain.addcoin(account='ad', coin='8,MBTC', suber='ad')
        # xchain.addchaincoin(account='ad', chain='btc', coin='8,MBTC',
        #                     fee="0.00020000 MBTC", suber='ad')


    def test_3(self):
        # xchain.delchain(account='ad', chain='tron', suber='ad')
        # xchain.addchain(account='ad', chain='tron', base_chain='tron', common_xin_account='', suber='ad')

        # xchain.delcoin(account='ad', coin='8,Mtron', suber='ad')
        # xchain.delcoin(account='ad', coin='8,AMBTC', suber='ad')
        # xchain.delcoin(account='ad', coin='8,AMBNB', suber='ad')
        # xchain.delcoin(account='ad', coin='8,AMUSDT', suber='ad')
        # xchain.delchaincoin(account='ad', chain='eth', coin='6,AMUSDT', suber='ad')
        # xchain.delchaincoin(account='ad', chain='eth', coin='8,AMETH', suber='ad')
        # xchain.delchaincoin(account='ad', chain='eth', coin='8,AMBNB', suber='ad')
        # xchain.delchaincoin(account='ad', chain='btc', coin='8,AMBTC', suber='ad')

        # xchain.delchaincoin(account='ad', chain='btc', coin='8,MBTC', suber='ad')
        # xchain.delchaincoin(account='ad', chain='eth', coin='8,METH', suber='ad')
        # xchain.delchaincoin(account='ad', chain='eth', coin='6,MUSDT', suber='ad')
        # xchain.delchaincoin(account='ad', chain='bsc', coin='6,MUSDT', suber='ad')
        # xchain.delchaincoin(account='ad', chain='tron', coin='6,MUSDT', suber='ad')
        
        xchain.delcoin(account='ad', coin='6,MBNB', suber='ad')
        xchain.delchaincoin(account='ad', chain='bsc', coin='8,MBNB', suber='ad')


    def test_4(self):
        xchain.reqxintoaddr(applicant='amcfafyqyhvw', applicant_account='amcfafyqyhvw', base_chain='tron', mulsign_wallet_id=0,
                            suber='amcfafyqyhvw').assetResponsePass()
        xchain.setaddress(applicant='amcfafyqyhvw', base_chain='tron', mulsign_wallet_id=0, xin_to='amcfafyqyhvwamcfafyqyhvwxx',
                                                 suber='mk').assetResponsePass()
        id = xchain.getLastXinorders()['id'] + 1
        xchain.mkxinorder(to='amcfafyqyhvw', chain_name='tron', coin_name='6,MUSDC', txid=f'txidxxxx222{xchain.getCode()}', xin_from='fromx', xin_to='amcfafyqyhvwamcfafyqyhvwxx',
                          quantity="100.000000 MUSDC", suber='mk').assetResponsePass()
        assert xchain.getLastXinorders()['id'] == id
        xchain.checkxinord(order_id=id, suber='ck').assetResponsePass()

    def test_5(self):
        id = xchain.getLastXoutorders()['id'] + 1
        mtoken.transfer(fromx='user1', to=xchain.contract, quantity="1.00200600 METH", memo='addressxx:eth:8,METH:0:memoxx', suber='user1')
        xchain.setxousent(order_id=id, txid=f'x{xchain.getCode()}', xout_from='x', suber='mk')
        xchain.setxouconfm(order_id=id, suber='mk')
        xchain.checkxouord(order_id=id, suber='ck')

    
    def test_create_date(self):
        for i in range(1000):
            # mtoken.transfer(fromx='user1', to=xchain.contract, quantity="1.00200600 METH", memo=f'addressxx{xchain.getCode()}:eth:8,METH:0:memoxx', suber='user1')
            xchain.mkxinorder(to='amcfafyqyhvw', chain_name='eth', coin_name='8,METH', txid=f'txidxxxx222{xchain.getCode()}', xin_from='fromx', xin_to='amcfafyqyhvwamcfafyqyhvw1',
                          quantity="1.55555555 METH", suber='mk').assetResponsePass()