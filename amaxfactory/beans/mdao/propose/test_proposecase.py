import time
from xdaogovcase.test_xdaogov_case import get_gov
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


def test_propose():
    daocode = f"{xdaoinfo.getCode().lower()}1.dao"
    print(daocode)
    amax.transfer(fromx='user1', to=xdaoinfo.contract, quantity="1.00000000 AMAX", memo=f'{daocode}|{daocode}|{daocode}|https://amaxscan.io/amax.png', suber='user1').assetResponsePass()
    
    # xdaostg.balancestg(creator='user1', stg_name='test',
    #                                       weight_value=10000000000, type='tokenbalance', ref_contract='amax.token', ref_sym='["symbol","8,AMAX"]', suber='user1').assetResponsePass()

    xdaostg.balancestg(creator='user1', stg_name='test',
                                          weight_value=1000000, type='tokensum', ref_contract='aplink.token', ref_sym='["symbol","4,APL"]', suber='user1').assetResponsePass()
    # xdaostg.balancestg(creator='user1', stg_name='test',
    #                                       weight_value=1000, type='nparentbalanc', ref_contract='amax.ntoken', ref_sym='["nsymbol",[100,0]]', suber='user1').assetResponsePass()

    # stg_id = xdaostg.getLastRow(xdaostg.contract,'stglist')["id"]
    stg_id =28
    print(stg_id)
    
    xdaogov.create(dao_code=daocode,propose_strategy_id=stg_id,vote_strategy_id=stg_id,require_participation=1,require_pass=1,update_interval=1,voting_period=1,suber='user1').assetResponsePass()

    xdaopropose.create(creator='user1',dao_code=daocode, title='test1', desc='x', suber='user1').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals')["id"]


    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc='x', suber='user1').assetResponsePass()

    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponsePass()

    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponsePass()

    time.sleep(23)

    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponsePass()
    
    


def test_create(): 
    daocode = get_gov()
    xdaopropose.create(creator='user1',dao_code='abcd', title='test title', desc='test desc', suber='user1').assetResponseFail()
    xdaopropose.create(creator='ad',dao_code=daocode, title='test title', desc='test desc', suber='user1').assetResponseFail()
    xdaopropose.create(creator='xxxx',dao_code=daocode, title='test title', desc='test desc', suber='user1').assetResponseFail()
    xdaopropose.create(creator='amax.dao',dao_code=daocode, title='test title', desc='test desc', suber='user1').assetResponseFail()
    xdaopropose.create(creator='user1',dao_code=daocode, title=long_string, desc='test desc', suber='user1').assetResponseFail()
    xdaopropose.create(creator='user1',dao_code=daocode, title='test title', desc=long_string, suber='user1').assetResponseFail()
    xdaopropose.create(creator='fee',dao_code=daocode, title='test title', desc='test desc', suber='fee').assetResponseFail()



def test_cancel(): 
    daocode = get_gov()
    xdaopropose.create(creator='user1',dao_code=daocode, title='test title', desc='test desc', suber='user1').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 100)["id"]

    xdaopropose.cancel(owner='xxx', proposalid=pp_id, suber='user1').assetResponseFail()
    xdaopropose.cancel(owner='ad', proposalid=pp_id, suber='ad').assetResponseFail()
    xdaopropose.cancel(owner='ad', proposalid=pp_id, suber='user1').assetResponseFail()
    xdaopropose.cancel(owner='user1', proposalid=pp_id, suber='ad').assetResponseFail()
    xdaopropose.cancel(owner='user1', proposalid=pp_id+10082, suber='user1').assetResponseFail()


    xdaopropose.cancel(owner='user1', proposalid=pp_id, suber='user1').assetResponsePass()
    time.sleep(2)
    # 已取消，不能取消
    xdaopropose.cancel(owner='user1', proposalid=pp_id, suber='user1').assetResponseFail()

    # 投票中取消
    xdaopropose.create(creator='user1',dao_code=daocode, title='test title', desc='test desc', suber='user1').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 100)["id"]

    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc='x', suber='user1').assetResponsePass()
    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponsePass()
    xdaopropose.cancel(owner='user1', proposalid=pp_id, suber='user1').assetResponsePass()

    # 已执行不能取消
    time.sleep(2)
    xdaopropose.create(creator='user1',dao_code=daocode, title='test title', desc='test desc', suber='user1').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 100)["id"]

    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc='x', suber='user1').assetResponsePass()
    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponsePass()
    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponsePass()
    time.sleep(23)
    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponsePass()
    xdaopropose.cancel(owner='user1', proposalid=pp_id, suber='user1').assetResponseFail()

    # 已过期不能取消
    time.sleep(2)
    xdaopropose.create(creator='user1',dao_code=daocode, title='test title', desc='test desc', suber='user1').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 100)["id"]

    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc='x', suber='user1').assetResponsePass()
    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponsePass()
    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponsePass()
    time.sleep(23)
    xdaopropose.cancel(owner='user1', proposalid=pp_id, suber='user1').assetResponseFail()



