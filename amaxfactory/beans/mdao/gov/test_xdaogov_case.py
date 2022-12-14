import time
from mdao.propose.xdaopropose import XDAOPROPOSE
xdaopropose = XDAOPROPOSE()

from mdao.stg.xdaostg import XDAOSTG
xdaostg = XDAOSTG()

from mdao.gov.xdaogov import XDAOGOV
xdaogov = XDAOGOV()

from mdao.info.xdaoinfo import XDAOINFO
xdaoinfo = XDAOINFO()

from amax.amaxtoken.amax import AMAX
amax = AMAX()


def test_create_fail(): 
    daocode = f"{xdaoinfo.getCode().lower()}1.dao"
    print(daocode)
    amax.transfer(fromx='user1', to=xdaoinfo.contract, quantity="1.00000000 AMAX", memo=f'{daocode}|{daocode}|{daocode}|https://amaxscan.io/amax.png', suber='user1').assetResponsePass()
    stg_id =28
    
    xdaogov.create(dao_code='abcdabcdabcd',propose_strategy_id=stg_id,vote_strategy_id=stg_id,require_participation=1,require_pass=1,update_interval=2,voting_period=1,suber='user1').assetResponseFail()
    xdaogov.create(dao_code=daocode,propose_strategy_id=stg_id+10083,vote_strategy_id=stg_id,require_participation=1,require_pass=1,update_interval=2,voting_period=1,suber='user1').assetResponseFail()
    xdaogov.create(dao_code=daocode,propose_strategy_id=stg_id,vote_strategy_id=stg_id+10086,require_participation=1,require_pass=1,update_interval=2,voting_period=1,suber='user1').assetResponseFail()
    xdaogov.create(dao_code=daocode,propose_strategy_id=stg_id,vote_strategy_id=stg_id,require_participation=1,require_pass=1,update_interval=2,voting_period=1,suber='ad').assetResponseFail()
    xdaogov.create(dao_code=daocode,propose_strategy_id=stg_id,vote_strategy_id=stg_id,require_participation=1,require_pass=0,update_interval=2,voting_period=1,suber='user1').assetResponseFail()
    xdaogov.create(dao_code=daocode,propose_strategy_id=stg_id,vote_strategy_id=stg_id,require_participation=1,require_pass=0,update_interval=2,voting_period=1,suber='user1').assetResponseFail()

    verified_id = 97
    testing_id = 99
    xdaogov.create(dao_code=daocode,propose_strategy_id=verified_id,vote_strategy_id=stg_id,require_participation=1,require_pass=1,update_interval=2,voting_period=1,suber='user1').assetResponseFail()
    xdaogov.create(dao_code=daocode,propose_strategy_id=testing_id,vote_strategy_id=stg_id,require_participation=1,require_pass=1,update_interval=2,voting_period=1,suber='user1').assetResponseFail()

    xdaogov.create(dao_code=daocode,propose_strategy_id=stg_id,vote_strategy_id=verified_id,require_participation=1,require_pass=1,update_interval=2,voting_period=1,suber='user1').assetResponseFail()
    xdaogov.create(dao_code=daocode,propose_strategy_id=stg_id,vote_strategy_id=testing_id,require_participation=1,require_pass=1,update_interval=2,voting_period=1,suber='user1').assetResponseFail()



    
    xdaogov.create(dao_code=daocode,propose_strategy_id=stg_id,vote_strategy_id=stg_id,require_participation=1,require_pass=1,update_interval=2,voting_period=1,suber='user1').assetResponsePass()
    time.sleep(2)
    xdaogov.create(dao_code=daocode,propose_strategy_id=stg_id,vote_strategy_id=stg_id,require_participation=1,require_pass=1,update_interval=2,voting_period=1,suber='user1').assetResponseFail()


    # xdaogov.create(dao_code=daocode,propose_strategy_id=stg_id,vote_strategy_id=stg_id,require_participation=10002,require_pass=1,update_interval=2,voting_period=1,suber='user1').assetResponseFail()

def test_create(): 
    pass

def test_deletegov(): xdaogov.deletegov(dao_code='user1',suber='user1') 


def get_gov(fromx='user1',require_pass=1,update_interval=1):
    daocode = f"{xdaoinfo.getCode().lower()}1.dao"
    print(daocode)
    amax.transfer(fromx=fromx, to=xdaoinfo.contract, quantity="1.00000000 AMAX", memo=f'{daocode}|{daocode}|{daocode}|https://amaxscan.io/amax.png', suber=fromx).assetResponsePass()
    stg_id =62
    xdaogov.create(dao_code=daocode,propose_strategy_id=stg_id,vote_strategy_id=stg_id,require_participation=1,require_pass=require_pass,update_interval=update_interval,voting_period=1,suber=fromx).assetResponsePass()
    return daocode


