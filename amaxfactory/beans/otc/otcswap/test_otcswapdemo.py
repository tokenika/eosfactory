from otc.otcswap.otcswap import OTCSWAP
otcswap = OTCSWAP()
from amax.arctoken.arc import arc as a
arc = a()

def test_transfer(): arc.transfer(fromx='user1',to=otcswap.contract,quantity="0.1000 BALK",memo='',suber='user1')

def test_setadmin(): otcswap.setconf(conf='otcconf1',suber=otcswap.contract)
def test_settleto(): otcswap.settleto(user='user1',fee="0.100000 MUSDT",quantity="20.000000 MUSDT",suber='meta.book')