def test_addplan(): 
    daocode = get_gov()
    xdaopropose.create(creator='user1',dao_code=daocode, title='test title', desc='test desc', suber='user1').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 100)["id"]

    xdaopropose.addplan(owner='user1xx', proposal_id=pp_id, title='test plan', desc='x', suber='user1').assetResponseFail()
    xdaopropose.addplan(owner='ad', proposal_id=pp_id, title='test plan', desc='x', suber='ad').assetResponseFail()
    xdaopropose.addplan(owner='ad', proposal_id=pp_id, title='test plan', desc='x', suber='user1').assetResponseFail()
    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc='x', suber='ad').assetResponseFail()
    xdaopropose.addplan(owner='user1', proposal_id=pp_id+10082, title='test plan', desc='x', suber='user1').assetResponseFail()
    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title=long_string, desc='x', suber='user1').assetResponseFail()

    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc="long_string", suber='user1').assetResponsePass()
    time.sleep(2)
    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc="xx", suber='user1').assetResponseFail()

    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponsePass()
    
    time.sleep(2)
    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan1', desc=long_string, suber='user1').assetResponseFail()

    
    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponsePass()
    time.sleep(23)
    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponsePass()
    
    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan1', desc="x", suber='user1').assetResponseFail()





def test_setaction(): 
    daocode = get_gov()

    xdaopropose.create(creator='user1',dao_code=daocode, title='test1', desc='x', suber='user1').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 68)["id"]

    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc='x', suber='user1').assetResponsePass()

    xdaopropose.setaction(owner='user1xx', proposal_id=pp_id,
        action_name='setpropmodel', data=f'["setpropmodel_data",["{daocode}","proposal"]]', title='test plan', suber='user1').assetResponseFail()
    xdaopropose.setaction(owner='ad', proposal_id=pp_id,
        action_name='setpropmodel', data=f'["setpropmodel_data",["{daocode}","proposal"]]', title='test plan', suber='user1').assetResponseFail()
    xdaopropose.setaction(owner='ad', proposal_id=pp_id,
        action_name='setpropmodel', data=f'["setpropmodel_data",["{daocode}","proposal"]]', title='test plan', suber='ad').assetResponseFail()
    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
        action_name='setpropmodel', data=f'["setpropmodel_data",["{daocode}","proposal"]]', title='test plan', suber='ad').assetResponseFail()
    xdaopropose.setaction(owner='user1', proposal_id=pp_id+1000,
        action_name='setpropmodel', data=f'["setpropmodel_data",["{daocode}","proposal"]]', title='test plan', suber='user1').assetResponseFail()
    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
        action_name='setpropxxx', data=f'["setpropmodel_data",["{daocode}","proposal"]]', title='test plan', suber='user1').assetResponseFail()
    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
        action_name='setpropmodel', data=f'["setpropmodel_data",["{daocode}"]]', title='test plan', suber='user1').assetResponseFail()
    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
        action_name='setpropmodel', data=f'["setpropmodel_data",["{daocode}","proposal"]]', title='test planx', suber='user1').assetResponseFail()

    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
        action_name='setpropmodel', data=f'["setpropmodel_data",["{daocode}","proposal"]]', title='test plan', suber='user1').assetResponsePass()
    
    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponsePass()

    time.sleep(2)
    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
        action_name='setpropmodel', data=f'["setpropmodel_data",["{daocode}","proposal"]]', title='test plan', suber='user1').assetResponseFail()
    
    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponsePass()

    time.sleep(23)

    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponsePass()
    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
        action_name='setpropmodel', data=f'["setpropmodel_data",["{daocode}","proposal"]]', title='test plan', suber='user1').assetResponseFail()