def test_propose_setlocktime():
    daocode = get_gov()

    xdaopropose.create(creator='user1',dao_code=daocode, title='test1', desc='x', suber='user1').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 68)["id"]


    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc='x', suber='user1').assetResponsePass()

    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setlocktime', data=f'["setlocktime_data",["{daocode}",3]]', title='test plan', suber='user1').assetResponseFail()
    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setlocktime', data=f'["setlocktime_data",["abcdabcd1234",3]]', title='test plan', suber='user1').assetResponseFail()
    
    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setlocktime', data=f'["setlocktime_data",["{daocode}",0]]', title='test plan', suber='user1').assetResponseFail()
    # xdaopropose.setaction(owner='user1', proposal_id=pp_id,
    #                                         action_name='setlocktime', data=f'["setlocktime_data",["{daocode}",1]]', title='test plan', suber='user1').assetResponseFail()

    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setlocktime', data=f'["setlocktime_data",["{daocode}",4]]', title='test plan', suber='user1').assetResponsePass()
    
    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponsePass()

    xdaopropose.votefor(voter='fee', proposal_id=pp_id, title='test plan', vote='approve', suber='fee').assetResponseFail()

    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponsePass()

    time.sleep(23)

    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponsePass()
    

def test_setlocktime(): 
    daocode = get_gov()
    xdaogov.setlocktime(dao_code='user1',lock_time=3,suber=xdaopropose.contract).assetResponseFail()
    # xdaogov.setlocktime(dao_code=daocode,lock_time=2,suber=xdaopropose.contract).assetResponseFail()
    # xdaogov.setlocktime(dao_code=daocode,lock_time=1,suber=xdaopropose.contract).assetResponseFail()
    xdaogov.setlocktime(dao_code=daocode,lock_time=1,suber='user1').assetResponseFail()

    xdaogov.setlocktime(dao_code=daocode,lock_time=4,suber=xdaopropose.contract).assetResponsePass()
    xdaogov.setlocktime(dao_code=daocode,lock_time=5,suber=xdaopropose.contract) .assetResponseFail()
    
    time.sleep(82)
    xdaogov.setlocktime(dao_code=daocode,lock_time=5,suber=xdaopropose.contract) .assetResponsePass()



def test_setpropmodel(): 
    daocode = get_gov(update_interval=1)
    xdaogov.setpropmodel(dao_code='user1',propose_model='proposal',suber=xdaopropose.contract).assetResponseFail()
    xdaogov.setpropmodel(dao_code=daocode,propose_model='proposalxx',suber=xdaopropose.contract).assetResponseFail()
    xdaogov.setpropmodel(dao_code=daocode,propose_model='proposal',suber='user1').assetResponseFail()

    xdaogov.setpropmodel(dao_code=daocode,propose_model='proposal',suber=xdaopropose.contract).assetResponsePass()
    xdaogov.setpropmodel(dao_code=daocode,propose_model='mix',suber=xdaopropose.contract).assetResponseFail()

    time.sleep(22)

    xdaogov.setpropmodel(dao_code=daocode,propose_model='mix',suber=xdaopropose.contract).assetResponsePass()

def test_setpropmodel_gov(): 
    daocode = get_gov(update_interval=1)

    xdaopropose.create(creator='user1',dao_code=daocode, title='test1', desc='x', suber='user1').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 68)["id"]


    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc='x', suber='user1').assetResponsePass()


    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setpropmodel', data=f'["setpropmodel_data",["abcdabcd1234","proposal"]]', title='test plan', suber='user1').assetResponseFail()
    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setpropmodel', data=f'["setpropmodel_data",["{daocode}","proposalzz"]]', title='test plan', suber='user1').assetResponseFail()
    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setpropmodel', data=f'["setpropmodel_data",["{daocode}","mix"]]', title='test plan', suber='user1').assetResponseFail()
    

    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setpropmodel', data=f'["setpropmodel_data",["{daocode}","proposal"]]', title='test plan', suber='user1').assetResponsePass()
    
    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponsePass()

    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponsePass()

    time.sleep(23)

    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponsePass()



    xdaopropose.create(creator='user1',dao_code=daocode, title='test1', desc='x', suber='user1').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 68)["id"]


    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc='x', suber='user1').assetResponsePass()


    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setpropmodel', data=f'["setpropmodel_data",["{daocode}","mix"]]', title='test plan', suber='user1').assetResponsePass()
    
    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponsePass()

    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponsePass()

    time.sleep(23)

    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponsePass()

def test_setproposestg(): 
    xdaogov.setproposestg(dao_code='user1',propose_strategy_id=1,suber='user1') 
    daocode = get_gov()
    xdaogov.setproposestg(dao_code='user1',propose_strategy_id=28,suber=xdaopropose.contract).assetResponseFail()
    xdaogov.setproposestg(dao_code=daocode,propose_strategy_id=10099,suber=xdaopropose.contract).assetResponseFail()
    # xdaogov.setproposestg(dao_code=daocode,propose_strategy_id=99,suber=xdaopropose.contract).assetResponseFail()
    xdaogov.setproposestg(dao_code=daocode,propose_strategy_id=28,suber="fee").assetResponseFail()


    xdaopropose.create(creator='user1',dao_code=daocode, title='test1', desc='x', suber='user1').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 68)["id"]

    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc='x', suber='user1').assetResponsePass()


    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setproposestg', data=f'["setproposestg_data",["abxd",28]]', title='test plan', suber='user1').assetResponseFail()
    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setproposestg', data=f'["setproposestg_data",["{daocode}",10062]]', title='test plan', suber='user1').assetResponseFail()  
    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setproposestg', data=f'["setproposestg_data",["{daocode}",99]]', title='test plan', suber='user1').assetResponseFail()                                                                               

    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setproposestg', data=f'["setproposestg_data",["{daocode}",28]]', title='test plan', suber='user1').assetResponsePass()
    
    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponsePass()

    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponsePass()

    time.sleep(23)

    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponsePass()
    xdaogov.setproposestg(dao_code=daocode,propose_strategy_id=62,suber=xdaopropose.contract).assetResponseFail()
    time.sleep(23)

    # xdaogov.setproposestg(dao_code=daocode,propose_strategy_id=28,suber=xdaopropose.contract).assetResponseFail()

    xdaogov.setproposestg(dao_code=daocode,propose_strategy_id=62,suber=xdaopropose.contract).assetResponsePass()

