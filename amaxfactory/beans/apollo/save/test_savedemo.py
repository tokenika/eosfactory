from apollo.save.save import SAVE
save = SAVE()
from amax.amaxtoken.amax import AMAX
amax = AMAX()

def test_collectint(): save.collectint(
    issuer='user1', owner='user1', save_id=21, suber='user1')
    # issuer='ad', owner='user1', save_id=6, suber='ad')


def test_delplan(): save.delplan(plan_id=0, suber='ad')

def test_init(): save.init("ad",["8,AMAX","amax.token"],["8,AMAX","amax.token"],["term","lad3",365,"false",0,"2022-09-28T06:30:00","2022-10-28T08:00:00"],suber=save.contract)

def test_setplan(): save.setplan(plan_id=2, pc=["term","lad1",10,"false",5000,"2022-09-28T06:30:00","2022-10-27T06:30:00"], suber='ad')

def test_splitshare(): save.splitshare(
    issuer='user1', owner='user1', suber='user1')

def test_withdraw(): save.withdraw(
    # issuer='user1', owner='user1', plan_id=9, suber='user1')
    issuer='ad', owner='user1', plan_id=6, suber='ad')


def test_transfer(): amax.transfer(fromx='user1', to=save.contract, quantity="10.00000000 AMAX", memo='deposit:3', suber='user1')
