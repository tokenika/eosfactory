from mdao.propose.xdaopropose import XDAOPROPOSE

xdaopropose = XDAOPROPOSE()


def test_addplan(): xdaopropose.addplan(
    owner='user1', proposal_id=1, title='x', desc='x', suber='user1')


def test_cancel(): xdaopropose.cancel(owner='user1', proposalid=1, suber='user1')

def test_create(): xdaopropose.create(creator='user1',
                                      dao_code='user1', title='x', desc='x', suber='user1')


def test_deletepropose(): xdaopropose.deletepropose(id=1, suber='user1')

def test_deletevote(): xdaopropose.deletevote(id=1, suber='user1')

def test_execute(): xdaopropose.execute(proposal_id=1, suber='user1')

def test_recycledb(): xdaopropose.recycledb(max_rows=1, suber='user1')


def test_setaction(): xdaopropose.setaction(owner='user1', proposal_id=1,
                                            action_name='user1', data=1, title='x', suber='user1')


def test_startvote(): xdaopropose.startvote(
    executor='user1', proposal_id=1, suber='user1')


def test_votefor(): xdaopropose.votefor(
    voter='user1', proposal_id=1, title='x', vote='user1', suber='user1')