def test_setvotestg_gov(): 
    daocode = get_gov()

    xdaopropose.create(creator='user1',dao_code=daocode, title='test1', desc='x', suber='user1').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 68)["id"]


    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc='x', suber='user1').assetResponsePass()


    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setvotestg', data=f'["setvotestg_data",["abcdabcd1234",28,1,1]]', title='test plan', suber='user1').assetResponseFail()
    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setvotestg', data=f'["setvotestg_data",["{daocode}",10086,1,1]]', title='test plan', suber='user1').assetResponseFail()
    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setvotestg', data=f'["setvotestg_data",["{daocode}",99,1,1]]', title='test plan', suber='user1').assetResponseFail()
    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setvotestg', data=f'["setvotestg_data",["{daocode}",28,1,0]]', title='test plan', suber='user1').assetResponseFail()
    

    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setvotestg', data=f'["setvotestg_data",["{daocode}",28,1,1]]', title='test plan', suber='user1').assetResponsePass()
    
    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponsePass()

    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponsePass()

    time.sleep(23)

    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponsePass()

def test_setvotestg(): 
    daocode = get_gov()
    xdaogov.setvotestg(dao_code='user1',vote_strategy_id=28,require_participation=1,require_pass=1,suber=xdaopropose.contract).assetResponseFail()
    xdaogov.setvotestg(dao_code=daocode,vote_strategy_id=10099,require_participation=1,require_pass=1,suber=xdaopropose.contract).assetResponseFail()
    xdaogov.setvotestg(dao_code=daocode,vote_strategy_id=28,require_participation=10001,require_pass=0,suber=xdaopropose.contract).assetResponseFail()
    xdaogov.setvotestg(dao_code=daocode,vote_strategy_id=28,require_participation=1,require_pass=1,suber="fee").assetResponseFail()
    # xdaogov.setvotestg(dao_code=daocode,vote_strategy_id=28,require_participation=1,require_pass=1,suber="user1").assetResponsePass()


    xdaopropose.create(creator='user1',dao_code=daocode, title='test1', desc='x', suber='user1').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 68)["id"]

    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc='x', suber='user1').assetResponsePass()

    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setpropmodel', data=f'["setpropmodel_data",["{daocode}","proposal"]]', title='test plan', suber='user1').assetResponsePass()
    
    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponsePass()

    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponsePass()

    time.sleep(23)

    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponsePass()
    time.sleep(23)

    xdaogov.setvotestg(dao_code=daocode,vote_strategy_id=62,require_participation=1,require_pass=1,suber="user1").assetResponseFail()

    xdaopropose.create(creator='user1',dao_code=daocode, title='test1', desc='x', suber='user1').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 68)["id"]

    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc='x', suber='user1').assetResponsePass()

    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setvotestg', data=f'["setvotestg_data",["{daocode}",28,1,1]]', title='test plan', suber='user1').assetResponsePass()
    
    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponsePass()

    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponsePass()

    time.sleep(23)

    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponsePass()

def test_setvotetime(): 
    daocode = get_gov(update_interval=3)
    xdaogov.setvotetime(dao_code='user1',vote_time=3,suber=xdaopropose.contract).assetResponseFail()
    xdaogov.setvotetime(dao_code=daocode,vote_time=1,suber='user1').assetResponseFail()


    xdaopropose.create(creator='user1',dao_code=daocode, title='test1', desc='x', suber='user1').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 68)["id"]

    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc='x', suber='user1').assetResponsePass()

    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setvotetime', data=f'["setvotetime_data",["abcd",2]]', title='test plan', suber='user1').assetResponseFail()
    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setvotetime', data=f'["setvotetime_data",["{daocode}",1]]', title='test plan', suber='user1').assetResponseFail()
    # xdaopropose.setaction(owner='user1', proposal_id=pp_id,
    #                                             action_name='setvotetime', data=f'["setvotetime_data",["{daocode}",40]]', title='test plan', suber='user1').assetResponseFail()
 
    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
                                            action_name='setvotetime', data=f'["setvotetime_data",["{daocode}",2]]', title='test plan', suber='user1').assetResponsePass()
    
    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponsePass()

    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponsePass()

    time.sleep(23)

    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponsePass()