def test_setaction2(): 
    daocode = get_gov()

    xdaopropose.create(creator='user1',dao_code=daocode, title='test1', desc='x', suber='user1').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 68)["id"]

    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc='x', suber='user1').assetResponsePass()
    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
        action_name='setpropmodel', data=f'["setpropmodel_data",["{daocode}","proposal"]]', title='test plan', suber='user1').assetResponsePass()
    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
        action_name='setvotestg', data=f'["setvotestg_data",["{daocode}",28,1,1]]', title='test plan', suber='user1').assetResponsePass()
    
    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponsePass()
    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponsePass()
    time.sleep(23)
    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponsePass()

def test_setaction3(): 
    daocode = get_gov()

    xdaopropose.create(creator='user1',dao_code=daocode, title='test1', desc='x', suber='user1').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 68)["id"]

    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc='x', suber='user1').assetResponsePass()
    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan2', desc='x', suber='user1').assetResponsePass()

    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
        action_name='setpropmodel', data=f'["setpropmodel_data",["{daocode}","proposal"]]', title='test plan2', suber='user1').assetResponseFail()

    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponsePass()
    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponsePass()
    time.sleep(23)
    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponsePass()

def test_startvote(): 
    daocode = get_gov()
    xdaopropose.create(creator='user1',dao_code=daocode, title='test1', desc='x', suber='user1').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 68)["id"]

    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc='x', suber='user1').assetResponsePass()
    
    xdaopropose.startvote(executor='user1xx', proposal_id=pp_id, suber='user1').assetResponseFail()
    xdaopropose.startvote(executor='ad', proposal_id=pp_id, suber='user1').assetResponseFail()
    xdaopropose.startvote(executor='ad', proposal_id=pp_id, suber='ad').assetResponseFail()
    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='ad').assetResponseFail()
    xdaopropose.startvote(executor='user1', proposal_id=pp_id+1000, suber='user1').assetResponseFail()
    
    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponsePass()
    time.sleep(2)
    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponseFail()

    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponsePass()
    time.sleep(23)
    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponsePass()
    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponseFail()


def test_votefor(): 
    daocode = get_gov()
    xdaopropose.create(creator='user1',dao_code=daocode, title='test1', desc='x', suber='user1').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 68)["id"]

    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc='x', suber='user1').assetResponsePass()
    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan2', desc='x', suber='user1').assetResponsePass()
    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponseFail()

    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponsePass()
    
    xdaopropose.votefor(voter='user1xx', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponseFail()
    xdaopropose.votefor(voter='ad', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponseFail()
    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='ad').assetResponseFail()
    xdaopropose.votefor(voter='fee', proposal_id=pp_id, title='test plan', vote='approve', suber='fee').assetResponseFail()
    xdaopropose.votefor(voter='user1', proposal_id=pp_id+10000, title='test plan', vote='approve', suber='user1').assetResponseFail()
    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approvex', suber='user1').assetResponseFail()
    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test planx', vote='approve', suber='user1').assetResponseFail()
    
    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponsePass()
    xdaopropose.votefor(voter='ad', proposal_id=pp_id, title='test plan2', vote='approve', suber='ad').assetResponsePass()
    xdaopropose.votefor(voter='ck', proposal_id=pp_id, title='test plan', vote='deny', suber='ck').assetResponsePass()
    xdaopropose.votefor(voter='mk', proposal_id=pp_id, title='test plan', vote='waive', suber='mk').assetResponsePass()

    time.sleep(2)
    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponseFail()
    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan2', vote='approve', suber='user1').assetResponseFail()
    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan2', vote='deny', suber='user1').assetResponseFail()
    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='waive', suber='user1').assetResponseFail()

    time.sleep(23)
    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponseFail()
    time.sleep(2)

    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponsePass()
    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponseFail()


