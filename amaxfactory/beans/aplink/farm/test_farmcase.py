from time import sleep
from aplink.farm.farm import farm as f
from aplink.apltoken.apl import apl as a
from amax.amaxtoken.amax import AMAX
apl= a()
amax = AMAX()

farm = f()

class TestFarm:
        # 设置地主
    def test_setlord(self): 
        globaltb = farm.getLastRow(farm.contract,"global")
        last_lease_id = globaltb["last_lease_id"] 
        last_allot_id = globaltb["last_allot_id"]
        # farm.init(lord='adx', jamfactory='ck', suber=farm.contract,last_lease_id=last_lease_id,last_allot_id=last_allot_id).assetResponseFail()
        # farm.init(lord='ad', jamfactory='ckx', last_lease_id=last_lease_id,last_allot_id=last_allot_id,suber=farm.contract).assetResponseFail()
        # farm.init(lord='ad', jamfactory='ck',last_lease_id=last_lease_id,last_allot_id=last_allot_id, suber="user1").assetResponseFail()
        farm.init(lord='ad', jamfactory='ck', last_lease_id=last_lease_id,last_allot_id=last_allot_id,suber=farm.contract).assetResponsePass()

    # 创建农场
    def test_lease(self): 
        farm.lease(tenant='xxxx', land_title='下级APL累积达到500，给上级奖励', land_uri='x',banner_uri ='xx', suber='ad').assetResponseFail()
        farm.lease(tenant='user1', land_title='下级APL累积达到500，给上级奖励下级APL累积达到500，给上级奖励下级APL累积达到500，给上级奖励下级APL累积达到500，给上级奖励下级APL累积达到500，给上级奖励下级APL累积达到500，给上级奖励', land_uri='x',banner_uri ='xx',  suber='ad').assetResponseFail()
        farm.lease(tenant='user1', land_title='下级APL累积达到500，给上级奖励', land_uri='下级APL累积达到500，给上级奖励下级APL累积达到500，给上级奖励下级APL累积达到500，给上级奖励下级APL累积达到500，给上级奖励下级APL累积达到500，给上级奖励下级APL累积达到500，给上级奖励',banner_uri ='xx',  suber='ad').assetResponseFail()
        farm.lease(tenant='user1', land_title='下级APL累积达到500，给上级奖励', land_uri='x',banner_uri ='下级APL累积达到500，给上级奖励下级APL累积达到500，给上级奖励下级APL累积达到500，给上级奖励下级APL累积达到500，给上级奖励下级APL累积达到500，给上级奖励下级APL累积达到500，给上级奖励',  suber='ad').assetResponseFail()
        farm.lease(tenant='user1', land_title='下级APL累积达到500，给上级奖励', land_uri='x',banner_uri ='xx', opened_at='2022-08-14T10:29:00.000', closed_at='2022-08-18T04:04:06.000', suber='user1').assetResponseFail()


    # 放入苹果
    def test_transfer(self): 
        test_lease = farm.getLastRowByIndex(farm.contract,'leases','i64',8,8,1)
        available_apples = test_lease['available_apples']
        
        # 测试错误的合约
        amax.transfer(fromx='ad',to=farm.contract,quantity="1.0000 APL",memo='8',suber='ad').assetResponsePass()
        test_lease = farm.getLastRowByIndex(farm.contract,'leases','i64',8,8,1)
        assert available_apples == test_lease['available_apples']
        
        # 测试错误的参数、权限
        apl.transfer(fromx='user1',to=farm.contract,quantity="100.0000 APL",memo='8',suber='user1').assetResponseFail()
        apl.transfer(fromx='ad',to=farm.contract,quantity="100.0000 APL",memo='',suber='ad').assetResponseFail()
        apl.transfer(fromx='ad',to=farm.contract,quantity="100.0000 APL",memo='4000',suber='ad').assetResponseFail()
        
        # 测试关闭状态
        farm.setstatus(8,"inactive",'ad').assetResponsePass()
        apl.transfer(fromx='ad',to=farm.contract,quantity="100.0000 APL",memo='8',suber='ad').assetResponseFail()

        # 启用状态，成功
        farm.setstatus(8,"active","ad").assetResponsePass()
        apl.transfer(fromx='ad',to=farm.contract,quantity="100.0000 APL",memo='8',suber='ad').assetResponsePass()

        test_lease = farm.getLastRowByIndex(farm.contract,'leases','i64',8,8,1)
        available_apples2 = test_lease['available_apples']
        
        amount1 = int(str(available_apples).split(".0000")[0])
        amount2 = int(str(available_apples2).split(".0000")[0])
        assert amount2 == amount1 + 100
        
        # 分配
    def test_allot(self): 
        farm.allot(lease_id=8000, farmer='user1', quantity="1.0000 APL", memo='x', suber='merchantx').assetResponseFail()
        farm.allot(lease_id=8, farmer='userxxx1', quantity="1.0000 APL", memo='x', suber='merchantx').assetResponseFail()
        farm.allot(lease_id=8, farmer='merchantx', quantity="1.0000 APL", memo='x', suber='merchantx').assetResponseFail()
        farm.allot(lease_id=8, farmer='user1', quantity="0.0000 APL", memo='x', suber='merchantx').assetResponseFail()
        farm.allot(lease_id=8, farmer='user1', quantity="-1.0000 APL", memo='x', suber='merchantx').assetResponseFail()
        farm.allot(lease_id=8, farmer='user1', quantity="1.000 APL", memo='x', suber='merchantx').assetResponseFail()
        farm.allot(lease_id=8, farmer='user1', quantity="1.0000 AMAX", memo='x', suber='merchantx').assetResponseFail()
        farm.allot(lease_id=8, farmer='user1', quantity="1.0000 APL", memo='x', suber='user1').assetResponseFail()
    
    def test_allot2(self): 
        
        apl.transfer(fromx='ad',to=farm.contract,quantity="1.0000 APL",memo='8',suber='ad').assetResponsePass()

        test_lease = farm.getLastRowByIndex(farm.contract,'leases','i64',8,8,1)
        available_apples = test_lease['available_apples']
        amount1 = int(str(available_apples).split(".0000")[0])
        amount2 = amount1 + 1
        available_apples2 = str(available_apples).replace(str(amount1),str(amount2))
        # 奖励大于可用应失败
        farm.allot(lease_id=8, farmer='user1', quantity=available_apples2, memo='x', suber='merchantx').assetResponseFail()
        
        farm.allot(lease_id=8, farmer='user1', quantity=available_apples, memo='x', suber='merchantx').assetResponsePass()
        # 可用为0应失败
        farm.allot(lease_id=8, farmer='user1', quantity=available_apples2, memo='x', suber='merchantx').assetResponseFail()
        # 未启用应失败
        apl.transfer(fromx='ad',to=farm.contract,quantity="1.0000 APL",memo='8',suber='ad').assetResponsePass()
        farm.setstatus(8,"inactive",'ad').assetResponsePass()
        farm.allot(lease_id=8, farmer='user1', quantity="1.0000 APL", memo='x', suber='merchantx').assetResponseFail()
        farm.setstatus(8,"active",'ad').assetResponsePass()

        # 未到开启时间
        farm.allot(lease_id=6, farmer='user1', quantity="1.0000 APL", memo='x', suber='merchantx').assetResponseFail()
        # 已到结束时间
        farm.allot(lease_id=7, farmer='user1', quantity="1.0000 APL", memo='x', suber='merchantx').assetResponseFail()

    def test_allot_3(self):
        apl.transfer(fromx='ad',to=farm.contract,quantity="1.0000 APL",memo='8',suber='ad').assetResponsePass()

        test_lease = farm.getLastRowByIndex(farm.contract,'leases','i64',8,8,1)
        alloted_apples1 = test_lease['alloted_apples']
        available_apples1 = test_lease['available_apples']
        amount1 = int(str(available_apples1).split(".0000")[0])
        alloted1 = int(str(alloted_apples1).split(".0000")[0])
        
        farm.allot(lease_id=8, farmer='user1', quantity="1.0000 APL", memo='x', suber='merchantx').assetResponsePass()

        test_lease2 = farm.getLastRowByIndex(farm.contract,'leases','i64',8,8,1)
        alloted_apples2 = test_lease2['alloted_apples']
        available_apples2 = test_lease2['available_apples']
        amount2 = int(str(available_apples2).split(".0000")[0])
        alloted2 = int(str(alloted_apples2).split(".0000")[0])
        
        assert amount2 == amount1 - 1
        assert alloted2 == alloted1 + 1 

        appleid = farm.getLastRow(farm.contract,'allots')['id']
        farm.pick(farmer='user1', allot_ids=[appleid], suber='user1').assetResponsePass()
        
        test_lease3 = farm.getLastRowByIndex(farm.contract,'leases','i64',8,8,1)
        alloted_apples3 = test_lease3['alloted_apples']
        available_apples3 = test_lease3['available_apples']
        amount3 = int(str(available_apples3).split(".0000")[0])
        alloted3 = int(str(alloted_apples3).split(".0000")[0])
        
        assert amount3 == amount2
        assert alloted3 == alloted2 
        assert appleid != farm.getLastRow(farm.contract,'allots')['id']


    
    def test_pick_1(self): 
        apl.transfer(fromx='ad',to=farm.contract,quantity="10.0000 APL",memo='8',suber='ad').assetResponsePass()
        farm.allot(lease_id=8, farmer='user1', quantity="1.0000 APL", memo='x', suber='merchantx').assetResponsePass()
        
        appleid = farm.getLastRow(farm.contract,"global")["last_allot_id"]
        farm.allot(lease_id=8, farmer='ck', quantity="1.0000 APL", memo='x', suber='merchantx').assetResponsePass()

        farm.pick(farmer='user1xx', allot_ids=[appleid], suber='user1').assetResponseFail()
        farm.pick(farmer='user1', allot_ids=[appleid], suber='merchantx').assetResponseFail()
        farm.pick(farmer='user1', allot_ids=[10000], suber='user1').assetResponseFail()
        
        farm.pick(farmer='merchantx', allot_ids=[appleid], suber='merchantx').assetResponseFail()
        farm.pick(farmer='user1', allot_ids=[appleid,appleid+1], suber='user1').assetResponseFail()
        
        farm.pick(farmer='ck', allot_ids=[appleid,appleid+1], suber='ck').assetResponseFail()
        
        farm.pick(farmer='user1', allot_ids=[appleid], suber='user1').assetResponsePass()
        farm.pick(farmer='ck', allot_ids=[appleid+1], suber='ck').assetResponseFail()

    def test_pick2(self):
        apl.transfer(fromx='ad',to=farm.contract,quantity="100.0000 APL",memo='4',suber='ad').assetResponsePass()

        appleid = farm.getLastRow(farm.contract,"global")["last_allot_id"]
        
        for i in range(2):
            farm.allot(lease_id=3, farmer='user1', quantity="0.2000 APL", memo=i, suber='meta.book').assetResponsePass()
        
        rewards = [i+appleid+1 for i in range(2 )]
        # farm.pick(farmer='user1', allot_ids=rewards, suber='user1').assetResponseFail()
        # rewards.pop(0)
        # farm.pick(farmer='user1', allot_ids=rewards, suber='user1').assetResponsePass()

    # 过期测试 , 测试要改代码
    
    def test_pick(self): 
        apl.transfer(fromx='ad',to=farm.contract,quantity="10.0000 APL",memo='8',suber='ad').assetResponsePass()
        
        farm.allot(lease_id=8, farmer='ck', quantity="1.0000 APL", memo='x', suber='merchantx').assetResponsePass()
        appleid = farm.getLastRow(farm.contract,"global")["last_allot_id"]
        sleep(2)
        farm.pick(farmer='ck', allot_ids=[appleid], suber='ck').assetResponsePass()

        farm.allot(lease_id=8, farmer='user1', quantity="1.0000 APL", memo='x', suber='merchantx').assetResponsePass()
        sleep(2)
        farm.pick(farmer='user1', allot_ids=[appleid], suber='user1').assetResponsePass()


    # 回收
    def test_reclaimallot(self): 
        farm.reclaimallot(issuer='ad',allot_id =740, memo='x', suber='ad').assetResponsePass()

    def test_reclaimlease(self): 
        farm.reclaimlease(issuer="ad",lease_id=8,memo='x', suber='ad')



    def test_setstatus(self): farm.setstatus(land_id=0, status=1, suber='ad')

