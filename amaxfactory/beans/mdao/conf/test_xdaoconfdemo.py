from mdao.conf.xdaoconf import XDAOCONF
xdaoconf = XDAOCONF()


def test_daoconf(): xdaoconf.daoconf(feetaker='user1', appinfo=1,
                                     status='user1', daoupgfee="0.10000000 AMAX", suber='user1')


def test_init(): xdaoconf.init(feetaker='fee', appinfo=["appname","version","url","logo"],
                               daoupgfee="1.00000000 AMAX", admin='ad',status="running" ,suber=xdaoconf.contract)
                               
def test_managerconf(): xdaoconf.setmanager(
    managetype='redpeck', manager='xredpeck', suber=xdaoconf.contract)


def test_reset(): xdaoconf.reset(suber='user1')
def test_seatconf(): xdaoconf.seatconf(
    amctokenmax=1, evmtokenmax=1, dappmax=1, suber='user1')


def test_setlimitcode(): xdaoconf.setlimitcode(symbolcode=1, suber='user1')
