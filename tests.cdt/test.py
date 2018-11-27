# import eosfactory.core.wallet as wallet
# import eosfactory.core.eosjs as eosjs
from threading import Timer

# wallet.wallet_manager().lock_all()
# owner = eosjs.CreateKey("owner")
# wallet.wallet_manager().import_key("ssasassds", owner)
# wallet.wallet_manager().private_keys("ssasassds")
# wallet.wallet_manager().keys("ssasassds")
# wallet.wallet_manager().create("ssasassds")

def hello():
    print("hello, world")

t = Timer(10.0, hello)
t.start() # after 30 seconds, "hello, world" will be printed