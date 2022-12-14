from xchain.mtoken.mtoken import Mtoken

mtoken = Mtoken()


class TestMtoken:
    def test_1(self):
        mtoken.create(issuer='user111', maximum_supply="1000000.00000000 AMAXXX", suber=mtoken.contract).assetResponseFail()
        mtoken.create(issuer='', maximum_supply="1000000.00000000 AMAXXX", suber=mtoken.contract).assetResponseFail()
        mtoken.create(issuer='user1', maximum_supply="0.00000000 AMAXXX", suber=mtoken.contract).assetResponseFail()
        mtoken.create(issuer='user1', maximum_supply="-1.00000000 AMAXXX", suber=mtoken.contract).assetResponseFail()
        mtoken.create(issuer='user1', maximum_supply="10.00000000 AMAxxXxXX", suber=mtoken.contract).assetResponseFail()
        mtoken.create(issuer='user1', maximum_supply="10.00000000 MUSDT", suber=mtoken.contract).assetResponseFail()

    def test_2(self):
        mtoken.create(issuer='user1', maximum_supply="1000000.00000000 TEST", suber=mtoken.contract).assetResponsePass()
        mtoken.issue(to='ad', quantity="10.10000000 TEST", memo='x', suber='user1').assetResponseFail()
        mtoken.issue(to='user1xxx', quantity="10.10000000 TEST", memo='x', suber='user1').assetResponseFail()
        mtoken.issue(to='user1', quantity="1000000.10000000 TEST", memo='x', suber='user1').assetResponseFail()
        mtoken.issue(to='user1', quantity="0.00000000 TEST", memo='x', suber='user1').assetResponseFail()
        mtoken.issue(to='user1', quantity="-110.10000000 TEST", memo='x', suber='user1').assetResponseFail()
        mtoken.issue(to='user1', quantity="10.100000 TEST", memo='x', suber='user1').assetResponseFail()
        mtoken.issue(to='user1', quantity="10.100000 TESXXT", memo='x', suber='user1').assetResponseFail()
        mtoken.issue(to='user1', quantity="500000.00000000 TEST", memo='x', suber='user1').assetResponsePass()
        mtoken.issue(to='user1', quantity="600000.00000000 TEST", memo='x', suber='user1').assetResponseFail()
        mtoken.issue(to='ad', quantity="50.00000000 TEST", memo='x', suber='ad').assetResponseFail()


    def test_3(self):
        mtoken.open(owner='add', symbol='8,TEST', ram_payer='user1', suber='user1').assetResponseFail()
        mtoken.open(owner='ad', symbol='8,TESTT', ram_payer='user1', suber='user1').assetResponseFail()
        mtoken.open(owner='ad', symbol='9,TEST', ram_payer='user1', suber='user1').assetResponseFail()
        mtoken.open(owner='ad', symbol='8,TEST', ram_payer='ad', suber='user1').assetResponseFail()
        mtoken.open(owner='ad', symbol='8,TEST', ram_payer='add', suber='user1').assetResponseFail()
        mtoken.open(owner='ad', symbol='8,TEST', ram_payer='user1', suber='user1').assetResponsePass()

    def test_4(self):
        mtoken.close(owner='add', symbol='8,TEST', suber='user1').assetResponseFail()
        mtoken.close(owner='merchantx', symbol='8,TEST', suber='user1').assetResponseFail()
        # mtoken.close(owner='ad', symbol='8,TEST', suber='ad').assetResponsePass()

        mtoken.transfer(fromx='user1', to='mk', quantity="1.00000000 TEST", memo='x', suber='user1').assetResponsePass()
        mtoken.close(owner='mk', symbol='8,TEST', suber='user1').assetResponseFail()

        mtoken.close(owner='ad', symbol='8,TEST', suber='user1').assetResponseFail()

    def test_5(self):
        mtoken.transfer(fromx='user1', to='mk', quantity="1.00000000 TEST", memo='x', suber='ad').assetResponseFail()

        mtoken.transfer(fromx='user111', to='mk', quantity="1.00000000 TEST", memo='x', suber='user1').assetResponseFail()
        mtoken.transfer(fromx='user1', to='mkxx', quantity="1.00000000 TEST", memo='x', suber='user1').assetResponseFail()
        mtoken.transfer(fromx='user1', to='mk', quantity="10000000.00000000 TEST", memo='x', suber='user1').assetResponseFail()
        mtoken.transfer(fromx='user1', to='mk', quantity="0.00000000 TEST", memo='x', suber='user1').assetResponseFail()
        mtoken.transfer(fromx='user1', to='mk', quantity="-1.00000000 TEST", memo='x', suber='user1').assetResponseFail()
        mtoken.transfer(fromx='user1', to='mk', quantity="1.0000000 TEST", memo='x', suber='user1').assetResponseFail()
        mtoken.transfer(fromx='user1', to='mk', quantity="1.00000000 TREST", memo='x', suber='user1').assetResponseFail()

        mtoken.transfer(fromx='user1', to='mk', quantity="1.00000000 TEST", memo='x', suber='user1').assetResponsePass()

    def test_6(self):
        mtoken.retire(quantity="10000000.10000000 TEST", memo='x', suber='user1').assetResponseFail()
        mtoken.retire(quantity="0.00000000 TEST", memo='x', suber='user1').assetResponseFail()
        mtoken.retire(quantity="-0.10000000 TEST", memo='x', suber='user1').assetResponseFail()
        mtoken.retire(quantity="0.10000000 TREST", memo='x', suber='user1').assetResponseFail()
        mtoken.retire(quantity="0.1000000 TEST", memo='x', suber='user1').assetResponseFail()
        mtoken.retire(quantity="0.10000000 TEST", memo='x', suber='mk').assetResponseFail()
        mtoken.retire(quantity="0.10000000 TEST", memo='x', suber='user1').assetResponsePass()



    def test_x(self):
        # mtoken.transfer(fromx='ad', to='user1', quantity="1000.00000000 MBTC", memo='x', suber='ad').assetResponsePass()
        # mtoken.transfer(fromx='ad', to='user1', quantity="1000.00000000 METH", memo='x', suber='ad').assetResponsePass()
        mtoken.transfer(fromx='ad', to='user1', quantity="10000.000000 MUSDT", memo='x', suber='ad').assetResponsePass()
