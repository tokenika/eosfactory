from aplink.farm.farm import farm as f
from aplink.apltoken.apl import apl as a
apl= a()

farm = f()


def test_create_new_lease():
    farm.lease(tenant='aplinknewbie', land_title='newbie reward', land_uri='x',banner_uri ='xx', suber='ad')
    id = farm.getLastRow("aplink.farm","global")["last_lease_id"]
    apl.transfer(fromx='ad',to='aplink.farm',quantity="10000.0000 APL",memo=id,suber='ad')
    print(id)
    
# 放入苹果
def test_transfer(): apl.transfer(fromx='issuer1',to='ad',quantity="1000.0000 APL",memo='5',suber='issuer1')

def test_transfer1(): apl.transfer(fromx='ad',to='aplink.farm',quantity="1000.0000 APL",memo='5',suber='ad')

# 创建农场
def test_lease(): farm.lease(tenant='amax.did4', land_title='DID奖励', land_uri='x',banner_uri ='xx', opened_at='2022-09-29T07:47:00.000', closed_at='2024-08-28T04:04:06.000', suber='ad')
def test_lease2(): farm.lease(tenant='meta.book', land_title='OTC行为奖励', land_uri='x',banner_uri ='xx', opened_at='2022-07-15T02:17:00.000', closed_at='2022-08-28T04:04:06.000', suber='ad')
def test_lease3(): farm.lease(tenant='xchainc', land_title='跨链行为奖励', land_uri='x',banner_uri ='xx', opened_at='2022-07-22T06:56:00.000', closed_at='2023-08-28T04:04:06.000', suber='ad')

def test_lease4(): farm.lease(tenant='merchantx', land_title='测试新版本3', land_uri='x',banner_uri ='xx', suber='ad')


# 领取
def test_pick(): farm.pick(farmer='user1', allot_ids=[35], suber='user1')

# 分配
def test_allot(): farm.allot(lease_id=1, farmer='user1', quantity="1.0000 APL", memo='x', suber='aplinknewbie')

def test_allot2(): farm.allot(lease_id=3, farmer='amvahtxqlrxd', quantity="100.0000 APL", memo='x', suber='xchainc')

def test_allot3(): farm.allot(lease_id=4, farmer='111122223333', quantity="10.0000 APL", memo='x', suber='merchantx')


# 回收
def test_reclaim(): farm.reclaim(land_id=0, recipient='mk', memo='x', suber='ad')

# 设置地主
def test_setlord(): farm.init(lord='ad', jamfactory='ad', suber=farm.contract)


def test_setstatus(): farm.setstatus(land_id=4, status='active', suber='ad')

def test_settenant(): farm.settenant(land_id=3, tenant='algo.fixswap', suber='ad')



