from xchain.mtoken.mtoken import Mtoken

mtoken = Mtoken()


def test_close(): mtoken.close(owner='user1', symbol='8,AMAXAA', suber='user1')


def test_create(): mtoken.create(issuer='user1', maximum_supply="1000000000.000000 MUSDD", suber='user1')


def test_issue(): mtoken.issue(to='ad', quantity="1000000000.000000 MUSDC", memo='x', suber='ad')


def test_open(): mtoken.open(owner='fee', symbol='8,AMAX', ram_payer='user1', suber='user1')


def test_retire(): mtoken.retire(quantity="0.10000000 AMAX", memo='x', suber='user1')

def test_transferx(): mtoken.transfer(fromx='amax.mtoken', to = 'ad', quantity = "100000000.000000 MUSDC", memo = 'x', suber = 'amax.mtoken')


def test_transfer(): mtoken.transfer(fromx='ad', to = 'user1', quantity = "10000.000000 MUSDC", memo = 'x', suber = 'ad')

def test_transfer2(): mtoken.transfer(fromx='merchantx', to = 'meta.book', quantity = "9990.000000  MUSDT", memo = '1:1:1', suber = 'merchantx')

def test_transfer3(): mtoken.transfer(fromx='ad', to = '111122223334', quantity = "200.000000  MUSDT", memo = '123:157:10000000', suber = 'ad')

def test_transfer4(): mtoken.transfer(fromx='user1', to = 'amax.split2', quantity = "2.000000  MUSDT", memo = 'plan:15:2', suber = 'user1')


def test_transfer5(): mtoken.transfer(fromx='ad', to = 'mk', quantity = "1000.000000 MUSDT", memo = 'x', suber = 'ad')