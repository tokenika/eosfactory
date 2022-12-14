from aplink.newbie.newbie import newbie as n

newbie = n()


def test_claimreward(): newbie.claimreward(newbie=['amax.ido'], suber='aplink.admin')


def test_recycledb(): newbie.recycledb(max_rows=1, suber='user1')


def test_rewardinvite(): newbie.rewardinvite(to='user1', suber='user1')


def test_setstate(): newbie.setstate( newbie_reward="100.0000 APL", aplink_token_contract='aplink.token',landid='2',contract="farm3",
                                     suber=newbie.contract)
def test_setstate2(): newbie.setstate2(newbie_reward="100.0000 APL", aplink_token_contract='aplink.token',landid='2',contract="farm3",
                                     suber=newbie.contract)


def test_init(): newbie.init(land_id=1,farm='farmx' ,suber=newbie.contract)
