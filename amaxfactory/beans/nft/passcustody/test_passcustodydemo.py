from nft.passcustody.passcustody import PASSCUSTODY
cus = PASSCUSTODY()


def test_addplan():
    cus.addplan(owner='p1.mart', title='NFT pass one lock 365', asset_contract='pass.ntoken',
                asset_symbol=[1005,0], unlock_interval_days=365, unlock_times=1, suber='p1.mart')


def test_endissue(): cus.endissue(
    issuer='user1', plan_id=1, issue_id=1, suber='user1')


def test_init(): cus.init(suber='user1')


def test_setconfig(): cus.setconfig(plan_fee="0.10000000 AMAX",
                                    fee_receiver='user1', suber='user1')


def test_setplanowner(): cus.setplanowner(
    owner='user1', plan_id=1, new_owner='user1', suber='user1')


def test_unlock(): cus.unlock(unlocker='user1', plan_id=1, issue_id=6, suber='user1')


def test_endlock(): cus.endlock(unlocker='user1', plan_id=1, issue_id=6, suber='user1')


def test_setwindow():
    cus.setwindow(plan_id=1,start_at='2022-11-01T03:51:00',finish_at='2022-11-01T16:51:00',symbol=[1,0],suber='p1.mart')


