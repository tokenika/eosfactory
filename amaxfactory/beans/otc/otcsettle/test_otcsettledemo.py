from otc.otcsettle.otcsettle import Otcsettle

otcsettle = Otcsettle()


def test_deal(): otcsettle.deal(deal_id=10001, merchant='merchantx', user='1234amax1234', quantity="1000.000000 MUSDT",
                                fee="5.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:36", suber='meta.book')


def test_pick(): otcsettle.pick(reciptian='user1', rewards=[0,1,2], suber='user1')


def test_setadmin(): otcsettle.setadmin(admin='ad', market='cashx1', swap='otcswapv2', suber=otcsettle.contract).assetResponsePass()


def test_setconfig(): otcsettle.setconf(conf="otcconf1", suber=otcsettle.contract)


def test_setlevel(): otcsettle.setlevel(user='user1', level=1, suber='ad')
