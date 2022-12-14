from tg.tgbind.tgbind import tgbind as tg
tgbind = tg()

class Testbind:
    def test_init(self):
        # tgbind.init(account='ad1', suber=tgbind.contract).assetResponseFail()
        tgbind.init(account='ad', suber='user1').assetResponseFail()
        tgbind.init(account='mk', suber=tgbind.contract).assetResponsePass()
        tgbind.init(account='ad', suber=tgbind.contract).assetResponsePass()


    def test_bind(self):
        tgbind.bind(account='user11111', tgid=11111, suber=tgbind.contract).assetResponseFail()
        tgbind.bind(account='mk', tgid=11111, suber='user1').assetResponseFail()
        tgbind.bind(account='user1', tgid=11111, suber='user1').assetResponseFail()
        tgbind.bind(account='mk', tgid=1111, suber='mk').assetResponseFail()

    def test_confirm(self):
        tgbind.confirm(tgid=1111188, suber='ad').assetResponseFail()
        tgbind.confirm(tgid=2056977094, suber='user1').assetResponseFail()

    def test_delbind(self):
        tgbind.bind(account='fee', tgid=2222, suber='fee').assetResponsePass()

        tgbind.delbind(tgid=111185888, suber='ad').assetResponseFail()
        tgbind.delbind(tgid=2222, suber='user1').assetResponseFail()
        tgbind.delbind(tgid=2222, suber='ad').assetResponsePass()

