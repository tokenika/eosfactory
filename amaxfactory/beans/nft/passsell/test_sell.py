import time
from nft.passsell.passsell import PASSSELL
from nft.ntoken.ntoken import ntoken as n
from xchain.mtoken.mtoken import Mtoken
mtoken = Mtoken()
ntoken = n()
passsell = PASSSELL()

def test_addproduct(): 
    passsell.addpass(owner='ad', title='pass one', nft_symbol=[2,0],
                                           price="10.000000 MUSDT", started_at="2022-08-16T02:50:00.000", ended_at="2022-09-16T02:50:00.000", suber='ad').assetResponsePass()
    

def test_cancelplan(): 
    passsell.addpass(owner='ad', title='pass one', nft_symbol=[2,0],
                                           price="10.000000 MUSDT", 
                                           started_at="2022-08-16T02:50:00.000", 
                                           ended_at="2022-09-16T02:50:00.000", suber='ad').assetResponsePass()
    product = passsell.getLastRow(passsell.contract, "products")
    id = product["id"]
    passsell.cancelplan(product_id=id, suber='ad').assetResponseFail()

    ntoken.transfer(fromx='ad', to='pass.mart2', assets=[[10,[2,0]]], memo=f'add:{id}', suber='ad').assetResponsePass()
    passsell.cancelplan(product_id=id, suber='user1').assetResponseFail()
    passsell.cancelplan( product_id=id, suber='user1').assetResponseFail()
    passsell.cancelplan(product_id=300, suber='user1').assetResponseFail()
    passsell.cancelplan( product_id=id, suber='ad').assetResponsePass()
    time.sleep(2)
    passsell.cancelplan(product_id=id, suber='ad').assetResponseFail()



def test_claimrewards(): 
    token_id = 10000010

    ntoken.create(issuer='ad', maximum_supply=1000000, symbol=[token_id,0], token_uri=f'xx2xx{ntoken.getCode()}', ipowner='ad',
                                 suber='ad').assetResponsePass()
    ntoken.issue(to='ad', quantity=[1000000,[token_id,0]], memo='x', suber='ad').assetResponsePass()
    passsell.addpass(owner='ad', title='pass one', nft_symbol=[token_id,0],
                                           price="10.000000 MUSDT", 
                                           started_at="2022-08-16T02:50:00.000", 
                                           ended_at="2022-08-26T08:55:00.000", suber='ad').assetResponsePass()
    product = passsell.getLastRow(passsell.contract, "products")
    id = product["id"]
    ntoken.transfer(fromx='ad', to=passsell.contract, assets=[[10,[token_id,0]]], memo=f'add:{id}', suber='ad').assetResponsePass()
    passlock.addplan(owner=passsell.contract, title='pass one lock3',asset_symbol=[token_id,0],unlock_times="2022-08-26T08:55:00.000",suber=passlock.contract) 

    mtoken.transfer(fromx='amxejegbfxnk', to = passsell.contract, quantity = "20.000000  MUSDT", memo = f'buy:{id}:2', suber = 'amxejegbfxnk').assetResponsePass()
    mtoken.transfer(fromx='amusqlyucgzc', to = passsell.contract, quantity = "20.000000  MUSDT", memo = f'buy:{id}:2', suber = 'amusqlyucgzc').assetResponsePass()

    mtoken.transfer(fromx='amusqlyucgzc', to = passsell.contract, quantity = "10.000000  MUSDT", memo = f'buy:{id}:2', suber = 'amusqlyucgzc').assetResponseFail()
    mtoken.transfer(fromx='amusqlyucgzc', to = passsell.contract, quantity = "0.000000  MUSDT", memo = f'buy:{id}:2', suber = 'amusqlyucgzc').assetResponseFail()
    mtoken.transfer(fromx='amusqlyucgzc', to = passsell.contract, quantity = "20.000000  MUSDT", memo = f'buy:{id}:1', suber = 'amusqlyucgzc').assetResponseFail()


    passsell.claimrewards(owner='user1', product_id=id, suber='user1').assetResponseFail()

    time.sleep(60)
    passsell.claimrewards(owner='merchantx', product_id=id, suber='merchantx').assetResponseFail()
    passsell.claimrewards(owner='user1', product_id=id, suber='merchantx').assetResponseFail()
    passsell.claimrewards(owner='merchantx', product_id=id, suber='user1').assetResponseFail()
    passsell.claimrewards(owner='user1', product_id=1000, suber='user1').assetResponseFail()

    passsell.claimrewards(owner='user1', product_id=id, suber='user1').assetResponsePass()
    time.sleep(2)
    passsell.claimrewards(owner='user1', product_id=id, suber='user1').assetResponseFail()

    passsell.claimrewards(owner='amxjzjnokygn', product_id=id, suber='amxjzjnokygn').assetResponsePass()

    # passsell.delprod(id).assetResponsePass()

