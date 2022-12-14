from nft.passsell.passsell import PASSSELL
from xchain.mtoken.mtoken import Mtoken
mtoken = Mtoken()
passsell = PASSSELL()


def test_addproduct(): passsell.addpass(owner='user1', title='pass one', nft_symbol=[1002,0],gift_symbol=[2002,0],
                                           price="5.000000 MUSDT", started_at="2022-10-26T02:50:00.000", ended_at="2022-12-27T09:00:00.000", buy_lock_plan_id=12,token_split_plan_id=30,suber='ad')

def test_cancelplan(): passsell.cancelplan(owner='ad', product_id=5, suber='ad')


def test_claimrewards(): passsell.claimrewards(owner='ad', product_id=5, suber='ad')


def test_dealtrace(): passsell.dealtrace(trace=1, suber='user1')

# 初始化
def test_init(): passsell.init(admin='ad',nft_contract='pass.ntoken',gift_nft_contract='verso.mid',custody_contract='p2.lock',token_split_contract='amax.split2',suber=passsell.contract)


# 设置收款地址
def test_setaccouts(): passsell.setaccouts(nft_contract='pass.ntoken',
                                           lock_contract='p2.lock', partner_name='mk', storage_account='ck',orther='fee', suber='ad')

# 设置结束时间
def test_setendtime(): passsell.setendtime(pass_id=1,sell_ended_at='2022-11-26T06:00:00.000', suber=passsell.contract)

# 设置领奖时间
def test_setclaimday(): passsell.setclaimday(
    admin='ad', days=10, suber='ad')


# 设置比例
def test_setrates(): passsell.setrates(owner='ad', first_rate=500,
                                       second_rate=1000, partner_rate=1500, suber='ad')

# 限购
def test_setrule(): passsell.setrule(
    owner='user1', product_id=1, rule=1, suber='user1')


# 设置拥有者
def test_setowner(): passsell.setowner(pass_id=5,owner='ad', suber=passsell.contract)



#购买pass
def test_bid():
    mtoken.transfer(fromx='ad', to = passsell.contract, quantity = "99.000000  MUSDT", memo = f'buy:3:1', suber = 'ad')#.assetResponsePass()


#删除pass
def test_closepass(): passsell.closepass(pass_id=3, suber='ad')


#购买时, pass的start time<current time
def test_addpass(): passsell.addpass(owner='user1', title='pass one', nft_symbol=[1002, 0], gift_symbol=[2002, 0],
                     price="5.000000 MUSDT", started_at="2022-8-26T02:50:00.000", ended_at="2022-11-26T06:00:00.000", buy_lock_plan_id=12, token_split_plan_id=30, suber='ad') 

#获取passid
def test_get_table(): 
    pass_id = passsell.getLastRow(passsell.contract, "passes")
    #id = product["id"]
    print("get table data:"+str(pass_id))    
    