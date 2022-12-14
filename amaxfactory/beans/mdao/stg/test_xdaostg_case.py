import time
from mdao.stg.xdaostg import XDAOSTG

xdaostg = XDAOSTG()

def test_balancestg_erro(): 
    xdaostg.balancestg(creator='user1xx', stg_name='test',weight_value=1000000, type='tokensum', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponseFail()
    xdaostg.balancestg(creator='ad', stg_name='test',weight_value=1000000, type='tokensum', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponseFail()
    xdaostg.balancestg(creator='user1', stg_name='testxxxxxxxxxxxxxxxxxxxxxtestxxxxxxxxxxxxxxxxxxxxxtestxxxxxxxxxxxxxxxxxxxxxtestxxxxxxxxxxxxxxxxxxxxx',weight_value=1000000, type='tokensum', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponseFail()
    xdaostg.balancestg(creator='user1', stg_name='test',weight_value=0, type='tokensum', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponseFail()
    xdaostg.balancestg(creator='user1', stg_name='test',weight_value=1000000, type='tokensumxxx', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponseFail()
    xdaostg.balancestg(creator='user1', stg_name='test',weight_value=1000000, type='tokensum', ref_contract='aplinkoken', ref_sym='["symbol","4,APL"]', suber='user1').assetResponseFail()
    xdaostg.balancestg(creator='user1', stg_name='test',weight_value=1000000, type='tokensum', ref_contract='aplink.token', ref_sym='["symbol","5,APLX"]', suber='user1').assetResponseFail()
    xdaostg.balancestg(creator='user1', stg_name='test',weight_value=1000000, type='nftbalance', ref_contract='did.ntoken', ref_sym='["nsymbol",[1009,0]]', suber='user1').assetResponseFail()
    xdaostg.balancestg(creator='user1', stg_name='test',weight_value=1000000, type='tokensum', ref_contract='amax.token', ref_sym='["symbol","8,AMAX"]', suber='user1').assetResponseFail()

    # xdaostg.balancestg(creator='user1', stg_name='test',weight_value=1000000, type='tokensum', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponseFail()

def test_balancestg_pass():    
     xdaostg.balancestg(creator='user1', stg_name='test',weight_value=1000000, type='tokenbalance', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponsePass()
     xdaostg.balancestg(creator='user1', stg_name='test',weight_value=1000000, type='tokenbalance', ref_contract='amax.token', ref_sym='["symbol","8,AMAX"]', suber='user1').assetResponsePass()
     xdaostg.balancestg(creator='user1', stg_name='test',weight_value=1000000, type='tokenbalance', ref_contract='amax.mtoken', ref_sym='["symbol","6,MUSDT"]', suber='user1').assetResponsePass()

     xdaostg.balancestg(creator='user1', stg_name='test',weight_value=1000000, type='tokensum', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponsePass()
     xdaostg.balancestg(creator='user1', stg_name='test',weight_value=1000000, type='nftbalance', ref_contract='did.ntoken', ref_sym='["nsymbol",[1,0]]', suber='user1').assetResponsePass()
     xdaostg.balancestg(creator='user1', stg_name='test',weight_value=1000000, type='nparentbalanc', ref_contract='amax.ntoken', ref_sym='["nsymbol",[100,0]]', suber='user1').assetResponsePass()



def test_thresholdstg_erro(): 
    xdaostg.thresholdstg(creator='user1xx', stg_name='test',threshold_value=1000000, type='tokensum', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponseFail()
    xdaostg.thresholdstg(creator='ad', stg_name='test',threshold_value=1000000, type='tokensum', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponseFail()
    xdaostg.thresholdstg(creator='user1', stg_name='testxxxxxxxxxxxxxxxxxxxxxtestxxxxxxxxxxxxxxxxxxxxxtestxxxxxxxxxxxxxxxxxxxxxtestxxxxxxxxxxxxxxxxxxxxx',threshold_value=1000000, type='tokensum', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponseFail()
    # xdaostg.thresholdstg(creator='user1', stg_name='test',threshold_value=0, type='tokensum', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponseFail()
    xdaostg.thresholdstg(creator='user1', stg_name='test',threshold_value=1000000, type='tokensumxxx', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponseFail()
    xdaostg.thresholdstg(creator='user1', stg_name='test',threshold_value=1000000, type='tokensum', ref_contract='aplinkoken', ref_sym='["symbol","4,APL"]', suber='user1').assetResponseFail()
    xdaostg.thresholdstg(creator='user1', stg_name='test',threshold_value=1000000, type='tokensum', ref_contract='aplink.token', ref_sym='["symbol","5,APLX"]', suber='user1').assetResponseFail()
    xdaostg.thresholdstg(creator='user1', stg_name='test',threshold_value=1000000, type='nftbalance', ref_contract='did.ntoken', ref_sym='["nsymbol",[1009,0]]', suber='user1').assetResponseFail()
    xdaostg.thresholdstg(creator='user1', stg_name='test',threshold_value=1000000, type='tokensum', ref_contract='amax.token', ref_sym='["symbol","8,AMAX"]', suber='user1').assetResponseFail()

    # xdaostg.balancestg(creator='user1', stg_name='test',weight_value=1000000, type='tokensum', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponseFail()

def test_thresholdstg_pass():    
     xdaostg.thresholdstg(creator='user1', stg_name='test',threshold_value=1000000, type='tokenbalance', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponsePass()
     xdaostg.thresholdstg(creator='user1', stg_name='test',threshold_value=1000000, type='tokensum', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponsePass()
     xdaostg.thresholdstg(creator='user1', stg_name='test',threshold_value=1000000, type='nftbalance', ref_contract='did.ntoken', ref_sym='["nsymbol",[1,0]]', suber='user1').assetResponsePass()
     xdaostg.thresholdstg(creator='user1', stg_name='test',threshold_value=1000000, type='nparentbalanc', ref_contract='amax.ntoken', ref_sym='["nsymbol",[100,0]]', suber='user1').assetResponsePass()


def test_create_fail(): 
    xdaostg.create(creator='user1xx', stg_name='test',stg_algo="x-100", type='tokensum', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponseFail()
    xdaostg.create(creator='ad', stg_name='test',stg_algo="x-100", type='tokensum', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponseFail()
    xdaostg.create(creator='user1', stg_name='testxxxxxxxxxxxxxxxxxxxxxtestxxxxxxxxxxxxxxxxxxxxxtestxxxxxxxxxxxxxxxxxxxxxtestxxxxxxxxxxxxxxxxxxxxx',stg_algo="x-100", type='tokensum', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponseFail()
    xdaostg.create(creator='user1', stg_name='test',stg_algo="x-100", type='tokensumxxx', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponseFail()
    xdaostg.create(creator='user1', stg_name='test',stg_algo="x-100", type='tokensum', ref_contract='aplinkoken', ref_sym='["symbol","4,APL"]', suber='user1').assetResponseFail()
    xdaostg.create(creator='user1', stg_name='test',stg_algo="x-100", type='tokensum', ref_contract='aplink.token', ref_sym='["symbol","5,APLX"]', suber='user1').assetResponseFail()
    xdaostg.create(creator='user1', stg_name='test',stg_algo="x-100", type='nftbalance', ref_contract='did.ntoken', ref_sym='["nsymbol",[1009,0]]', suber='user1').assetResponseFail()
    xdaostg.create(creator='user1', stg_name='test',stg_algo="x-100", type='tokensum', ref_contract='amax.token', ref_sym='["symbol","8,AMAX"]', suber='user1').assetResponseFail()


def test_create_pass():
     xdaostg.create(creator='user1', stg_name='test',stg_algo="x-100", type='tokenbalance', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponsePass()
     xdaostg.create(creator='user1', stg_name='test',stg_algo="x-100", type='tokensum', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponsePass()
     xdaostg.create(creator='user1', stg_name='test',stg_algo="x-100", type='nftbalance', ref_contract='did.ntoken', ref_sym='["nsymbol",[1,0]]', suber='user1').assetResponsePass()
     xdaostg.create(creator='user1', stg_name='test',stg_algo="x-100", type='nparentbalanc', ref_contract='amax.ntoken', ref_sym='["nsymbol",[100,0]]', suber='user1').assetResponsePass()

def test_verify_fail(): 
    xdaostg.create(creator='user1', stg_name='test',stg_algo="x-100", type='tokenbalance', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponsePass()
    stg_id = xdaostg.getLastRow(xdaostg.contract,'stglist', 80)["id"]

    xdaostg.verify(creator='user1x', stg_id=stg_id,value=200, expect_weight=100, suber='user1').assetResponseFail()
    xdaostg.verify(creator='ad', stg_id=stg_id,value=200, expect_weight=100, suber='user1').assetResponseFail()
    xdaostg.verify(creator='user1', stg_id=stg_id+10,value=200, expect_weight=100, suber='user1').assetResponseFail()
    xdaostg.verify(creator='user1', stg_id=stg_id,value=200, expect_weight=200, suber='user1').assetResponseFail()
    xdaostg.verify(creator='ad', stg_id=stg_id,value=200, expect_weight=100, suber='ad').assetResponseFail()
    xdaostg.verify(creator='user1', stg_id=stg_id,value=200, expect_weight=100, suber='user1').assetResponsePass()

    
    

def test_verify(): 
    xdaostg.create(creator='user1', stg_name='test',stg_algo="x-100", type='tokenbalance', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponsePass()
    stg_id = xdaostg.getLastRow(xdaostg.contract,'stglist', 80)["id"]

    xdaostg.verify(creator='user1', stg_id=stg_id,value=200, expect_weight=100, suber='user1').assetResponsePass()
    
    time.sleep(4)
    xdaostg.verify(creator='user1', stg_id=stg_id,value=200, expect_weight=100, suber='user1').assetResponsePass()
    
    xdaostg.publish(creator='user1', stg_id=stg_id, suber='user1')
    
    time.sleep(4)

    xdaostg.verify(creator='user1', stg_id=stg_id,value=200, expect_weight=100, suber='user1').assetResponseFail()


def test_publish(): 
    xdaostg.create(creator='user1', stg_name='test',stg_algo="x-100", type='tokenbalance', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponsePass()
    stg_id = xdaostg.getLastRow(xdaostg.contract,'stglist', 80)["id"]
    xdaostg.publish(creator='user1', stg_id=stg_id, suber='user1').assetResponseFail()

    xdaostg.verify(creator='user1', stg_id=stg_id,value=200, expect_weight=100, suber='user1').assetResponsePass()

    xdaostg.publish(creator='user1xx', stg_id=stg_id, suber='user1').assetResponseFail()
    xdaostg.publish(creator='user1', stg_id=10086, suber='user1').assetResponseFail()
    xdaostg.publish(creator='ad', stg_id=stg_id, suber='ad').assetResponseFail()
    xdaostg.publish(creator='user1', stg_id=stg_id, suber='ad').assetResponseFail()

    
    time.sleep(2)
    xdaostg.publish(creator='user1', stg_id=stg_id, suber='user1').assetResponsePass()
    
    time.sleep(2)
    xdaostg.publish(creator='user1', stg_id=stg_id, suber='user1').assetResponseFail()
    
    


def test_remove(): 
    xdaostg.create(creator='user1', stg_name='test',stg_algo="x-100", type='tokenbalance', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponsePass()
    stg_id = xdaostg.getLastRow(xdaostg.contract,'stglist',80)["id"]
    
    xdaostg.remove(creator='user1xx', stg_id=stg_id, suber='user1').assetResponseFail()
    xdaostg.remove(creator='user1', stg_id=stg_id+100085, suber='user1').assetResponseFail()
    xdaostg.remove(creator='user1', stg_id=stg_id, suber='ad').assetResponseFail()
    xdaostg.remove(creator='ad', stg_id=stg_id, suber='ad').assetResponseFail()
    
    xdaostg.remove(creator='user1', stg_id=stg_id, suber='user1').assetResponsePass()


    xdaostg.create(creator='user1', stg_name='test',stg_algo="x-100", type='tokenbalance', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponsePass()
    stg_id = xdaostg.getLastRow(xdaostg.contract,'stglist',80)["id"]
    xdaostg.verify(creator='user1', stg_id=stg_id,value=200, expect_weight=100, suber='user1').assetResponsePass()
    time.sleep(2)
    xdaostg.remove(creator='user1', stg_id=stg_id, suber='user1').assetResponsePass()


    xdaostg.balancestg(creator='user1', stg_name='test',
                                          weight_value=1000000, type='tokensum', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponsePass()
    stg_id = xdaostg.getLastRow(xdaostg.contract,'stglist',80)["id"]
    time.sleep(2)
    xdaostg.remove(creator='user1', stg_id=stg_id, suber='user1').assetResponseFail()

    

def test_setalgo(): 
    xdaostg.create(creator='user1', stg_name='test',stg_algo="x-100", type='tokenbalance', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponsePass()
    stg_id = xdaostg.getLastRow(xdaostg.contract,'stglist',80)["id"]
    
    xdaostg.setalgo(creator='user1', stg_id=stg_id, stg_algo='x-200', suber='user1').assetResponsePass()

    stg = xdaostg.getLastRow(xdaostg.contract,'stglist',80)
    assert stg['stg_algo'] == "x-200"
    assert stg['status']   == "testing"
    
    xdaostg.verify(creator='user1', stg_id=stg_id,value=300, expect_weight=100, suber='user1').assetResponsePass()
    xdaostg.setalgo(creator='user1', stg_id=stg_id, stg_algo='x-300', suber='user1').assetResponsePass()

    time.sleep(2)
    xdaostg.verify(creator='user1', stg_id=stg_id,value=400, expect_weight=100, suber='user1').assetResponsePass()
    stg = xdaostg.getLastRow(xdaostg.contract,'stglist',80)
    assert stg['stg_algo'] == "x-300"
    assert stg['status']   == "verified"
    
    xdaostg.setalgo(creator='user1xx', stg_id=stg_id, stg_algo='x-200', suber='user1').assetResponseFail()
    xdaostg.setalgo(creator='user1', stg_id=stg_id+10082, stg_algo='x-200', suber='user1').assetResponseFail()
    xdaostg.setalgo(creator='ad', stg_id=stg_id, stg_algo='x-200', suber='ad').assetResponseFail()
    
    time.sleep(2)

    xdaostg.verify(creator='user1', stg_id=stg_id,value=400, expect_weight=100, suber='user1').assetResponsePass()
    xdaostg.publish(creator='user1', stg_id=stg_id, suber='user1').assetResponsePass()
    xdaostg.setalgo(creator='user1', stg_id=stg_id, stg_algo='x-200', suber='user1').assetResponseFail()