def test_dealtrace(): passsell.dealtrace(trace=1, suber='user1')

# 初始化
def test_init(): 
    passsell.init(suber=passsell.contract).assetResponseFail()


# 设置收款地址
def test_setaccouts(): 
    passsell.setaccouts(owner='ad', nft_contract='amax.ptoken',lock_contract='pass.lock', partner_name='mk', storage_account='ck', suber='ad').assetResponsePass()
    passsell.setaccouts(owner='user1', nft_contract='amax.ptoken',lock_contract='pass.lock', partner_name='mk', storage_account='ck', suber='ad').assetResponseFail()
    passsell.setaccouts(owner='ad', nft_contract='amax.ptoken',lock_contract='pass.lock', partner_name='mk', storage_account='ck', suber='user1').assetResponseFail()
    passsell.setaccouts(owner='user1', nft_contract='amax.ptoken',lock_contract='pass.lock', partner_name='mk', storage_account='ck', suber='user1').assetResponseFail()

# 设置管理员
def test_setadmin(): 
    passsell.setendtime(admin="ad", pass_id='ad', suber="ad").assetResponsePass()
    passsell.setendtime(admin="adx", pass_id='ad', suber="ad").assetResponseFail()
    passsell.setendtime(admin="ad", pass_id='adx', suber="ad").assetResponseFail()
    passsell.setendtime(admin="ad", pass_id='ad', suber="user1").assetResponseFail()
    passsell.setendtime(admin="user1", pass_id='ad', suber="user1").assetResponseFail()

# 设置领奖时间
def test_setclaimday(): 
    passsell.setclaimday(admin='ad', days=10, suber='ad').assetResponsePass()
    passsell.setclaimday(admin='user1', days=10, suber='ad').assetResponseFail()
    passsell.setclaimday(admin='ad', days=10, suber='user1').assetResponseFail()
    passsell.setclaimday(admin='user1', days=10, suber='user1').assetResponseFail()

# 设置比例
def test_setrates(): 
    passsell.setrates(owner='ad', first_rate=0,second_rate=0, partner_rate=0, suber='ad').assetResponsePass()

    passsell.setrates(owner='ad', first_rate=500,second_rate=1000, partner_rate=1500, suber='ad').assetResponsePass()
    passsell.setrates(owner='user1', first_rate=500,second_rate=1000, partner_rate=1500, suber='ad').assetResponseFail()
    passsell.setrates(owner='ad', first_rate=500,second_rate=1000, partner_rate=1500, suber='user1').assetResponseFail()
    passsell.setrates(owner='user1', first_rate=500,second_rate=1000, partner_rate=1500, suber='user1').assetResponseFail()
    passsell.setrates(owner='ad', first_rate=-1,second_rate=-1, partner_rate=-1, suber='ad').assetResponseFail()
    passsell.setrates(owner='ad', first_rate=10000,second_rate=10000, partner_rate=10000, suber='ad').assetResponseFail()


# 限购
def test_setrule(): 
    passsell.setrule(owner='ad', product_id=2, rule=10, suber='ad').assetResponsePass()
    passsell.setrule(owner='ad', product_id=2, rule=0, suber='ad').assetResponsePass()
    passsell.setrule(owner='user1', product_id=2, rule=0, suber='ad').assetResponseFail()
    passsell.setrule(owner='ad', product_id=2, rule=0, suber='user1').assetResponseFail()
    passsell.setrule(owner='user1', product_id=2, rule=0, suber='user1').assetResponseFail()
    passsell.setrule(owner='ad', product_id=20, rule=0, suber='ad').assetResponseFail()
    passsell.setrule(owner='ad', product_id=2, rule=-1, suber='ad').assetResponseFail()
