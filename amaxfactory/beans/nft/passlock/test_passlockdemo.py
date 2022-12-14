from re import sub
from nft.passlock.passlock import PASSLOCK
from nft.passsell.passsell import PASSSELL
passsell = PASSSELL()
passlock = PASSLOCK()


def test_addplan(): passlock.addplan(owner='user1', title='pass one lock3',asset_contract='pass.ntoken',asset_symbol=[1002,0],unlock_interval_days=5,unlock_times=5,suber='user1') 
def test_enableplan(): passlock.enableplan(owner='user1',plan_id=6,enabled='true',suber='user1') 
# def test_init(): passlock.init(suber=passlock.contract) 
def test_setplanowner(): 
    # passlock.setplanowner(owner=passlock.contract,plan_id=3,new_owner='pass.sell',suber=passlock.contract) 
    passlock.setplanowner(owner="user1",plan_id=6,new_owner='ad',suber="user1") 


def test_enableplan(): passlock.enableplan(
    owner='user1', plan_id=1, enabled='true', suber='user1')
# def test_init(): passlock.init(suber=passlock.contract)

def test_setwindow():
    passlock.setwindow(plan_id=1,start_at='2022-10-31T03:51:00',finish_at='2022-11-20T16:51:00',symbol=[1,0],suber='p1.mart')

def test_setplanowner():
    # passlock.setplanowner(owner=passlock.contract,plan_id=3,new_owner='pass.sell',suber=passlock.contract)
    passlock.setplanowner(owner="pass.sell", plan_id=3,
                          new_owner='user1', suber="user1")


def test_unlock():
    # passlock.unlock(owner='user1',lock_id=3,suber='amxejegbfxnk').assetResponseFail()
    # passlock.unlock(owner='amxejegbfxnk',lock_id=3,suber='user1') .assetResponseFail()
    # passlock.unlock(owner='user1',lock_id=3,suber='user1') .assetResponseFail()
    # passlock.unlock(owner='amxejegbfxnk',lock_id=300,suber='amxejegbfxnk') .assetResponseFail()
    # passlock.unlock(owner='amxejegbfxnk',lock_id=-1,suber='amxejegbfxnk') .assetResponseFail()
    passlock.unlock(owner='user1',plan_id=8,lock_id=0,suber='user1') 


def test_init():
    passlock.init(nft_contract='amax.ptoken', suber=passlock.contract)
