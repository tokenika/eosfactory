from otc.otcsettle.otcsettle import Otcsettle
from otc.otcconf.otcconfv import otcconfv as o
from base import amcli
otcconfv = o()


otcsettle = Otcsettle()

class TestSettle:

    # 测试异常数据
    def test_deal(self): 
        otcconfv.setsettlelv(configs=[[0,0,0],[1000000000,1000,4000],[3000000000,2500,5000],[6000000000,4000,6000]], suber='ad').assetResponsePass()

        otcsettle.deal(deal_id=10001, merchant='merchantx', user='1234amax1234', quantity="1000.000000 MUSDT",
                                    fee="5.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:36", suber='otcconf1').assetResponseFail()
        otcsettle.deal(deal_id=10001, merchant='merchantxx', user='1234amax1234', quantity="1000.000000 MUSDT",
                                    fee="5.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:36", suber='meta.book').assetResponseFail()
        otcsettle.deal(deal_id=10001, merchant='merchantx', user='1234amax123x', quantity="1000.000000 MUSDT",
                                    fee="5.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:36", suber='meta.book').assetResponseFail()
        otcsettle.deal(deal_id=10001, merchant='merchantx', user='1234amax1234', quantity="1000.000000 MUSDT",
                                    fee="5.000000 MUSDT", arbit_status=0, start_at="2022-07-020T03:13:34", end_at="2022-07-19T03:13:36", suber='meta.book').assetResponseFail()
        reward_id = otcsettle.getLastReward()["id"]
        otcsettle.deal(deal_id=10001, merchant='merchantx', user='1234amax1234', quantity="1000.000000 USDT",
                                    fee="5.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:36", suber='meta.book').assetResponsePass()
        otcsettle.deal(deal_id=10001, merchant='merchantx', user='1234amax1234', quantity="1000.00000 MUSDT",
                                    fee="5.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:36", suber='meta.book').assetResponsePass()
        otcsettle.deal(deal_id=10001, merchant='merchantx', user='1234amax1234', quantity="1000.000000 MUSDT",
                                    fee="5.000000 USDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:36", suber='meta.book').assetResponsePass()
        otcsettle.deal(deal_id=10001, merchant='merchantx', user='1234amax1234', quantity="1000.000000 MUSDT",
                                    fee="5.00000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:36", suber='meta.book').assetResponsePass()
        assert  reward_id == otcsettle.getLastReward()["id"]
        
    # 测试正常数据
    def test_deal2(self):
        otcconfv.setsettlelv(configs=[[0,0,0],[1000000000,1000,4000],[3000000000,2500,5000],[6000000000,4000,6000]], suber='ad').assetResponsePass()

        merchant_settle = otcsettle.getSettle("merchantx")
        user_settle = otcsettle.getSettle("1234amax1234")
        recommender_settle = otcsettle.getSettle("user1")
        
        reward_id = otcsettle.getLastReward()["id"] + 1

        otcsettle.deal(deal_id=10001, merchant='merchantx', user='1234amax1234', quantity="1000.000000 MUSDT",
                                    fee="5.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:44", suber='meta.book').assetResponsePass()
        
        merchant_settle2 = otcsettle.getSettle("merchantx")
        user_settle2 = otcsettle.getSettle("1234amax1234")
        recommender_settle2 = otcsettle.getSettle("user1")
        
        assert int(merchant_settle2["sum_deal"]) == int(merchant_settle["sum_deal"]) + 1000000000
        assert int(merchant_settle2["sum_fee"]) == int(merchant_settle["sum_fee"]) + 5000000
        assert int(merchant_settle2["sum_deal_count"]) == int(merchant_settle["sum_deal_count"]) + 1
        assert int(merchant_settle2["sum_arbit_count"]) == int(merchant_settle["sum_arbit_count"]) 
        assert int(merchant_settle2["sum_deal_time"]) == int(merchant_settle["sum_deal_time"]) + 10

        assert int(user_settle2["sum_deal"]) == int(user_settle["sum_deal"]) + 1000000000
        assert int(user_settle2["sum_fee"]) == int(user_settle["sum_fee"]) + 5000000
        assert int(user_settle2["sum_deal_count"]) == int(user_settle["sum_deal_count"]) + 1
        assert int(user_settle2["sum_arbit_count"]) == int(user_settle["sum_arbit_count"]) 
        assert int(user_settle2["sum_deal_time"]) == int(user_settle["sum_deal_time"]) + 10

        assert int(recommender_settle2["sum_child_deal"]) == int(recommender_settle["sum_child_deal"]) + 1000000000

        last_reward = otcsettle.getLastReward()
        assert reward_id == last_reward["id"]
        assert last_reward["reciptian"] == "user1"
        #  "cash_rate": 4000,
        #   "score_rate": 6000
        assert last_reward["cash"] == "2.000000 MUSDT"
        assert last_reward["score"] == "3.0000 BALC"
    
    # 测试仲裁数据
    def test_deal3(self):
        merchant_settle = otcsettle.getSettle("merchantx")
        user_settle = otcsettle.getSettle("1234amax1234")
        recommender_settle = otcsettle.getSettle("user1")
        
        reward_id = otcsettle.getLastReward()["id"]

        otcsettle.deal(deal_id=10001, merchant='merchantx', user='1234amax1234', quantity="1000.000000 MUSDT",
                                    fee="5.000000 MUSDT", arbit_status=1, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:44", suber='meta.book').assetResponsePass()
        
        merchant_settle2 = otcsettle.getSettle("merchantx")
        user_settle2 = otcsettle.getSettle("1234amax1234")
        recommender_settle2 = otcsettle.getSettle("user1")
        
        assert int(merchant_settle2["sum_deal"]) == int(merchant_settle["sum_deal"]) 
        assert int(merchant_settle2["sum_fee"]) == int(merchant_settle["sum_fee"]) 
        assert int(merchant_settle2["sum_deal_count"]) == int(merchant_settle["sum_deal_count"])
        assert int(merchant_settle2["sum_arbit_count"]) == int(merchant_settle["sum_arbit_count"]) +1
        assert int(merchant_settle2["sum_deal_time"]) == int(merchant_settle["sum_deal_time"]) 

        assert int(user_settle2["sum_deal"]) == int(user_settle["sum_deal"])
        assert int(user_settle2["sum_fee"]) == int(user_settle["sum_fee"]) 
        assert int(user_settle2["sum_deal_count"]) == int(user_settle["sum_deal_count"]) 
        assert int(user_settle2["sum_arbit_count"]) == int(user_settle["sum_arbit_count"]) +1
        assert int(user_settle2["sum_deal_time"]) == int(user_settle["sum_deal_time"]) 

        assert int(recommender_settle2["sum_child_deal"]) == int(recommender_settle["sum_child_deal"])
        
        last_reward = otcsettle.getLastReward()
        assert reward_id == last_reward["id"]

    def teardown(self):
        otcconfv.setsettlelv(configs=[[0,0,0],[1000000000,1000,4000],[3000000000,2500,5000],[6000000000,4000,6000]], suber='ad').assetResponsePass()

    # 测试 现金比例为0
    def test_deal3(self):
        otcconfv.setsettlelv(configs=[[0,0,0],[1000000000,1000,4000],[3000000000,2500,5000],[6000000000,0,6000]], suber='ad').assetResponsePass()
                
        reward_id = otcsettle.getLastReward()["id"] + 1

        otcsettle.deal(deal_id=10001, merchant='merchantx', user='1234amax1234', quantity="1000.000000 MUSDT",
                                    fee="5.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:44", suber='meta.book').assetResponsePass()
     
        last_reward = otcsettle.getLastReward()
        assert reward_id == last_reward["id"]
        assert last_reward["reciptian"] == "user1"
        #  "cash_rate": 0,
        #   "score_rate": 6000
        assert last_reward["cash"] == "0.000000 MUSDT"
        assert last_reward["score"] == "3.0000 BALC"
    
    # 测试积分比例为0
    def test_deal4(self):
        otcconfv.setsettlelv(configs=[[0,0,0],[1000000000,1000,4000],[3000000000,2500,5000],[6000000000,4000,0]], suber='ad').assetResponsePass()
                
        reward_id = otcsettle.getLastReward()["id"] + 1

        otcsettle.deal(deal_id=10001, merchant='merchantx', user='1234amax1234', quantity="1000.000000 MUSDT",
                                    fee="5.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:44", suber='meta.book').assetResponsePass()
     
        last_reward = otcsettle.getLastReward()
        assert reward_id == last_reward["id"]
        assert last_reward["reciptian"] == "user1"
        #  "cash_rate": 4000,
        #   "score_rate": 0
        assert last_reward["cash"] == "2.000000 MUSDT"
        assert last_reward["score"] == "0.0000 BALC"

    # 测试现金、积分比例为0
    def test_deal5(self):
        otcconfv.setsettlelv(configs=[[0,0,0],[1000000000,1000,4000],[3000000000,2500,5000],[6000000000,0,0]], suber='ad').assetResponsePass()
        
        reward_id = otcsettle.getLastReward()["id"] 

        otcsettle.deal(deal_id=10001, merchant='merchantx', user='1234amax1234', quantity="1000.000000 MUSDT",
                                    fee="5.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:44", suber='meta.book').assetResponsePass()
     
        assert reward_id == otcsettle.getLastReward()["id"]

    def test_deal6(self):
        # 获取推荐关系的两个用户
        newuser = amcli.newaccount("user1")
        newuser2 = amcli.newaccount(newuser)
        assert newuser
        assert newuser2
        
        # 验证 0级无奖励、未达到1级
        reward_id = otcsettle.getLastReward()["id"] 

        otcsettle.deal(deal_id=10001, merchant='merchantx', user=newuser2, quantity="100.000000 MUSDT",
                                    fee="0.500000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:44", suber='meta.book').assetResponsePass()
     
        assert reward_id == otcsettle.getLastReward()["id"]
        
        recommender_settle = otcsettle.getSettle(newuser)
        assert int(recommender_settle["sum_child_deal"]) == 100000000
        assert recommender_settle["level"] == 0
        
        # 验证达到1级，有奖励
        otcsettle.deal(deal_id=10001, merchant='merchantx', user=newuser2, quantity="900.000000 MUSDT",
                            fee="5.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:44", suber='meta.book').assetResponsePass()

        reward_id += 1
        last_reward = otcsettle.getLastReward()
        assert reward_id == last_reward["id"]
        
        recommender_settle = otcsettle.getSettle(newuser)
        assert int(recommender_settle["sum_child_deal"]) == 1000000000
        assert recommender_settle["level"] == 1
        assert last_reward["cash"] == "0.500000 MUSDT"
        assert last_reward["score"] == "2.0000 BALC"
        
        # 验证未达到2级
        otcsettle.deal(deal_id=10001, merchant='merchantx', user=newuser2, quantity="100.000000 MUSDT",
                            fee="0.500000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:44", suber='meta.book').assetResponsePass()

        reward_id += 1
        last_reward = otcsettle.getLastReward()
        assert reward_id == last_reward["id"]
        
        recommender_settle = otcsettle.getSettle(newuser)
        assert int(recommender_settle["sum_child_deal"]) == 1100000000
        assert recommender_settle["level"] == 1
        assert last_reward["cash"] == "0.050000 MUSDT"
        assert last_reward["score"] == "0.2000 BALC"
        
        # 验证达到2级，有奖励
        otcsettle.deal(deal_id=10001, merchant='merchantx', user=newuser2, quantity="1900.000000 MUSDT",
                            fee="10.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:44", suber='meta.book').assetResponsePass()

        reward_id += 1
        last_reward = otcsettle.getLastReward()
        assert reward_id == last_reward["id"]
        
        recommender_settle = otcsettle.getSettle(newuser)
        assert int(recommender_settle["sum_child_deal"]) == 3000000000
        assert recommender_settle["level"] == 2
        assert last_reward["cash"] == "2.500000 MUSDT"
        assert last_reward["score"] == "5.0000 BALC"
        
        # 验证未达到3级，有奖励
        otcsettle.deal(deal_id=10001, merchant='merchantx', user=newuser2, quantity="1000.000000 MUSDT",
                            fee="10.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:44", suber='meta.book').assetResponsePass()

        reward_id += 1
        last_reward = otcsettle.getLastReward()
        assert reward_id == last_reward["id"]
        
        recommender_settle = otcsettle.getSettle(newuser)
        assert int(recommender_settle["sum_child_deal"]) == 4000000000
        assert recommender_settle["level"] == 2
        assert last_reward["cash"] == "2.500000 MUSDT"
        assert last_reward["score"] == "5.0000 BALC"
        
        # 验证达到3级，有奖励
        otcsettle.deal(deal_id=10001, merchant='merchantx', user=newuser2, quantity="2000.000000 MUSDT",
                            fee="20.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:44", suber='meta.book').assetResponsePass()

        reward_id += 1
        last_reward = otcsettle.getLastReward()
        assert reward_id == last_reward["id"]
        
        recommender_settle = otcsettle.getSettle(newuser)
        assert int(recommender_settle["sum_child_deal"]) == 6000000000
        assert recommender_settle["level"] == 3
        assert last_reward["cash"] == "8.000000 MUSDT"
        assert last_reward["score"] == "12.0000 BALC"
        

        # 达到3级不增长
        otcsettle.deal(deal_id=10001, merchant='merchantx', user=newuser2, quantity="3000.000000 MUSDT",
                            fee="30.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:44", suber='meta.book').assetResponsePass()

        reward_id += 1
        last_reward = otcsettle.getLastReward()
        assert reward_id == last_reward["id"]
        
        recommender_settle = otcsettle.getSettle(newuser)
        assert int(recommender_settle["sum_child_deal"]) == 9000000000
        assert recommender_settle["level"] == 3
        assert last_reward["cash"] == "12.000000 MUSDT"
        assert last_reward["score"] == "18.0000 BALC"

    def test_pick(self): 
        # 获取推荐关系的两个用户
        newuser = amcli.newaccount("user1")
        newuser2 = amcli.newaccount(newuser)
        assert newuser
        assert newuser2
        
        reward_id = otcsettle.getLastReward()["id"] + 1 

        otcsettle.deal(deal_id=10001, merchant='merchantx', user=newuser2, quantity="1000.000000 MUSDT",
                                    fee="5.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:44", suber='meta.book').assetResponsePass()
     
        last_reward = otcsettle.getLastReward()
        assert reward_id == last_reward['id']
               
        otcsettle.pick(reciptian=newuser2, rewards=[reward_id], suber=newuser).assetResponseFail()
        otcsettle.pick(reciptian=newuser2, rewards=[reward_id], suber=newuser2).assetResponseFail()
        otcsettle.pick(reciptian=newuser, rewards=[reward_id], suber=newuser).assetResponsePass()
        otcsettle.pick(reciptian=newuser, rewards=[reward_id], suber=newuser).assetResponseFail()
        otcsettle.pick(reciptian=newuser, rewards=[10086], suber=newuser).assetResponseFail()
        otcsettle.pick(reciptian=newuser, rewards=[0], suber=newuser).assetResponseFail()

        otcsettle.deal(deal_id=10001, merchant='merchantx', user=newuser2, quantity="1000.000000 MUSDT",
                                    fee="5.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:44", suber='meta.book').assetResponsePass()
        otcsettle.deal(deal_id=10001, merchant='merchantx', user=newuser2, quantity="1000.000000 MUSDT",
                                    fee="5.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:14:44", suber='meta.book').assetResponsePass()
        otcsettle.pick(reciptian=newuser, rewards=[reward_id,reward_id+1,reward_id+2], suber=newuser).assetResponseFail()
        otcsettle.pick(reciptian=newuser, rewards=[reward_id,reward_id+1], suber=newuser).assetResponsePass()


        otcsettle.deal(deal_id=10001, merchant='merchantx', user=newuser2, quantity="1000.000000 MUSDT",
                                    fee="5.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:45", suber='meta.book').assetResponsePass()
        otcsettle.deal(deal_id=10001, merchant='merchantx', user=newuser2, quantity="1000.000000 MUSDT",
                                    fee="5.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:14:46", suber='meta.book').assetResponsePass()
        otcsettle.deal(deal_id=10001, merchant='merchantx', user=newuser, quantity="1000.000000 MUSDT",
                                    fee="5.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:14:46", suber='meta.book').assetResponsePass()
        
        otcsettle.pick(reciptian=newuser, rewards=[reward_id,reward_id+1,reward_id+2], suber=newuser).assetResponseFail()
        otcsettle.pick(reciptian=newuser, rewards=[reward_id,reward_id+1], suber=newuser).assetResponsePass()
        
        rewards = []

        for i in range(21):
            i = i+10
            otcsettle.deal(deal_id=10001, merchant='merchantx', user=newuser2, quantity="10.000000 MUSDT",
                                    fee="0.050000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at=f"2022-06-01T03:14:{i}", suber='meta.book').assetResponsePass()
            
            rewards = [i+reward_id+3 for i in range(21)]
        
        otcsettle.pick(reciptian=newuser, rewards=rewards, suber=newuser).assetResponseFail()

        rewards.pop(0)
        otcsettle.pick(reciptian=newuser, rewards=rewards, suber=newuser).assetResponsePass()

        

    def test_setconfig(self): 
        otcsettle.setconf(conf="otcconfx", suber=otcsettle.contract).assetResponseFail()
        otcsettle.setconf(conf="meta.book", suber=otcsettle.contract).assetResponseFail()
        otcsettle.setconf(conf="metaconf1111", suber="user1").assetResponseFail()
        otcsettle.setconf(conf="metaconf1111", suber=otcsettle.contract).assetResponsePass()
        otcsettle.setconf(conf="otcconf1", suber=otcsettle.contract).assetResponsePass()



    def test_setlevel(self): 
        otcsettle.setlevel(user='user1', level=1, suber='user1').assetResponseFail()
        # otcsettle.setlevel(user='user1x', level=1, suber='ad').assetResponseFail() bug
        otcsettle.setlevel(user='user1', level=-1, suber='ad').assetResponseFail() 
        otcsettle.setlevel(user='user1', level=4, suber='ad').assetResponseFail()

        # 获取推荐关系的两个用户
        newuser = amcli.newaccount("user1")
        newuser2 = amcli.newaccount(newuser)
        assert newuser
        assert newuser2
        
        otcsettle.setlevel(user=newuser, level=2, suber='ad').assetResponsePass()
        
        otcsettle.deal(deal_id=10001, merchant='merchantx', user=newuser2, quantity="100.000000 MUSDT",
                                    fee="5.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:44", suber='meta.book').assetResponsePass()
        
        assert otcsettle.getSettle(newuser)['level'] == 2

        
        otcsettle.deal(deal_id=10001, merchant='merchantx', user=newuser2, quantity="1000.000000 MUSDT",
                                    fee="5.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:44", suber='meta.book').assetResponsePass()
        
        assert otcsettle.getSettle(newuser)['level'] == 2

        otcsettle.deal(deal_id=10001, merchant='merchantx', user=newuser2, quantity="6000.000000 MUSDT",
                                    fee="5.000000 MUSDT", arbit_status=0, start_at="2022-06-01T03:13:34", end_at="2022-06-01T03:13:44", suber='meta.book').assetResponsePass()
        
        assert otcsettle.getSettle(newuser)['level'] == 3
