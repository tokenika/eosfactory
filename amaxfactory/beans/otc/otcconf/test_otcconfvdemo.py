from otc.otcconf.otcconfv import otcconfv as o
otcconfv = o()


def test_init(): 
    otcconfv.init(admin='ad', suber=otcconfv.contract)


def test_setappname(): otcconfv.setappname(otc_name='user1', suber='user1')


def test_setfarm(): otcconfv.setfarm(farmname='aplink.farm', farm_id=3,symbol="MUSDT", farm_scale=40000, suber='ad')
def test_setfarm2(): otcconfv.setfarm(farmname='aplink.farm', farm_id=3,symbol="AMAX", farm_scale=10000000, suber='ad')



def test_setmanager(): otcconfv.setmanager(type='otcbook', account='cashx1', suber='ad')
def test_setmanager2(): otcconfv.setmanager(type='settlement', account='otcsettle1', suber='ad')
def test_setmanager3(): otcconfv.setmanager(type='swaper', account='otcswapa1', suber='ad')
def test_setmanager4(): otcconfv.setmanager(type='arbiter', account='ad', suber='ad')
# def test_setmanager(): otcconfv.setmanager(type='settlement', account='cashx1', suber='ad')


def test_setsettlelv(): otcconfv.setsettlelv(configs=[[0,0,0],[1000000000,1000,4000],[3000000000,2500,5000],[6000000000,4000,6000]], suber='ad')


def test_setstatus(): otcconfv.setstatus(status=2, suber='ad')


def test_setswapstep(): otcconfv.setswapstep(rates=[[0,1500],[1000000000,2500],[2000000000,3500],[3000000000,5000]], suber="ad")


def test_settimeout(): otcconfv.settimeout(accepted_timeout=300, payed_timeout=600, suber=otcconfv.contract)

def test_init(): otcconfv.init('ad',otcconfv.contract)