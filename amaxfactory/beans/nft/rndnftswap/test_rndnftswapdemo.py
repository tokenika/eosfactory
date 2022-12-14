from nft.rndnftswap.rndnftswap import RNDNFTSWAP
rndnftswap = RNDNFTSWAP()

#base_nft
from nft.ntoken.ntoken import ntoken as n
ntoken = n()

# quote_nft
from kverso.vntoken.vntoken import VNTOKEN
vntoken = VNTOKEN()


def test_init(): rndnftswap.init(admin='ad', suber=rndnftswap.contract)


def test_createbooth(): rndnftswap.createbooth(owner="user1",title="test01",base_nft_contract="pass.ntoken",quote_nft_contract="verso.mid",
quote_nft_price="[3,[20202,0]]",opened_at="2022-8-26T02:50:00.000",close_at="2023-11-27T08:16:00.000", suber='ad')



def test_enablebooth(): rndnftswap.enablebooth(
    owner='user1', quote_nft_contract="verso.mid",symbol_id=2002, enabled='true', suber='user1')



def test_setboothtime(): rndnftswap.setboothtime(
    owner='user1', quote_nft_contract="verso.mid",symbol_id=11010, opened_at="2022-8-26T02:50:00.000", closed_at="2022-10-26T02:50:00.000", suber='user1')


def test_closebooth(): rndnftswap.closebooth(
    owner='user1',quote_nft_contract="verso.mid",symbol_id=2003, suber='user1')


def test_dealtrace(): rndnftswap.dealtrace(trace=1, suber='user1')



#账号之间交易ntoken_nft
def test_transfer3(): ntoken.transfer(fromx='user1', to='ck', assets=[[30,[2003,0]]], memo='refuel:2003', suber='user1')

#账号之间交易vntoken_nft
def test_transfer3(): vntoken.transfer(fromx='user1', to='ck', assets=[[30,[2003,0]]], memo='x', suber='user1')



from otc.otcbook.otcbook import otcbookv as o
book = o()

#仲裁
def test_otc():  book.closearbit(account='mk', deal_id='2023', arbit_result=0, suber='mk')



# 充值nft盲盒, refuel
def test_nft_transfer():
    #转入 
    ntoken.transfer(fromx='ck', to='rndnft.swap1', assets=[[1,[1004,0]]], memo='refuel:verso.mid:2003', suber='ck')


# 抽取盲盒, swap
def test_nft_swap():
    #转入 
    vntoken.transfer(fromx='ck', to='rndnft.swap1', assets=[[15,[2003,0]]], memo='swap', suber='ck')