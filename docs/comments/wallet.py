
from amaxfactory.eosf import *

reset()

create_wallet()
create_master_account("master")
create_account("alice", master)
create_account("carol", master)
get_wallet().keys()

stop()

from amaxfactory.eosf import *

resume()

create_wallet()
get_wallet().keys()

stop()

from amaxfactory.eosf import *

reset()

create_wallet()
get_wallet().keys()

stop()

from amaxfactory.eosf import *

reset()
create_master_account("master")
create_account("alice", master)

get_wallet().index()
get_wallet().open()
get_wallet().unlock()
get_wallet().keys()
get_wallet().lock()

stop()
