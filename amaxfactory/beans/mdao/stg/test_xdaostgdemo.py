from mdao.stg.xdaostg import XDAOSTG

xdaostg = XDAOSTG()


def test_balancestg(): xdaostg.balancestg(creator='user1', stg_name='x',
                                          weight_value=1, type='user1', ref_contract='user1', ref_sym=1, suber='user1')
                                          
def test_create(): xdaostg.create(creator='user1', stg_name='x', stg_algo='x',
                                  type='user1', ref_contract='user1', ref_sym=1, suber='user1')


def test_publish(): xdaostg.publish(creator='user1', stg_id=1, suber='user1')

def test_remove(): xdaostg.remove(creator='user1', stg_id=1, suber='user1')

def test_setalgo(): xdaostg.setalgo(
    creator='user1', stg_id=1, stg_algo='x', suber='user1')


def test_testalgo(): xdaostg.testalgo(account='user1', stg_id=1, suber='user1')


def test_thresholdstg(): xdaostg.thresholdstg(creator='user1', stg_name='x',
                                              threshold_value=1, type='user1', ref_contract='user1', ref_sym=1, suber='user1')


def test_verify(): xdaostg.verify(creator='user1', stg_id=1,
                                  value=1, expect_weight=1, suber='user1')
