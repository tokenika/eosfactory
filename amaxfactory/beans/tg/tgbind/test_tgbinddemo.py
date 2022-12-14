from tg.tgbind.tgbind import tgbind as tg
tgbind = tg()

def test_bind(): tgbind.bind(account='user1',tgid=1111,suber='user1')
def test_confirm(): tgbind.confirm(tgid=1111,suber='ad')
def test_delbind(): tgbind.delbind(tgid=1111,suber='ad')
def test_init(): tgbind.init(account='ad',suber='tgbind')