def test_execute(): 
    daocode = get_gov()

    xdaopropose.create(creator='user1',dao_code=daocode, title='test1', desc='x', suber='user1').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 68)["id"]

    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponseFail()

    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc='x', suber='user1').assetResponsePass()

    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
        action_name='setpropmodel', data=f'["setpropmodel_data",["{daocode}","proposal"]]', title='test plan', suber='user1').assetResponsePass()

    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponsePass()
    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponseFail()

    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponsePass()
    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponseFail()

    time.sleep(23)
    
    xdaopropose.execute(proposal_id=pp_id+10085, suber='user1').assetResponseFail()
    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponsePass()
    time.sleep(2)
    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponseFail()


def test_execute2(): 
    daocode = get_gov(require_pass=2)

    xdaopropose.create(creator='user1',dao_code=daocode, title='test1', desc='x', suber='user1').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 68)["id"]

    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc='x', suber='user1').assetResponsePass()

    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
        action_name='setpropmodel', data=f'["setpropmodel_data",["{daocode}","proposal"]]', title='test plan', suber='user1').assetResponsePass()

    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponsePass()

    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponsePass()

    time.sleep(23)
    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponseFail()

def test_execute3(): 
    daocode = get_gov()

    xdaopropose.create(creator='user1',dao_code=daocode, title='test1', desc='x', suber='user1').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 68)["id"]

    xdaopropose.addplan(owner='user1', proposal_id=pp_id, title='test plan', desc='x', suber='user1').assetResponsePass()

    xdaopropose.setaction(owner='user1', proposal_id=pp_id,
        action_name='setpropmodel', data=f'["setpropmodel_data",["{daocode}","proposal"]]', title='test plan', suber='user1').assetResponsePass()

    xdaopropose.startvote(executor='user1', proposal_id=pp_id, suber='user1').assetResponsePass()

    xdaopropose.votefor(voter='user1', proposal_id=pp_id, title='test plan', vote='approve', suber='user1').assetResponsePass()
    xdaopropose.votefor(voter='ck', proposal_id=pp_id, title='test plan', vote='deny', suber='ck').assetResponsePass()

    time.sleep(23)
    xdaopropose.execute(proposal_id=pp_id, suber='user1').assetResponseFail()


long_string = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


def test_setaction_1(): 
    daocode = get_gov(fromx='ad')

    xdaopropose.create(creator='ad',dao_code=daocode, title='test1', desc='x', suber='ad').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 68)["id"]

    xdaopropose.addplan(owner='ad', proposal_id=pp_id, title='test plan', desc='x', suber='ad').assetResponsePass()

    xdaopropose.setaction(owner='ad', proposal_id=pp_id,
        action_name='updatedao', data=f'["updatedao_data",["ad","{daocode}","update_logo1","update_des1c",[["u3rl","updat2e_url"]],"MUSDT","amax.mtoken","2"]]', title='test plan', suber='ad').assetResponsePass()

    xdaopropose.startvote(executor='ad', proposal_id=pp_id, suber='ad').assetResponsePass()

    xdaopropose.votefor(voter='ad', proposal_id=pp_id, title='test plan', vote='approve', suber='ad').assetResponsePass()

    time.sleep(23)
    xdaopropose.execute(proposal_id=pp_id, suber='ad').assetResponsePass()

def test_setaction_2(): 
    daocode = get_gov(fromx='ad')

    xdaopropose.create(creator='ad',dao_code=daocode, title='test1', desc='x', suber='ad').assetResponsePass()
    pp_id = xdaopropose.getLastRow(xdaopropose.contract,'proposals', 68)["id"]

    xdaopropose.addplan(owner='ad', proposal_id=pp_id, title='test plan', desc='x', suber='ad').assetResponsePass()

    xdaopropose.setaction(owner='ad', proposal_id=pp_id,
        action_name='bindtoken', data=f'["bindtoken_data",["ad","{daocode}",["6,MUSDT","amax.mtoken"]]]', title='test plan', suber='ad').assetResponsePass()

    xdaopropose.startvote(executor='ad', proposal_id=pp_id, suber='ad').assetResponsePass()

    xdaopropose.votefor(voter='ad', proposal_id=pp_id, title='test plan', vote='approve', suber='ad').assetResponsePass()

    time.sleep(23)
    xdaopropose.execute(proposal_id=pp_id, suber='ad').assetResponsePass()
    